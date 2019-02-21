
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
		sensitivity to bounding box variations between cars. 
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
		
	
		Measuring Similarity 
		Since the *viewing setup* is shared, the difference in appearances is constrained to minor translations 
		and changes in **shape** due to changes in color and brightness. My approach to make our same-car approach invariant to the above 
		is as follow:
		- minor-movement and coarse comparison:
			I use a template matching method to measure where and how well spot in one time/place point appears 
			in the other. We use Normalized Correlation metric as it is invariant to linear changes in contrast.
			We will convert the 3 channel BGR image to a single channel gray. Same colors produce same gray however 
			the distance between colors is attenueted in converted gray. There are many good alternatives and we can assess them if sensitivity 
			is revealed as an issue. 
			
			Specifically, the image roi in one image is matched in an expanded roi in the other image. A threshold of 0.5 is used. 
			
		Combining DL & Similarity
			two cars are considered the same iff:
				if DL detects a car in at least one of the two spots and image ROIs match better than similarity threshold
			two cars are considered NOT the same car iff:
				Regardless of DL results, if the image ROIs match lower than the image similarity threshold. 
			
##### Issues
		Possible changes present in sequential timestamp captures of the parking spot
			 Car -> Same Car Partial  ( pulling in to parking spot )
			 Same Car Partial -> Empty  ( pulling in out of the parking spot )
			 Parked Car -> Same Parked Car with door/trunk/etc open
			 Psrked Car -> Next Parked Car


#### analyze-cars.py 
	analyze car applies has-car to every first frame extracted from videos in the time range. 
##### basic	
	A pipeline of two timestamps is used to validate the 
	assessment using the is-same-car method above. A small simple state machine is used to run this pipeline and generate results. 

#### Issues
	

#### Explorations
		Parking Lot detection
			Two patterns suggest a parking lot ( single floor and flat plane )
				- Visible Boundary Lines separating spots
				- Cars parked in row / column organization
				
				Visible Boundary lines can be detected robustly if correctly implemented 
				Locations of multiple cars detected by DL/yolov3 can be processed to detect row / column organization
			
			Issues: 
				Parked cars can obscure boundary lines.
				Needs enough resolution for detecting boundary lines (8-16 pixels across)
				Needs as many spots to have a good estimate of parking lot presence and location
				

	



