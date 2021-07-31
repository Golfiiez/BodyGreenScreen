import cv2 
# unused import but will do it for gaussian blur and other choices
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation
class SegmentUtils():
    def __init__(self) -> None:
        self.selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
            model_selection=0)
        self._BG_COLOR = (100, 255, 100)
        self._BG_IMAGE = None

    def set_bg_color(self, bg_color:tuple):
        self._BG_COLOR = bg_color
    
    def set_bg_image(self, path_to_image):
        self._BG_IMAGE = cv2.imread(path_to_image)

    def segment_human_out(self, image, threshold = 0.7):
        results = self.selfie_segmentation.process(image)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) <= threshold
        # The background can be customized.
        #   a) Load an image (with the same width and height of the input image) to
        #      be the background, e.g., bg_image = cv2.imread('/path/to/image/file')
        #   b) Blur the input image by applying image filtering, e.g.,
        # bg_image = cv2.GaussianBlur(image,(55,55),0)
        if bg_image is None:
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
        output_image = np.where(condition, image, bg_image)

        return output_image
    