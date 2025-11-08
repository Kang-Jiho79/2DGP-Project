from pico2d import *

class Village:
    def __init__(self):
        self.image = load_image('resource/background/village/village.png')

    def draw(self):
        self.image.clip_composite_draw(0, 0, 1248, 832, 0, '', 400, 300, 800, 600)

    def update(self):
        pass