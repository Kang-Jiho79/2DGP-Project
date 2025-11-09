from pico2d import *

class UpgradeShop:
    def __init__(self, player):
        self.player = player
        self.image = load_image('resource/npc/upgrade_npc_ui.png')
        self.price = 100 + 50 * self.player.sword_level
        self.success_rate = 90 - 10 * self.player.sword_level
        self.upgrade_button = (550,280,640,450)
        self.font = load_font('ENCR10B.TTF', 20)

    def draw(self):
        self.image.clip_composite_draw(0, 0, 1472, 704, 0, '', 640, 360, 800, 600)
        left, bottom, right, top = self.upgrade_button
        draw_rectangle(left, bottom, right, top)
        self.font.draw(700, 400, f'Upgrade Sword : {self.player.sword_level + 1}', (0, 0, 0))
        self.font.draw(700, 350, f'Price: {self.price} Gold', (0, 0, 0))
        self.font.draw(700, 300, f'Success Rate: {self.success_rate} %', (0, 0, 0))

    def update(self):
        pass