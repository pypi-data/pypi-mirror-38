from picamera import PiCamera
from time import sleep

CAMERA = PiCamera()


def previewFor(secs):
    CAMERA.start_preview()
    sleep(secs)
    CAMERA.stop_preview()

def upsideDown():
    CAMERA.rotation = 180

def takeVideoFor(file,secs):
    CAMERA.start_recording(file)
    sleep(secs)
    CAMERA.stop_recording()
def takePhoto(file):
    CAMERA.capture(file)
def rightWayUp():
    CAMERA.rotation = 0
def previewAndVideoFor(file,secs):
    CAMERA.start_preview()
    CAMERA.start_recording(file)
    sleep(secs)
    CAMERA.stop_recording()
    CAMERA.stop_preview()
def video(file):
    CAMERA.start_recording(file)
def noVideo():
    CAMERA.stop_recording()
def preview():
    CAMERA.start_preview()
def noPreview():
    CAMERA.stop_preview()
def previewAndVideo(file):
    CAMERA.start_preview()
    CAMERA.start_recording(file)
def noPreviewAndVideo():
    CAMERA.stop_recording()
    CAMERA.stop_preview()