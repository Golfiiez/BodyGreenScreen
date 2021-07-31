import cv2
from utils import segment
from pyvirtualcam import PixelFormat, Camera

# TODO: GUI
# TODO: some video capture selection 
# TODO: threshold value slider
# TODO: image path browser for replacement
# TODO: mode swapping (gaussian blur ?)
# TODO: make it's executionable in both windows and macOS (or just windows)

# Query final capture device values
# (may be different from preferred settings)
cap = cv2.VideoCapture(1)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
default_image_path = './temp/Screen Shot 2564-07-31 at 14.19.00.png'

segment_utils = segment.SegmentUtils()

with Camera(width, height, fps, fmt=PixelFormat.BGR) as cam:
    print('Virtual camera device: ' + cam.device)
    segment_utils.set_default_img(  default_image_path, ( width, height ) )
    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image, 1)
        output_image = segment_utils.segment_human_out( image )
        cam.send(output_image)
        cam.sleep_until_next_frame()
        
cap.release()
