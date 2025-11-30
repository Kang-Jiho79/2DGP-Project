from pico2d import *
import math
import game_framework
import game_world

PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class GuidedMissile:
    mob_image = None
    player_image = None

    def __init__(self, shooter, speed=1.0, tracking_strength=0.5, lifetime=5.0, playered=False, original_mob=None):
        if GuidedMissile.mob_image is None:
            GuidedMissile.mob_image = load_image('resource/missile/guided_missile.png')
        if GuidedMissile.player_image is None:
            GuidedMissile.player_image = load_image('resource/missile/player_guided_missile.png')
        self.shooter = shooter
        self.x = self.shooter.x if shooter else 0
        self.y = self.shooter.y if shooter else 0
        self.speed = speed
        self.tracking_strength = tracking_strength
        self.lifetime = lifetime
        self.elapsed_time = 0.0
        self.playered = playered
        self.original_mob = original_mob if original_mob else shooter
        self.is_alive = True  # 미사일 상태 추가

        # 초기 방향 (아래쪽으로)
        self.dir_x = 0
        self.dir_y = -1

    def get_target_position(self):
        """playered가 True면 original_mob, 아니면 플레이어 위치 반환"""
        if self.playered and self.original_mob:
            return self.original_mob.x, self.original_mob.y
        else:
            # 플레이어 위치 찾기
            for layer in game_world.world:
                for obj in layer:
                    if obj.__class__.__name__ == 'Player':
                        return obj.x, obj.y
            return self.x, self.y

    def update(self):
        if not self.is_alive:
            return

        # 경과 시간 업데이트
        self.elapsed_time += game_framework.frame_time

        # 생존 시간 초과시 제거
        if self.elapsed_time >= self.lifetime:
            self._remove_missile()
            return

        # 타겟 위치 얻기
        target_x, target_y = self.get_target_position()

        # 타겟 방향 계산
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            # 타겟 방향으로의 단위 벡터
            target_dir_x = dx / distance
            target_dir_y = dy / distance

            # 현재 방향을 타겟 방향으로 조금씩 변경 (유도)
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
            self._remove_missile()

    def draw(self):
        if not self.is_alive:
            return

        if self.playered:
            self.player_image.draw(self.x, self.y, 32, 32)
        else:
            self.mob_image.draw(self.x, self.y, 32, 32)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_alive:
            return 0, 0, 0, 0
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if not self.is_alive:
            return

        if group == 'player:mob_missile' or group == 'player_missile:mob':
            self._remove_missile()
        if group == 'object:wall':
            self._remove_missile()

    def _remove_missile(self):
        if self.is_alive:
            self.is_alive = False
            game_world.remove_object(self)