"""
Record
"""
import ogl_viewer_v2.viewer as gl
import sys
import pyzed.sl as sl
import os
from signal import signal, SIGINT
from UWBE_PROJECT.python.utils.directory_gui import browse_directory

cam = sl.Camera()

def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)

signal(SIGINT, handler)

def get_recording_output():
    print("Choose where to save recording.")
    path_string = browse_directory()
    if path_string == "q":
        return "q"
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
    path_output = get_recording_output()
    if path_output == "q":
        return
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD1080
    init.depth_mode = sl.DEPTH_MODE.NONE

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(err)
        print(repr(status))
        exit(1)

    camera_info = cam.get_camera_information()
    timestamp = str(cam.get_timestamp(sl.TIME_REFERENCE.IMAGE).get_microseconds() / 1000000.0)
    # Create OpenGL viewer
    viewer = gl.GLViewer(timestamp)
    viewer.init(camera_info.camera_configuration.calibration_parameters.right_cam, False)

    # Create ZED objects filled in the main loop
    image = sl.Mat()

    # Set runtime parameters
    runtime_parameters = sl.RuntimeParameters()

    print("SVO is Recording.")

    while viewer.is_available():
        # Grab an image, a RuntimeParameters object must be given to grab()
        if cam.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve left image
            cam.retrieve_image(image, sl.VIEW.RIGHT)
            # Update GL view
            timestamp = str(cam.get_timestamp(sl.TIME_REFERENCE.IMAGE).get_microseconds()/1000000.0)
            viewer.update_view(image, timestamp)

if __name__ == "__main__":
    main()

# C:\Users\ML-2\Documents\GitHub\zed-sdk\UWBE_PROJECT\python\core\record.py