<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>README</title>
  <link rel="stylesheet" href="https://stackedit.io/style.css" />
</head>

<body class="stackedit">
  <div class="stackedit__html"><h1 id="assignment-identify-cars-parked-in-the-spot-marked">Assignment: Identify cars parked in the spot marked</h1>
<h2 id="sections">Sections</h2>
<h3 id="how-to-build--run">How to build &amp; Run</h3>
<h3 id="steps">Steps</h3>
<h4 id="fetch-and-extract">Fetch and Extract</h4>
<h5 id="basic">basic</h5>
<p><a href="http://fetch-and-extract.sh">fetch-and-extract.sh</a> calls a python script to download the video file, open and extract the first frame. Both video and image file are downloaded to a default folder where the script first checks to see if the video file as well as the first frame have already been downloaded. Python script uses <em>htmllistparse</em> to generate a list of files available and <em>requests</em> lib to initiate tcp connection and follow it up with writing arrived data to a local file.</p>
<h5 id="improvements">Improvements</h5>
<h6 id="threading">Threading</h6>
<p>Implementation python file: <a href="http://fetchandextract.py">fetchandextract.py</a> contains and implementation of threaded downloader class derived from threading.thread class. The constructor takes the above download information and calls the same python method to download the file but <em>runs it in its own thread</em> thus allowing us to download multiple video files simultaneously.</p>
<h6 id="video-file-storage">Video File Storage</h6>
<p>In dealing with a large number of extractions, a better choice of video file temporary storage is OS’s shared memory ( files stored in memory ).</p>
<h6 id="concurrent-downloading-and-preprocessing">Concurrent downloading and preprocessing</h6>
<h4 id="has-car-using-yolov3">has-car <em>Using Yolov3</em></h4>
<h5 id="basic-1">basic</h5>
<h5 id="improvements-1">Improvements</h5>
<h4 id="same-car-using-yolov3">same-car <em>Using Yolov3</em></h4>
<h5 id="basic-2">basic</h5>
<h5 id="improvements-2">Improvements</h5>
<h4 id="all-together">All together</h4>
<h5 id="basic-3">basic</h5>
<h5 id="improvements-3">Improvements</h5>
<h4 id="discussion">Discussion</h4>
<h3 id="camera-outside-overlooking-street">Camera Outside Overlooking Street:</h3>
<ul>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Rigidly mounted.</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Capture parameters set.</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Camera / Viewing pose set.</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Spot marked center at TL (235,235)</li>
</ul>
</div>
</body>

</html>
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTk5NzIxODY1OV19
-->