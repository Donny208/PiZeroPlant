from picamera import PiCamera
from time import sleep

class Camera:
    def __init__(self):
        # self.x = 2592
        # self.y = 1944
        self.x = 2592-200
        self.y = 1944-200
        self.camera = PiCamera()
        self.camera.resolution = (self.x, self.y)
        self.camera.vflip = True

    def takePhoto(self, name):
        print("Taking Photo")
        self.camera.capture(name)
        print("Photo Saved as: "+name)