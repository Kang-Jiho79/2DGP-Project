from pico2d import *
import game_framework
import game_world

class DamageText:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y + 30  # 더미 위쪽에 표시
        self.damage = damage
        self.font = load_font('ENCR10B.TTF', 20)
        self.timer = 1.0  # 1초간 표시
        self.alpha = 255

    def update(self):
        self.timer -= game_framework.frame_time
        self.y += 50 * game_framework.frame_time  # 위로 올라감
        self.alpha = int(255 * (self.timer / 1.0))  # 점점 투명해짐

        if self.timer <= 0:
            game_world.remove_object(self)
        return True

    def draw(self):
        self.font.draw(self.x, self.y + 10, str(self.damage), (255, 0, 0))