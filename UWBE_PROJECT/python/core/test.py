"""
Detect people and save their positioning data to a csv
"""
import threading
import pyzed.sl as sl
import pychromecast
import os
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
import time

def wlan_ip():
    import subprocess
    result = subprocess.run('ipconfig', stdout=subprocess.PIPE, text=True).stdout.lower()
    scan = 0
    for i in result.split('\n'):
        if 'wireless' in i: scan = 1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()

IPV4_ADDRESS = wlan_ip()
CAST_IP = os.getenv("CAST_IP")
CAST_UUID = os.getenv("CAST_UUID")


new_object = False
running = True

class StartThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # Create a Camera object
        global new_object
        zed = sl.Camera()

        # Create a InitParameters object and set configuration parameters
        init_params = sl.InitParameters()
        init_params.coordinate_units = sl.UNIT.METER
        init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

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

        # Configure object detection runtime parameters
        obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
        obj_runtime_param.detection_confidence_threshold = 30
        obj_runtime_param.object_class_filter = [sl.OBJECT_CLASS.PERSON]    # Only detect Persons

        # Create ZED objects filled in the main loop
        objects = sl.Objects()
        image = sl.Mat()

        # Set runtime parameters
        runtime_parameters = sl.RuntimeParameters()

        start_time = time.time()
        # run for 1000 seconds
        while time.time()-start_time < 1000:
            # Grab an image, a RuntimeParameters object must be given to grab()
            if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
                # Retrieve left image
                zed.retrieve_image(image, sl.VIEW.RIGHT)
                # Retrieve objects
                zed.retrieve_objects(objects, obj_runtime_param)

                if not new_object and objects.is_new and objects.object_list:
                    new_object = True
                elif not objects.object_list:
                    new_object = False


        # Disable modules and close camera
        zed.disable_object_detection()
        zed.disable_positional_tracking()
        zed.close()
        running = False

class AudioPlayer:
    def __init__(self):
        self.mc = None
        self.cast = None
        self.get_chromecast()

    def get_chromecast(self):
        # Try connecting to chromecast directly
        try:
            cast = pychromecast.Chromecast(CAST_IP)
            cast.wait()
            print(cast)
            self.cast = cast
            self.mc = self.cast.media_controller
            return
        except:
            print("Connection attempt failed. Retrying...", end="\n")

        # Scan network for all chromecasts and search for chromecast by uuid
        try:
            chromecasts, services = pychromecast.get_chromecasts()
            for chromecast in chromecasts:
                if str(chromecast.device.uuid) == CAST_UUID:
                    cast = chromecast
                    cast.wait()
                    print(f"Connection Successful: {cast}")
                    self.cast = cast
                    self.mc = self.cast.media_controller
                    return
        except Exception as e:
            print(e)
            print("Failed to get chromecast")
    def play_url(self, url):
        self.mc.play_media(url=url, content_type='audio/mp3')
        self.mc.block_until_active()
        self.mc.play()

class PlayAudio(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.audio_player = AudioPlayer()
        self.previous_zone = None
        self._wait_duration = 0.0
        self.previous_time = None


    def run(self):
        # every second, check the zone of the tag and broadcast the location if the tag has changed zones
        while running:
            time.sleep(1)
            if new_object:
                # Play mp3 from url
                url = f"http://{IPV4_ADDRESS}:5000/static/Hello.mp3"
                filename, headers = urlretrieve(url)
                audio = MP3(filename)
                self._wait_duration = audio.info.length
                self.audio_player.play_url(url)
                time.sleep(600)
