import cv2
# unused import but will do it for gaussian blur and other choices
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation


class SegmentUtils():
    def __init__(self, threshold=0.7, bg_color=(100, 255, 100)) -> None:
        self.selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
            model_selection=0)
        self._MASK_COLOR = bg_color
        self._BG_IMAGE = None
        self._DEF_IMAGE = None
        self._DEF_COND = None

        # set mode
        self._MODE_DEF_IMG = False
        self._MODE_BG_IMG = False

        # set default threshold
        self._THRESHOLD = threshold

    def update_threshold(self, threshold:float):
        self._THRESHOLD = threshold

    def set_bg_color(self, bg_color: tuple):
        self._MASK_COLOR = bg_color

    def set_bg_image(self, path_to_image):
        self._BG_IMAGE = cv2.imread(path_to_image)

    def set_default_img(self, path_to_uploaded_img: str, frame_dim: tuple):
        image = cv2.imread(path_to_uploaded_img)
        image = cv2.resize(image, frame_dim, interpolation=cv2.INTER_AREA)
        results = self.selfie_segmentation.process(image)
        condition = np.stack((results.segmentation_mask,)
                             * 3, axis=-1) >= self._THRESHOLD

        self._DEF_COND = condition
        self._DEF_IMAGE = image

    def is_human_present(self, condition):
        return np.sum(np.invert(condition)) > 0

    def display_default_img(self, frame):
        output_image = np.where(self._DEF_COND, self._DEF_IMAGE, frame)
        return output_image

    def segment_human_out(self, image):
        results = self.selfie_segmentation.process(image)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) <= self._THRESHOLD
        # The background can be customized.
        #   a) Load an image (with the same width and height of the input image) to
        #      be the background, e.g., bg_image = cv2.imread('/path/to/image/file')
        #   b) Blur the input image by applying image filtering, e.g.,
        # bg_image = cv2.GaussianBlur(image,(55,55),0)

        if not self.is_human_present(condition):
            return self.display_default_img( image )

        masked_image = np.zeros(image.shape, dtype=np.uint8)
        masked_image[:] = self._MASK_COLOR
        output_image = np.where(condition, image, masked_image)

        return output_image

    def away_from_screen_correction(self, image):
        results = self.selfie_segmentation.process(image)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) <= self._THRESHOLD

        if not self.is_human_present(condition):
            return self.display_default_img(image)
        return image
