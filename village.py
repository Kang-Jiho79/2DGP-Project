from pico2d import *

class Village:
    def __init__(self):
        self.image = load_image('resource/background/village/village.png')

    def draw(self):
        self.image.clip_composite_draw(0, 0, 1248, 832, 0, '', 640, 360, 1280, 720)

    def update(self):
        pass