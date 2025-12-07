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
    sound_loaded = False
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
        self.original_mob = original_mob if original_mob else shooter
        self.is_alive = True  # 미사일 상태 추가

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
        from sound_manager import SoundManager
        if not Missile.sound_loaded:
            sound = SoundManager()
            try:
                sound.load_sfx('resource/sound/mob/missile.wav', 'missile')
                Missile.sound_loaded = True
            except Exception:
                pass

        # 사운드 재생만 수행
        self.sound = SoundManager()
        try:
            self.sound.play_sfx('missile', volume=0.3)
        except Exception:
            pass

    def update(self):
        if not self.is_alive:
            return

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
            self.player_image.composite_draw(self.angle, '', self.x, self.y, 32, 16)
        else:
            self.mob_image.composite_draw(self.angle, '', self.x, self.y, 32, 16)

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