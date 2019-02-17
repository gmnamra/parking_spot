# Assignment: Identify cars parked in the spot marked 

## Sections
### How to build & Run
### Steps
#### Fetch and Extract
##### basic
fetch-and-extract.sh calls a python script to download the video file, open and extract the first frame. Both video and image file are downloaded to a default folder where the script first checks to see if the video file as well as the first frame have already been downloaded. Python script uses *htmllistparse* to generate a list of files available and *requests* lib to initiate tcp connection and follow it up with writing arrived data to a local file. 
##### Improvements
###### Threading
Implementation python file: fetchandextract.py contains and implementation of threaded downloader class derived from threading.thread class. The constructor takes the above download information and calls the same python method to download the file but *runs it in its own thread*.  
#### Extract Car Using Yolov3
##### basic
##### Improvements
#### Same Car
##### basic
##### Improvements
#### All together
##### basic
##### Improvements

#### Discussion


### Camera Outside Overlooking Street:
 - [x] Rigidly mounted. 
 - [x] Capture parameters set. 
 - [x] Camera / Viewing pose set.
 - [x] Spot marked center at TL (235,235)


<!--stackedit_data:
eyJoaXN0b3J5IjpbNTYwMjgzMTQxLC05NDQyMzcxMiwtOTM4Nj
gxOTc1LC0xMDA4OTE1MjMyLC0xMTgwNDUzOTQ2XX0=
-->