from pico2d import *
import math
import game_framework
import game_world

PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 40.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Missile:
    mob_image = None
    player_image = None
    def __init__(self, shooter, target_x, target_y, speed=1.0, playered=False, original_mob=None):
        if Missile.mob_image is None:
             Missile.mob_image = load_image('resource/missile/missile.png')
        if Missile.player_image is None:
             Missile.player_image = load_image('resource/missile/player_missile.png')
        self.shooter = shooter
        self.x = self.shooter.x if shooter else 0
        self.y = self.shooter.y if shooter else 0
        self.speed = speed
        self.playered = playered
        self.original_mob = original_mob if original_mob else shooter  # 최초 발사한 몬스터 저장

        # 목표까지의 벡터 계산
        dx = target_x - self.x
        dy = target_y - self.y
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
        if self.playered:
            self.player_image.composite_draw(self.angle, '', self.x, self.y, 32, 16)
        else:
            self.mob_image.composite_draw(self.angle, '', self.x, self.y, 32, 16)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # 충돌 박스
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'player:mob_missile' or group == 'player_missile:mob':
            # # 새로운 튕겨진 미사일 생성
            # from player import Player  # 플레이어 클래스 import
            # if isinstance(other, Player) and self.original_mob:
            #     # 원래 몬스터를 타겟으로 하는 새 미사일 생성
            #     new_missile = Missile(
            #         mob=other,  # 플레이어를 새 발사체로
            #         target_x=self.original_mob.x,
            #         target_y=self.original_mob.y,
            #         speed=self.speed,
            #         playered=True,
            #         original_mob=self.original_mob  # 원래 몬스터 정보 전달
            #     )
            #     new_missile.x = self.x
            #     new_missile.y = self.y
            #     game_world.add_object(new_missile, 2)  # 적절한 레이어에 추가

            game_world.remove_object(self)
