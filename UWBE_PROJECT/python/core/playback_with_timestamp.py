"""
Record
"""
import ogl_viewer_v2.viewer as gl
import sys
import pyzed.sl as sl
import time

def main():
    cam = sl.Camera()

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.depth_mode = sl.DEPTH_MODE.NONE

    # If applicable, use the SVO given as parameter
    # Otherwise use ZED live stream
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        print("Using SVO file: {0}".format(filepath))
        init.set_from_svo_file(filepath)

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    camera_info = cam.get_camera_information()
    timestamp = str(cam.get_timestamp(sl.TIME_REFERENCE.IMAGE).get_microseconds() / 1000000.0)
    # Create OpenGL viewer
    viewer = gl.GLViewer(timestamp)
    viewer.init(camera_info.camera_configuration.calibration_parameters.right_cam, False)

    image = sl.Mat()

    # Set runtime parameters
    runtime_parameters = sl.RuntimeParameters()

    # set playback speed parameters
    fps = 30
    framedelay = 1.0/fps
    time_perf = time.perf_counter()

    while viewer.is_available():
        # Grab an image, a RuntimeParameters object must be given to grab()
        if cam.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve left image
            cam.retrieve_image(image, sl.VIEW.RIGHT)
            # Add time delay for playback speed
            timestamp = str(cam.get_timestamp(sl.TIME_REFERENCE.IMAGE).get_microseconds()/1000000.0)
            time_elapsed = time.perf_counter() - time_perf
            if time_elapsed < framedelay:
                time.sleep(framedelay-time_elapsed)
            # Update GL view
            viewer.update_view(image, timestamp)
            time_perf = time.perf_counter()

            #debug
            current_fps = 1/(time.perf_counter()-time_perf)
            print(current_fps)



if __name__ == "__main__":
    main()

#C:\Users\ML-2\Documents\GitHub\zed-sdk\UWBE_PROJECT\python\core\playback_with_timestamp.py C:\Users\ML-2\Documents\GitHub\UWBE\csv\200000652\experiments\moving_experiment\ILS\setup_2\zed_comparison\zed_video\recording_1.svo