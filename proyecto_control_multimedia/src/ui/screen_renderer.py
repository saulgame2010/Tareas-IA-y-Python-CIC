import cv2

from src import config
from src.domain.virtual_button import VirtualButton


class ScreenRenderer:
    def draw_buttons(
        self,
        frame,
        buttons: list[VirtualButton],
        active_action: str | None = None
    ) -> None:
        for button in buttons:
            is_active = button.action == active_action

            color = config.COLOR_GREEN if is_active else config.COLOR_GRAY

            cv2.rectangle(
                frame,
                (button.x, button.y),
                (button.x2, button.y2),
                color,
                -1
            )

            cv2.rectangle(
                frame,
                (button.x, button.y),
                (button.x2, button.y2),
                config.COLOR_WHITE,
                2
            )

            cv2.putText(
                frame,
                button.label,
                (button.x + 25, button.y + 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                config.COLOR_WHITE,
                2
            )

    def draw_finger_position(
        self,
        frame,
        finger_position: tuple[int, int] | None
    ) -> None:
        if finger_position is None:
            return

        x, y = finger_position

        cv2.circle(
            frame,
            (x, y),
            10,
            config.COLOR_BLUE,
            -1
        )

    def draw_hand_landmarks(self, frame, hand_landmarks, frame_width: int, frame_height: int) -> None:
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

        points = []

        for landmark in hand_landmarks:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            points.append((x, y))

        for start, end in connections:
            cv2.line(
                frame,
                points[start],
                points[end],
                config.COLOR_WHITE,
                2
            )

        for point in points:
            cv2.circle(
                frame,
                point,
                4,
                config.COLOR_YELLOW,
                -1
            )

    def draw_status_text(self, frame, text: str) -> None:
        cv2.putText(
            frame,
            text,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            config.COLOR_GREEN,
            2
        )