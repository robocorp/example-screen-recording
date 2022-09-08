*** Settings ***
Library     video_recorder.py
Library     RPA.Browser.Selenium
Library     RPA.Desktop


*** Tasks ***
Video Recording Example
    [Setup]    Prepare and start the video
    Open Available Browser    https://robocorp.com/docs
    Sleep    2s
    Input Text    //input[@placeholder='Search']    SpaceX
    Sleep    2s
    Click Link    (//a[h3])[1]
    Sleep    3s
    Close All Browsers
    # [Teardown]    Store Video Only If Run Fails
    #RPA.Desktop.Press Keys    cmd    shift    m
    [Teardown]    Stop Recorder


*** Keywords ***
Store Video Only If Run Fails
    Run Keyword If Test Failed    Stop Recorder
    Run Keyword If Test Passed    Cancel Recorder

Prepare and start the video
    RPA.Desktop.Press Keys    cmd    m
    Start Recorder    filename=output/video.avi
