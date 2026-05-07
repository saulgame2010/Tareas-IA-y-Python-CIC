import time

import cv2

from src import config
from src.domain.gesture import GestureResult
from src.domain.virtual_button import VirtualButton
from src.services.media_controller import MediaController
from src.ui.screen_renderer import ScreenRenderer
from src.vision.camera import Camera
from src.vision.hand_detector import HandDetector


class GestureMediaApp:
    def __init__(self):
        self.camera = Camera()
        self.hand_detector = HandDetector()
        self.renderer = ScreenRenderer()
        self.media_controller = MediaController()

        self.buttons = self._create_virtual_buttons()

        self.last_action_time = 0.0

    def _create_virtual_buttons(self) -> list[VirtualButton]:
        buttons = []

        for button_config in config.BUTTONS_CONFIG:
            button = VirtualButton(
                label=button_config["label"],
                action=button_config["action"],
                x=button_config["x"],
                y=button_config["y"],
                width=config.BUTTON_WIDTH,
                height=config.BUTTON_HEIGHT,
            )

            buttons.append(button)

        return buttons

    def run(self) -> None:
        if not self.camera.is_opened():
            print("No se pudo abrir la cámara.")
            return

        print("Aplicación iniciada.")
        print("Presiona 'q' para salir.")

        while True:
            frame = self.camera.read_frame()

            if frame is None:
                print("No se pudo leer el frame de la cámara.")
                break

            detection_result = self.hand_detector.detect(frame)

            gesture_result = self._process_detection_result(
                detection_result=detection_result,
                frame=frame
            )

            self._execute_action_if_needed(gesture_result)

            self._render_frame(
                frame=frame,
                detection_result=detection_result,
                gesture_result=gesture_result
            )

            cv2.imshow(config.WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        self._close()

    def _process_detection_result(self, detection_result, frame) -> GestureResult:
        frame_height, frame_width, _ = frame.shape

        if not detection_result.hand_landmarks:
            return GestureResult(
                action=None,
                button_label=None,
                finger_position=None
            )

        hand_landmarks = detection_result.hand_landmarks[0]

        # Landmark 8 = punta del dedo índice
        index_finger_tip = hand_landmarks[8]

        finger_x = int(index_finger_tip.x * frame_width)
        finger_y = int(index_finger_tip.y * frame_height)

        finger_position = (finger_x, finger_y)

        for button in self.buttons:
            if button.contains_point(finger_x, finger_y):
                return GestureResult(
                    action=button.action,
                    button_label=button.label,
                    finger_position=finger_position
                )

        return GestureResult(
            action=None,
            button_label=None,
            finger_position=finger_position
        )

    def _execute_action_if_needed(self, gesture_result: GestureResult) -> None:
        action = gesture_result.action
    
        if action is None:
            return
    
        current_time = time.time()
        elapsed_time = current_time - self.last_action_time
    
        if elapsed_time < config.ACTION_COOLDOWN_SECONDS:
            return
    
        self.media_controller.execute(action)
    
        self.last_action_time = current_time
    
        print(f"Acción ejecutada: {gesture_result.button_label}")

    def _render_frame(self, frame, detection_result, gesture_result: GestureResult) -> None:
        self._draw_detected_hand(
            frame=frame,
            detection_result=detection_result
        )

        self.renderer.draw_buttons(
            frame=frame,
            buttons=self.buttons,
            active_action=gesture_result.action
        )

        self.renderer.draw_finger_position(
            frame=frame,
            finger_position=gesture_result.finger_position
        )

        self.renderer.draw_status_text(
            frame=frame,
            text=self._get_status_text(gesture_result)
        )

    def _draw_detected_hand(self, frame, detection_result) -> None:
        if not detection_result.hand_landmarks:
            return

        frame_height, frame_width, _ = frame.shape

        hand_landmarks = detection_result.hand_landmarks[0]

        self.renderer.draw_hand_landmarks(
            frame=frame,
            hand_landmarks=hand_landmarks,
            frame_width=frame_width,
            frame_height=frame_height
        )

    def _get_status_text(self, gesture_result: GestureResult) -> str:
        if gesture_result.has_action:
            return f"Accion detectada: {gesture_result.button_label}"

        if gesture_result.finger_position is not None:
            return "Mano detectada"

        return "Muestra tu mano frente a la camara"

    def _close(self) -> None:
        self.hand_detector.close()
        self.camera.release()
        cv2.destroyAllWindows()
        print("Aplicación finalizada.")