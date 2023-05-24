# sotolab-robotic-prey-fish

## First time setup and running:

* plug in camera and transmit board
* place robot near the start position and turn on (all the way, both clicks)
* open up controller.py
* find ports:
  * find transmit board serial port by opening at terminal and typing ls /dev/tty.usb*
  * in main, switch out port_t with the listed port
  * port_c is the camera port and is either 0 or 1. find with guess and check
* if the camera or tank have been moved:
  * find the new bounds of the tank from the camera's view with calibrate_setup.py
  * copy those new bounds into main
* click the ol' "run python file" button and watch the robot go

## Code overview:

### cyberbot directory
has code for micro:bits, generally this does not need updating

* to upload new code, paste into main.py, open just the "for running" directory and upload from there
* receiver.py and transmitter.py store the code for those chips
* if stuck, see https://www.youtube.com/watch?v=eSGJLu1kqyg
* display.scroll("text") is useful for quick debugging

### src directory 
has code for running the bot

* controller.py is the top-level class that creates instances of data_handler and video_processor
* paths.py and point_tracker.py are also necessary helper files
* analyze_data is for post-processing, and kalman.py is a kalman filter


### testing sub-directory 
has some test files that may be useful or may be antiquated/broken

* calibrate_setup.py is for finding the bounds of the tank from the camera's view (in pixels)
* collectImages.py is for taking photos from the video stream
* drawTrajectory.py draws a path
* imageProcessing tests the camera subsystem
* pathTrackerSim tests the path tracking performance, but likely is unrealistic and not useful
* sendCommandsSimple tests the robot subsystem
* wallPotentialField visualizes the artificial potential field algorithm

### data directory
should ideally take care of itself. the DataHandler object controller.py instantiates should populate it with data files as directed, with sub-directories and filenames corresponding to the day's date and time

## Known issues:

* calibrate_setup.py has problems
* saving video files is untested but likely works
* pixels to meters conversion should be automated
* new code does not implement desired angle tracking (gain for beta = 0)
* new code does not implement delayed start functionality (robot starts as soon as the file is run. it could be useful to implement a delay that waits for the user to press a key for the trajectory to begin. this is partially implemented with the "go" boolean in the VideoProcesor)
* kalman filter should implement an actual motion model (prediction step)
* radio communication may be dropping some transmissions
