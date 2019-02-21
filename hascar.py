
import cv2 as cv
import sys
import numpy as np
from rectangle import intersection_over_union
from common import __this_spot__
import match
from fetchandextract import fetch_first_frame



# Initialize the parameters
confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
iouThreshold = 0.4
inpWidth = 416  # Width of network's input image
inpHeight = 416  # Height of network's input image

# Load names of classes
classesFile = "coco.names";
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
carClassIndex = classes.index('car')

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "yolov3.cfg";
modelWeights = "yolov3.weights";

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(frame, classId, conf, iou, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 2)

    label = '%.2f:%.3f' % (conf, iou)

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_TRIPLEX, 0.6, 1)
    top = max(top, labelSize[1])

    #
    # cv.rectangle(frame, (left, top - round(1.25 * labelSize[1])),
    #             (left + round(1.25 * labelSize[0]), top + baseLine),
    #             (128,128,128), cv.FILLED)

    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_TRIPLEX, 0.6, (0, 0, 0), 1)


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs, parkingSpot, show):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    parkingSpot_width = parkingSpot[3] - parkingSpot[1]
    parkingSpot_height = parkingSpot[2] - parkingSpot[0]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    ious = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            if not classId == carClassIndex:
                continue
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)

                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                bbox = [left, top, left + width, top + height]
                iou = intersection_over_union(bbox, parkingSpot)
                if iou < iouThreshold:
                 continue

                ious.append(iou)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    # Return the first pass or failure if none
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        if show:
            drawPred(frame, classIds[i], confidences[i], ious[i], left, top, left + width, top + height)
        return True
    return False


def process(filename, show):
    # Process inputs
    if show:
        winName = 'Parking Lot Monitoring'
        cv.namedWindow(winName, cv.WINDOW_NORMAL)

    frame = cv.imread(filename)

    msg = 'running yolo3 on ' + filename
    print(msg)

    # Create a 4D blob from a frame.
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

    # Sets the input to the network
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(getOutputsNames(net))

    # Remove the bounding boxes with low confidence
    parkingSpot = __this_spot__
    assessment = postprocess(frame, outs, parkingSpot, show)

    # Put efficiency information.
    # The function getPerfProfile returns the overall time for inference(t) and
    # the timings for each of the layers(in layersTimes)
    if show:
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        cv.rectangle(frame, (parkingSpot[0],parkingSpot[1]), (parkingSpot[2], parkingSpot[3]), (50, 255, 50), 3)
        while cv.waitKey(1) < 0:
            cv.imshow(winName, frame)
    return assessment


def compare(filename_a, filename_b, show=False):
    yolo3_a = process(filename_a, show)
    yolo3_b = process(filename_b, show)
    imga = cv.imread(filename_a)
    imgb = cv.imread(filename_b)
    # Crop at the spot
    parkingSpot = __this_spot__
    roi_a = imga[parkingSpot[0]:parkingSpot[2], parkingSpot[1]: parkingSpot[3]]
    roi_b = imgb[parkingSpot[0]:parkingSpot[2], parkingSpot[1]: parkingSpot[3]]
    mi_a, h_a = match.LabMutualInformation(roi_a)
    mi_b, h_b = match.LabMutualInformation(roi_b)

    r = match.correlate(h_a, h_b)
    if show:
        match.mi_lum(roi_a, roi_b)

    roi_a_wider = imga[parkingSpot[0]-5:parkingSpot[2]+5, parkingSpot[1]-5: parkingSpot[3]+5]
    res = match.find_template(roi_a_wider,roi_b)

    if yolo3_a or yolo3_b:
        return res[1] > 0.5
    return False






if __name__ == '__main__':

    # compare(image_filename_a, image_filename_b)

    show = False
    files = []
    options = []
    exec_filename = sys.argv[0]

    for idx, arg in enumerate(sys.argv):
        if arg == exec_filename: continue
        if arg == 'show':
            options.append("show")
            continue
        ok = fetch_first_frame(arg)
        if ok[0]:
            files.append(ok[1])


    show = len(options) == 1
    if len(files) == 1:
        found = process(files[0], show)
        if not found:
            print('no car detected')
        else:
            print('car detected')
    elif len(files) == 2:
        is_same = compare(files[0], files[1], show)
        if not is_same:
            print('Different Cars')
        else:
            print('Same Cars')


