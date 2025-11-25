import game_framework
from pico2d import *


class VillageGate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        draw_rectangle(self.x - 25, self.y - 25, self.x + 25, self.y + 25)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        pass