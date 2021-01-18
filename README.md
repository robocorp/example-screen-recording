# example-screen-recording

This repository contains video_recorder.py library for Robot Framework. It can capture desktop to video file while Robot executes. tasks.robot is a simple example that shows how video can be captured and stored to Robocorp Cloud if Robot run fails.

Recording should work in Windows, Linux and MacOS, but it is tested only on MacOS. Recording does not work in Robocorp Cloud's standard containers as those run in headless mode without desktop. If you want to record video from container run, you must use container that uses xvfb.