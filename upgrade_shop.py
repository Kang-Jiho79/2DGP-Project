from pico2d import *
from village_mode import player

class UpgradeShop:
    def __init__(self):
        self.image = load_image('resource/npc/upgrade_npc_ui.png')
        self.price = 100 + 50 * player.sword_level
        self.success_rate = 90 - 10 * player.sword_level
        self.upgrade_button = (0,0,0,0)

    def draw(self):
        self.image.clip_composite_draw(0, 0, 1472, 704, 0, '', 640, 360, 800, 600)
        left, bottom, right, top = self.upgrade_button
        draw_rectangle(left, bottom, right, top)

    def update(self):
        pass