from pico2d import *
import math
import game_framework
import game_world

PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Missile:
    def __init__(self, x, y, target_x, target_y, speed=300):
        self.image = load_image('resource/missile/missile.png')  # 미사일 이미지 경로
        self.x = x
        self.y = y
        self.speed = speed

        # 목표까지의 벡터 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)

        # 정규화된 방향 벡터
        if distance > 0:
            self.dir_x = dx / distance
            self.dir_y = dy / distance
        else:
            self.dir_x = 1
            self.dir_y = 0

        # 회전 각도 계산 (라디안)
        self.angle = math.atan2(dy, dx)

    def update(self):
        # 미사일 이동
        self.x += self.dir_x * self.speed * game_framework.frame_time * RUN_SPEED_PPS
        self.y += self.dir_y * self.speed * game_framework.frame_time * RUN_SPEED_PPS

        # 화면 밖으로 나가면 제거
        if self.x < -50 or self.x > 1330 or self.y < -50 or self.y > 770:
            game_world.remove_object(self)

    def draw(self):
        # 각도를 도(degree)로 변환하여 회전 그리기
        angle_deg = math.degrees(self.angle)
        self.image.composite_draw(angle_deg, '', self.x, self.y, 32, 16)

    def get_bb(self):
        # 충돌 박스
        return self.x - 16, self.y - 8, self.x + 16, self.y + 8