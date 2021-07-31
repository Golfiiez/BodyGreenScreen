import cv2
# unused import but will do it for gaussian blur and other choices
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation


class SegmentUtils():
    def __init__(self, width, height, threshold=0.7, bg_color=(100, 255, 100)) -> None:
        self.selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
            model_selection=0)
        self._MASK_COLOR = bg_color
        self._BG_IMAGE = None
        self._DEF_IMAGE = None
        self._DEF_COND = None
        self.width = width
        self.height = height

        # set mode
        self._MODE_DEF_IMG = False
        self._MODE_BG_IMG = False
        self._MODE = 'normal'

        # set default threshold
        self._THRESHOLD = threshold

    def set_mode(self, mode: str):
        self._MODE = mode

    def update_threshold(self, threshold: float):
        self._THRESHOLD = threshold

    def update_mode_selected(self, mode_str: str):
        self._MODE = mode_str

    def set_bg_color(self, bg_color: tuple):
        self._MASK_COLOR = bg_color

    def set_bg_image(self, path_to_image):
        image = cv2.imread(path_to_image)
        image = cv2.resize(image, (self.width, self.height),
                           interpolation=cv2.INTER_AREA)
        self._BG_IMAGE = image

    def set_default_img(self, path_to_uploaded_img: str):
        image = cv2.imread(path_to_uploaded_img)
        image = cv2.resize(image, (self.width, self.height),
                           interpolation=cv2.INTER_AREA)
        results = self.selfie_segmentation.process(image)
        condition = np.stack((results.segmentation_mask,)
                             * 3, axis=-1) >= self._THRESHOLD

        self._DEF_COND = condition
        self._DEF_IMAGE = image

    def is_human_present(self, condition):
        return np.sum(np.invert(condition)) > 0

    def change_bg(self, image):
        results = self.selfie_segmentation.process(image)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) > self._THRESHOLD
        inv_condition = np.invert(condition)
        masked_image = np.zeros(image.shape, dtype=np.uint8)
        masked_image[:] = (0, 0, 0)
        bg_img = np.where(condition, self._BG_IMAGE, image)
        return bg_img

    def display_default_img(self, frame):
        output_image = np.where(self._DEF_COND, self._DEF_IMAGE, frame)
        return output_image

    def segment_human_out(self, image):
        results = self.selfie_segmentation.process(image)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) <= self._THRESHOLD

        masked_image = np.zeros(image.shape, dtype=np.uint8)
        masked_image[:] = self._MASK_COLOR
        output_image = np.where(condition, image, masked_image)
        return output_image

    def gaussian_blur(self, image, std: tuple = (99, 99)):
        results = self.selfie_segmentation.process(image)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) > self._THRESHOLD

        inv_condition = np.invert(condition)

        masked_image = np.zeros(image.shape, dtype=np.uint8)
        masked_image[:] = (0, 0, 0)

        subject_part = np.where(condition, image, masked_image)
        bg_part = np.where(inv_condition, image, masked_image)

        blur_subject_part = cv2.GaussianBlur(subject_part, std, 0)

        return np.add(blur_subject_part, bg_part).astype(np.uint8)

    def process_img(self, image):
        if self._MODE == 'normal':
            return self.segment_human_out(image)
        elif self._MODE == 'blur':
            return self.gaussian_blur(image)
        elif self._MODE == 'image':
            return self.change_bg(image)

    def away_from_screen_correction(self, image):
        results = self.selfie_segmentation.process(image)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) <= self._THRESHOLD

        if not self.is_human_present(condition):
            return self.display_default_img(image)
        return image
