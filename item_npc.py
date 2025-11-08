from pico2d import *

class ItemNPC:
    def __init__(self, x = 245, y = 180):
        self.image = load_image('resource/npc/item_npc.png')
        self.x = x
        self.y = y

    def draw(self):
        self.image.clip_composite_draw(0, 0, 64, 64, 0, '', self.x, self.y, 64, 64)

    def update(self):
        pass