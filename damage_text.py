from pico2d import *
import game_framework
import game_world

class DamageText:
    font = None
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y + 30  # 더미 위쪽에 표시
        self.damage = damage
        if DamageText.font is None:
           DamageText.font = load_font('ENCR10B.TTF', 20)
        self.timer = 1.0  # 1초간 표시

    def update(self):
        self.timer -= game_framework.frame_time
        self.y += 50 * game_framework.frame_time  # 위로 올라감

        if self.timer <= 0:
            game_world.remove_object(self)

    def draw(self):
        DamageText.font.draw(self.x, self.y, str(self.damage), (255, 0, 0))