import math
from pico2d import *
import game_framework
import game_world


class CheeseMissile:
    def __init__(self, x, y, target, speed):
        self.x = x
        self.y = y
        self.target = target  # 보스
        self.speed = speed
        self.image = load_image('resource/boss/boss_cheese_missile.png')
        self.angle = 0  # 회전 각도

    def update(self):
        # 보스를 향해 이동
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance > 0:
            # 이동
            self.x += (dx / distance) * self.speed * game_framework.frame_time
            self.y += (dy / distance) * self.speed * game_framework.frame_time

            # 회전 각도 계산 (보스를 향하도록)
            self.angle = math.atan2(dy, dx)

    def draw(self):
        # 각도에 따라 회전해서 그리기
        self.image.composite_draw(self.angle, '', self.x, self.y, 20, 20)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'cheese_missile:boss':
            game_world.remove_object(self)
        if group == "player:mob_missile":
            if hasattr(other, 'take_damage'):
                if other.current_state == 'IDLE' or other.current_state == 'WALK' or other.current_state == 'ATTACK':
                    other.take_damage(self.target.damage)