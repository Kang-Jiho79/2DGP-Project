from pico2d import *

class Title:
    def __init__(self):
        self.image = load_image('resource/title/title.png')

    def draw(self):
        self.image.clip_composite_draw(0, 0, 2752, 1536, 0, '', 640, 360, 1280, 720)

    def update(self):
        pass