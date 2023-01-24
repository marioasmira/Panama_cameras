import picamera  # for camera
import time  # for sleep

cam_resolution = (1280, 720)  # camera resolution (needs to be a tuple)
cam_framerate = 30  # camera framerate

camera = picamera.PiCamera(
        resolution=cam_resolution,framerate=cam_framerate
    )  # initialize the camera class
time.sleep(2)  # wait 2 seconds for the camera to ajust to light conditions

camera.start_recording("test.h264", format="h264")  # starts the recording
camera.annotate_text = "test"
time.sleep(5)
camera.stop_recording()