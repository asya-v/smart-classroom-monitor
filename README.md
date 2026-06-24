# Smart Classroom Monitor

A computer vision project for monitoring classroom occupancy using YOLO.

The system detects and counts people in real time, estimates the occupancy level, and records overcrowding events.

## Features

* real-time person detection using YOLO;
* current and maximum occupancy count;
* classroom status: `EMPTY`, `OCCUPIED`, or `CROWDED`;
* overcrowding detection based on a selected limit;
* screenshot capture when the limit is exceeded;
* event logging.

## Technologies

* Python
* YOLO
* OpenCV

## How It Works

The program receives a video stream from a camera, detects people in each frame, and counts them.

Based on the number of detected people, it displays the current room status. When the occupancy limit is exceeded, the program saves a screenshot and records the event in a log file.

## Possible Applications

* classrooms;
* offices;
* meeting rooms;
* public spaces.

## Status

Educational computer vision project completed during an AI Engineering course at American Corner & Makerspace Astana.
