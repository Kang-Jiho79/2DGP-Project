from pico2d import *

class Village:
    def __init__(self):
        self.image = load_image('resource/background/village/village.png')

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass