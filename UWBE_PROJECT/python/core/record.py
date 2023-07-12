"""
Record
"""

import sys
import pyzed.sl as sl
import os
from signal import signal, SIGINT

cam = sl.Camera()

def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)

signal(SIGINT, handler)

def get_recording_output():
    path_string = r'C:\Users\ML-2\Documents\GitHub\zed-sdk\UWBE_PROJECT\recordings'
    if not os.path.exists(path_string):
        os.makedirs(path_string)
    dir = path_string
    counter = 1
    output = os.path.join(dir, f"recording_{counter}.svo")
    while os.path.exists(output):
        counter += 1
        output = os.path.join(dir, f"recording_{counter}.svo")
    return output

def main():
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.depth_mode = sl.DEPTH_MODE.NONE

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    path_output = get_recording_output()
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(err)
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()
    print("SVO is Recording, use Ctrl-C to stop.")
    frames_recorded = 0

    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS :
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")

if __name__ == "__main__":
    main()

# C:\Users\ML-2\Documents\GitHub\zed-sdk\UWBE_PROJECT\python\core\record.py