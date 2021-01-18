# example-screen-recording

This repository contains video_recorder.py library for Robot Framework. It can capture desktop to video file while Robot executes. tasks.robot is a simple example that shows how video can be captured and stored to Robocorp Cloud if Robot run fails.

Recording should work in Windows, Linux and MacOS. Recording does not work in Robocorp Cloud standard container as those run in headless mode without desktop. If you want to record video in container, you must use container that has xvfb.

## Installation

Copy video_recorder.py to Robot directory and import it in .robot file

```
*** Settings ***
Library  video_recording.py
```

Screen Recording requires python-mss, numpy and opencv libraries that must be added to conda.yaml:
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
  - pip:
    - rpaframework==7.0.5
```

## Usage

Start recording:

    Start Recording
      filename=recording.avi
      max_length=60.0
      monitor=1
      scale=1.0
      fps=5

Stop or cancel recording:

    Stop Recording
    Cancel Recording

See tasks.robot for full example.
