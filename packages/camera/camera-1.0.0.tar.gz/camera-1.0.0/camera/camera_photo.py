from picamera import PiCamera
from time import sleep

CAMERA = PiCamera()


def preview_for(secs):
    CAMERA.start_preview()
    sleep(secs)
    CAMERA.stop_preview()

def upside_down():
    CAMERA.rotation = 180

def take_video_for(file,secs):
    CAMERA.start_recording(file)
    sleep(secs)
    CAMERA.stop_recording()
def take_photo(file):
    CAMERA.capture(file)
def right_way_up():
    CAMERA.rotation = 0
