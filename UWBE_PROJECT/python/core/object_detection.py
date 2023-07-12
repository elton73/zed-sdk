"""
Detect people and save their positioning data to a csv
"""
import sys
import ogl_viewer.viewer as gl
import pyzed.sl as sl
from UWBE_PROJECT.python.utils.csv_handler import CsvHandler
from UWBE_PROJECT.python.utils.conversions import calculate_magnitude
import time

if __name__ == "__main__":
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.coordinate_units = sl.UNIT.METER
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    # If applicable, use the SVO given as parameter
    # Otherwise use ZED live stream
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        print("Using SVO file: {0}".format(filepath))
        init_params.set_from_svo_file(filepath)


    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Enable object detection module
    obj_param = sl.ObjectDetectionParameters()
    # Defines if the object detection will track objects across images flow.
    obj_param.enable_tracking = True       # if True, enable positional tracking

    obj_param.detection_model = sl.OBJECT_DETECTION_MODEL.MULTI_CLASS_BOX_ACCURATE

    if obj_param.enable_tracking:
        zed.enable_positional_tracking()

    zed.enable_object_detection(obj_param)

    camera_info = zed.get_camera_information()
    timestamp = str(zed.get_timestamp(sl.TIME_REFERENCE.IMAGE).get_microseconds() / 1000000.0)
    # Create OpenGL viewer
    viewer = gl.GLViewer(timestamp)
    viewer.init(camera_info.camera_configuration.calibration_parameters.left_cam, obj_param.enable_tracking)

    # Configure object detection runtime parameters
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = 30
    obj_runtime_param.object_class_filter = [sl.OBJECT_CLASS.PERSON]    # Only detect Persons

    # Create ZED objects filled in the main loop
    objects = sl.Objects()
    image = sl.Mat()

    # Set runtime parameters
    runtime_parameters = sl.RuntimeParameters()

    # Setup tracking type: velocity or position
    viewer.tracking_type = "velocity"
    # Setup csv handler
    save_to_csv = True       # if True, save to CSV
    if save_to_csv:
        csv_handler = CsvHandler()
        csv_handler.setup_csv("Raw_Data")
        csv_handler.write_csv(["ID", "Velocities(x)", "Velocities(y)", "Velocities(z)", "Velocities(m)", "Distance(x)", "Distance(y)", "Distance(z)", "Distance(m)", "Action State", "Time"])


    frames = 0
    time_time = time.time()
    while viewer.is_available():
        # Grab an image, a RuntimeParameters object must be given to grab()
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.VIEW.LEFT)
            # Retrieve objects
            zed.retrieve_objects(objects, obj_runtime_param)
            # Update GL view
            timestamp = str(zed.get_timestamp(sl.TIME_REFERENCE.IMAGE).get_microseconds() / 1000000.0)
            viewer.update_view(image, objects)
            frames += 1
            if frames == 60:
                time_time = time.time()
                frames = 0
            # Update CSV file
            if save_to_csv and objects.is_new:
                for _obj in objects.object_list:
                    actual_position = [_obj.position[0], -float(_obj.position[2]), _obj.position[1]]
                    csv_handler.write_csv([_obj.id, _obj.velocity[0], _obj.velocity[1], _obj.velocity[2], calculate_magnitude(_obj.velocity), _obj.position[0], -float(_obj.position[2]), _obj.position[1], calculate_magnitude(actual_position), _obj.action_state, (objects.timestamp.get_microseconds())/1000000.0])

    viewer.exit()

    image.free(memory_type=sl.MEM.CPU)
    # Disable modules and close camera
    zed.disable_object_detection()
    zed.disable_positional_tracking()

    zed.close()

    #C:\Users\ML-2\Documents\GitHub\zed-sdk\UWBE_PROJECT\python\core\object_detection.py C:\Users\ML-2\Documents\GitHub\zed-sdk\UWBE_PROJECT\recordings\recording_1.svo