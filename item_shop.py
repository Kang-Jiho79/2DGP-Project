from pico2d import *

class ItemShop:
    def __init__(self):
        self.image = load_image('resource/npc/item_npc_ui.png')

    def draw(self):
        self.image.clip_composite_draw(0, 0, 1472, 704, 0, '', 400, 300, 800, 600)

    def update(self):
        pass