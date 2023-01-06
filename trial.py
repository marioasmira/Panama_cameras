# Script to control a Raspberry Pi camera
# to record a 30 min video of frog mating choice trials
# Author: Mário
# Date: 04/01/2023

# ---------------- Setup -------------------------------
import picamera  # for camera
import os  # for conversion at the end
import time  # for sleep
import sys, traceback
from datetime import datetime
import transfer

server_folder = "/home/panama1/external/Frog_videos/"
additional_folder = ""
target_folder = server_folder + additional_folder
cam_resolution = (1280, 720)  # camera resolution (needs to be a tuple)
cam_framerate = 30  # camera framerate
trial_duration = 30 # minutes
camera_seconds = trial_duration * 60 # convert trial_duration to seconds
acclimatization_duration = 15 # minutes
acclimatization_seconds = acclimatization_duration * 60 # convert to seconds
wait_inverval = 5 #minutes
wait_seconds = wait_inverval * 60 #convert to seconds

def main() -> None:
    # --------- Initialize Camera ------------------------
    # initiate file name and camera object
    name_input = input(
        "Trial ID (avoid using spaces): "
    )  # ask for video file name
    formated_frame_time = datetime.now().strftime("%Y%m%d_%H%M")
    name = name_input + "_" + formated_frame_time # add the date & time
    file = name + ".h264"  # append the video file format
    camera = picamera.PiCamera(
        resolution=cam_resolution,framerate=cam_framerate
    )  # initialize the camera class
    print("Initializing camera...")
    time.sleep(2)  # wait 2 seconds for the camera to ajust to light conditions
    camera.awb_mode = 'fluorescent'

    try:
        # -------------------Trial ----------------------
        # stops here and waits for the user to press Enter
        input("Press a key to start the trial...")
        print("Waiting 30 minutes for acclimatization.")
        for i in range(0, acclimatization_duration + 1, wait_inverval):
            print("Currently at minute", i, "of acclimatization.")
            if (i == acclimatization_duration):
                break
            time.sleep(wait_seconds)

        print("Starting recording into file " + file + ".")
        camera.start_recording(file, format="h264")  # starts the recording
        camera.annotate_text = name
        t = 0
        ten_percent = camera_seconds / 10
        while t < camera_seconds:
            minutes = t / 60
            percentage = t / camera_seconds * 100
            print(round(minutes, 1), "minutes have passed.", round(percentage), "% done.")
            t = t + ten_percent
            time.sleep(ten_percent)

        camera.stop_recording()
        print("Done recording")

        print("Starting transfer to server...")
        try:
            transfer.transfer_file(file, target_folder + file)
            print("Transfer done.")
        except (IOError, OSError) as error:
            print(error)
            print("There was an error during transfer. Check videos.")

        print("Finished trial", name_input)
        will_delete = input("Should the video file be deleted? Yes for deleting, anything else for keeping.\n")
        if(will_delete == "Yes"):
            os.remove(file)

    except KeyboardInterrupt:
        print("\nInterrupted... Exiting.")
    finally:
        camera.close()
        sys.exit(0)

if __name__ == "__main__":
    main()