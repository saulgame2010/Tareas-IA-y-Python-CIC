from dataclasses import dataclass


@dataclass
class VirtualButton:
    label: str
    action: str
    x: int
    y: int
    width: int
    height: int

    @property
    def x2(self) -> int:
        return self.x + self.width

    @property
    def y2(self) -> int:
        return self.y + self.height

    def contains_point(self, point_x: int, point_y: int) -> bool:
        return self.x <= point_x <= self.x2 and self.y <= point_y <= self.y2