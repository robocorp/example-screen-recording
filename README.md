# example-screen-recording

This repository contains video_recorder.py library for Robot Framework. It can capture desktop to video file while Robot executes. tasks.robot is a simple example that shows how video can be captured and stored to Robocorp Cloud if Robot run fails.

Recording should work in Windows, Linux and MacOS. Recording does not work in Robocorp Cloud standard container as those run in headless mode without desktop. If you want to record video in container, you must use container that has xvfb.

## Installation

Copy video_recorder.py to Robot directory and import it in .robot file

```
*** Settings ***
Library  video_recording.py
```

Add python-mss, numpy, opencv and pynput -libraries to conda.yaml e.g.
```
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.7.5
  - pip=20.1
  - python-mss
  - numpy
  - opencv
  - pynput
  - pip:
    - rpaframework==7.0.5
```

## Usage

### Start recording:

    Start Recording
      filename=recording.avi
      max_length=60.0
      monitor=1
      scale=1.0
      fps=5
      force_fps=False
      fourcc=VP80

    Example: Start Recording  filename=output/video.webm

#### Arguments

 - ``filename`` specifies the name by which the record will be saved. Use e.g. ``filename=output/video.webml``  to upload record to the Robocorp Cloud. Extension specifies the container type and it must be compatible with the ``fourcc`` argument below.
 - ``max_length`` maximum length of the record in seconds. Recording will stop automatically when limit is reached.
 - ``monitor`` selects which monitor you want to capture. Use value 0 to capture all.
 - ``scale`` is used to change the size of the screen recordings. It specifies how much this reduction is with respect to screen resolution. By default this parameter is set to native screen resolution.
 - ``fps`` specifies the frame rate at which the video is displayed.
 - ``force_fps`` if set to true, recorder will add duplicate frames if capture can't keep up. This shuold keep the recording close to real time. If set to false, recorder will never write consecutive duplicate frames. This may speed up the play, but save disc space.
 - ``fourcc`` name of the video codec - do not change unless you know what you are doing ;-)

### Stop or cancel recording:

    Stop Recording
    Cancel Recording

See tasks.robot for full example.
