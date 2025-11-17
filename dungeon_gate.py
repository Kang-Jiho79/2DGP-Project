import game_framework
from pico2d import *


class DungeonGate:
    def __init__(self, x, y, current_level):
        self.x = x
        self.y = y
        self.current_level = current_level  # 현재 던전 레벨

    def update(self):
        pass

    def draw(self):
        draw_rectangle(self.x - 25, self.y - 25, self.x + 25, self.y + 25)