from dataclasses import dataclass
from typing import Optional


@dataclass
class GestureResult:
    action: Optional[str]
    button_label: Optional[str]
    finger_position: Optional[tuple[int, int]]

    @property
    def has_action(self) -> bool:
        return self.action is not None