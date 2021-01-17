*** Settings ***
Library  video_recorder.py
Library  RPA.Browser.Selenium

*** Keyword ***
Stop Video Recording
    Run Keyword If Test Failed  Stop Recorder
    Run Keyword If Test Passed  Cancel Recorder 

*** Task ***
Video Recording Example
    [Setup]  Start Recorder  filename=output/video.avi
    Open Available Browser  https://robocorp.com/
    Sleep  1s
    Click Link    xpath=(//a)[5]
    Sleep  1s
    Click Link    //a[@href="/docs/automation-libraries/rpa-framework-overview"]
    Sleep  1s
    Close All Browsers
    Fail
    [Teardown]  Stop Video Recording


