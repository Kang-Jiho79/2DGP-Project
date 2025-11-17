from pico2d import *
import math
import game_framework
import game_world

PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class GuidedMissile:
    def __init__(self, x, y, speed=1.0, tracking_strength=0.5, lifetime=5.0):
        self.image = load_image('resource/missile/guided_missile.png')
        self.x = x
        self.y = y
        self.speed = speed  # 속도를 줄임 (1.0 -> 0.3)
        self.tracking_strength = tracking_strength  # 유도 강도를 줄임 (1.0 -> 0.05)
        self.lifetime = lifetime  # 생존 시간 (초)
        self.elapsed_time = 0.0  # 경과 시간

        # 초기 방향 (아래쪽으로)
        self.dir_x = 0
        self.dir_y = -1

    def get_player_position(self):
        """게임월드에서 플레이어 찾기"""
        for layer in game_world.world:
            for obj in layer:
                if obj.__class__.__name__ == 'Player':
                    return obj.x, obj.y
        return self.x, self.y

    def update(self):
        # 경과 시간 업데이트
        self.elapsed_time += game_framework.frame_time

        # 생존 시간 초과시 제거
        if self.elapsed_time >= self.lifetime:
            game_world.remove_object(self)
            return
        # 플레이어 위치 얻기
        player_x, player_y = self.get_player_position()

        # 플레이어 방향 계산
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            # 플레이어 방향으로의 단위 벡터
            target_dir_x = dx / distance
            target_dir_y = dy / distance

            # 현재 방향을 플레이어 방향으로 조금씩 변경 (유도)
            self.dir_x += (target_dir_x - self.dir_x) * self.tracking_strength
            self.dir_y += (target_dir_y - self.dir_y) * self.tracking_strength

            # 방향 벡터 정규화
            current_length = math.sqrt(self.dir_x * self.dir_x + self.dir_y * self.dir_y)
            if current_length > 0:
                self.dir_x /= current_length
                self.dir_y /= current_length

        # 미사일 이동
        self.x += self.dir_x * self.speed * game_framework.frame_time * RUN_SPEED_PPS
        self.y += self.dir_y * self.speed * game_framework.frame_time * RUN_SPEED_PPS

        # 화면 밖으로 나가면 제거
        if self.x < -50 or self.x > 1330 or self.y < -50 or self.y > 770:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y, 32, 16)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16