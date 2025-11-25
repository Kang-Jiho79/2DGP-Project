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
        self.original_mob = original_mob if original_mob else shooter  # 최초 발사한 몬스터 저장

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
        # 경과 시간 업데이트
        self.elapsed_time += game_framework.frame_time

        # 생존 시간 초과시 제거
        if self.elapsed_time >= self.lifetime:
            game_world.remove_object(self)
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
            game_world.remove_object(self)

    def draw(self):
        if self.playered:
            self.player_image.draw(self.x, self.y, 32, 32)
        else:
            self.mob_image.draw(self.x, self.y, 32, 32)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'player:mob_guided_missile' or group == 'player_guided_missile:mob':
            # # 새로운 튕겨진 미사일 생성
            # from player import Player  # 플레이어 클래스 import
            # if isinstance(other, Player):
            #     new_missile = GuidedMissile(
            #         mob=other,  # 플레이어를 새 발사체로
            #         speed=self.speed,
            #         tracking_strength=self.tracking_strength,
            #         lifetime=self.lifetime,
            #         playered=True,
            #         original_mob=self.original_mob  # 원래 몬스터 정보 전달
            #     )
            #     new_missile.x = self.x
            #     new_missile.y = self.y
            #     game_world.add_object(new_missile, 2)  # 적절한 레이어에 추가

            game_world.remove_object(self)