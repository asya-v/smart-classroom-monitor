# Smart Classroom Monitor

A computer vision project for monitoring room occupancy using YOLO and OpenCV.

The system detects and counts people in real time, displays the current and maximum occupancy, tracks how long the room has been occupied, and records overcrowding events.

## Features

* real-time person detection using YOLOv8;
* current and maximum people count;
* room status: `EMPTY`, `OCCUPIED`, or `CROWDED`;
* occupied time tracking;
* event logging;
* automatic screenshots when the occupancy limit is exceeded;
* support for a phone IP camera or a computer webcam.

## Technologies

* Python
* YOLOv8
* OpenCV

## Installation

```bash
pip install ultralytics opencv-python
```

## Camera Setup

For a phone IP camera, change the camera address in the code:

```python
CAMERA_URL = "http://YOUR_PHONE_IP:8080/video"
```

For a computer webcam, use:

```python
CAMERA_URL = 0
```

## Run

```bash
python smart_classroom_monitor.py
```

Press `Q` to close the program.

## Output

The program:

* draws bounding boxes around detected people;
* displays occupancy information on the video;
* writes data to `people_log.txt`;
* saves overcrowding screenshots in the `screenshots` folder.

## Status

Educational computer vision project created during an AI Engineering course at American Corner & Makerspace Astana.
