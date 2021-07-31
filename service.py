import cv2
import threading
from tkinter import *
from utils import segment
from pyvirtualcam import PixelFormat, Camera

# TODO: some video capture selection
# TODO: image path browser for replacement
# TODO: mode swapping (gaussian blur ?)
# TODO: make it's executionable in both windows and macOS (or just windows)

# Query final capture device values
# (may be different from preferred settings)
class Service():
    def __init__(self, stopEvent : threading.Event ):
        self.cap = cv2.VideoCapture(1)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.default_image_path = './test_img/someone.jpg'
        self.segment_utils = segment.SegmentUtils()
        self.stopEvent = stopEvent

    def run_service_loop(self):
        with Camera(self.width, self.height, self.fps, fmt=PixelFormat.BGR) as cam:
            print('Virtual camera device: ' + cam.device)
            self.segment_utils.set_default_img(self.default_image_path, (self.width, self.height))
            while not self.stopEvent.is_set():
                success, image = self.cap.read()
                image = cv2.flip(image, 1)
                output_image = self.segment_utils.process_img(image)
                # image = self.segment_utils.away_from_screen_correction(image)
                cam.send(output_image)
                cam.sleep_until_next_frame()
        self.cap.release()


