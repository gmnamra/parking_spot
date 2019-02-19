# Assignment: Identify cars parked in the marked spot 

## General
Please follow the setup section carefully. The steps in the Scripts section correpond to the steps outlined in the cv-assignment. Improvements and issues are listed and discussed in each section. Video files and frames extracted from stored and cached in an internal download directory. Referencing them is exactly as specified in the assignment. 


### Setup 
yolov3.weights is in the repository of this solution ( through Large File Size support). Additionally https://hiring.verkada.com/video/index.txt is downloaded if it is needed. A copy downloaded earlier is in the repository. 
The following python3 packages are required
**Opencv 3
numpy
matplotlib**

### Scripts
#### Fetch and Extract
##### basic
fetch-and-extract.sh calls a python script to download the video file, open and extract the first frame. Both video and image file are downloaded to a default folder where the script first checks to see if the video file as well as the first frame have already been downloaded. Python script uses *htmllistparse* to generate a list of files available and *requests* lib to initiate tcp connection and follow it up with writing arrived data to a local file. 
##### Improvements
###### Threading
Implementation python file: fetchandextract.py contains and implementation of threaded downloader class derived from threading.thread class. The constructor takes the above download information and calls the same python method to download the file but *runs it in its own thread* thus allowing us to download multiple video files simultaneously. 
###### Video File Storage
In dealing with a large number of extractions, a better choice of video file temporary storage is OS's shared memory ( files stored in memory ). 
###### Concurrent downloading and preprocessing
		
#### has-car *Using Yolov3*
##### basic
	Process Entire timestamped frame
	Post process
		reject all candidates not classified as 'car'
		threshold by confidence result
		Computed intersection over union bounding between Parking Spot and candidate bounding box
		
###### YOLOv3 Network
 -  yolov3.cfg and yolov3.weights from https://pjreddie.com/yolo/.
 -  Trained on 80 object categories (COCO dataset). 
 -  Input image size: 416 by 416. 
 	
##### Issues
		Clutter: Parked Car with door/trunk/etc open
		Moved: 
			 Car -> Same Car Partial  ( pulling in to parking spot )
			 Same Car Partial -> Empty  ( pulling in out of the parking spot )
		Other Clutter ( shadows, etc )
			 
#### same-car *Using Yolov3*
##### basic
##### Issues
		Possible sequential timestamp changes observed in the parking spot
			 Car -> Same Car Partial  ( pulling in to parking spot )
			 Same Car Partial -> Empty  ( pulling in out of the parking spot )
			 Parked Car -> Same Parked Car with door/trunk/etc open
			 Psrked Car -> Next Parked Car


#### analyze-cars.py 
##### basic
##### Improvements

#### Discussion


### Camera Outside Overlooking Street:
 -  Rigidly mounted. 
 -  Capture parameters set. 
 -  Camera / Viewing pose set.
 -  Spot marked center at TL (235,235)


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTgwOTE1NjQ3MiwtMTAwMzcxMTM5NSwtOT
Q0MjM3MTIsLTkzODY4MTk3NSwtMTAwODkxNTIzMiwtMTE4MDQ1
Mzk0Nl19
-->