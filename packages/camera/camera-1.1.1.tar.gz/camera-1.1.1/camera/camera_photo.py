from picamera import PiCamera
from time import sleep

CAMERA = PiCamera()


def previewFor(rotation,secs):
    if rotation > 360:
        raise ValueError('rotation cannot be more than 360 degrees.')
    CAMERA.rotation = rotation
    CAMERA.start_preview()
    sleep(secs)
    CAMERA.stop_preview()



def takeVideoFor(file,rotation,secs):
    if rotation > 360:
        raise ValueError('rotation cannot be more than 360 degrees.')
    CAMERA.rotation = rotation
    CAMERA.start_recording(file)
    sleep(secs)
    CAMERA.stop_recording()
def takePhoto(file,rotation):
    if rotation > 360:
        raise ValueError('rotation cannot be more than 360 degrees.')
    CAMERA.rotation = rotation
    CAMERA.capture(file)

def previewAndVideoFor(file,rotation,secs):
    if rotation > 360:
        raise ValueError('rotation cannot be more than 360 degrees.')
        CAMERA.rotation = rotation
    CAMERA.start_preview()
    CAMERA.start_recording(file)
    sleep(secs)
    CAMERA.stop_recording()
    CAMERA.stop_preview()
def video(file,rotation):
    if rotation > 360:
        raise ValueError('rotation cannot be more than 360 degrees.')
    CAMERA.rotation = rotation
    CAMERA.start_recording(file)
def noVideo():
    CAMERA.stop_recording()
def preview(rotation):
    if rotation > 360:
        raise ValueError('rotation cannot be more than 360 degrees.')
    CAMERA.rotation = rotation
    CAMERA.start_preview()
def noPreview():
    CAMERA.stop_preview()
def previewAndVideo(file,rotation):
    if rotation > 360:
        raise ValueError('rotation cannot be more than 360 degrees.')
    CAMERA.rotation = rotation
    CAMERA.start_preview()
    CAMERA.start_recording(file)
def noPreviewAndVideo():
    CAMERA.stop_recording()
    CAMERA.stop_preview()
