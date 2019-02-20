
# Assignment: Identify cars parked in the marked spot 

## General
Please follow the setup section carefully. The steps in the Scripts section correpond to the steps outlined in the cv-assignment. Improvements and issues are listed and discussed in each section. Video files and frames extracted from stored and cached in an internal download directory. Referencing them is exactly as specified in the assignment. 


### Setup 
yolov3.weights is in the repository of this solution ( through Large File Size support). Additionally https://hiring.verkada.com/video/index.txt is downloaded if it is needed. A copy downloaded earlier is in the repository. 
The following python3 packages are required
**Opencv 3
numpy
matplotlib**


### Viewing Setup
Camera Outside Overlooking Street:
 -  Rigidly mounted. 
 -  Capture parameters set. 
 -  Camera / Viewing pose set.
 -  Spot marked center at TL (235,235)

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
		We define same-car as the **same** car occupying 
		- the parking spot at tow different time point or,
		- two different parking spots at same or different time points 
		
		Our DL model can only report if there is "anything" like a car in each spot. 
		Since the *viewing setup* is shared, the difference in appearances is constrained to minor translations 
		and changes in **shape** due to changes in color and brightness. My approach to make our same-car approach invariant to the above 
		is as follow:
		- minor-movement and coarse comparison:
			We use a template matching method to measure where and how well spot in one time/place point appears 
			in the other. We use Normalized Correlation metric as it is invariant to linear changes in contrast.
			We will convert the 3 channel BGR image to a single channel gray. Same colors produce same gray however 
			the difference is attenueted in gray. There are many good alternatives and we can assess them if sensitivity 
			is revealed as an issue. 
		- to compare color signature I compute mutual information between color axis for each image. In other words, how does one color axis 
			 is predicted by the other. Among color spaces, distance between colors are most correlated with human perception 
			 in Lab color space. BGR images are converted to Lab color space. **L** represents the luminance channel as measured from a 
			 reference white point. **a** and **b** are chromatic channels. 
		
		
		
		
		
		
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

