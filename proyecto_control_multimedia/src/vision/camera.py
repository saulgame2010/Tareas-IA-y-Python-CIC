import cv2

from src import config


class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(config.CAMERA_INDEX)

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    def is_opened(self) -> bool:
        return self.capture.isOpened()

    def read_frame(self):
        success, frame = self.capture.read()

        if not success:
            return None

        # Efecto espejo para que el movimiento sea más natural
        return cv2.flip(frame, 1)

    def release(self) -> None:
        self.capture.release()