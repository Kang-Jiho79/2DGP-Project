from pico2d import *
import math
import game_framework
import game_world

PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.3
FRAMES_PER_ACTION = 5

bombshee_missile_animation = (
    (0, 0, 23, 23), (27, 0, 33, 33), (64, 3, 30, 30), (98, 5, 28, 28), (130, 5, 28, 28)
)


class BombsheeMissile:
    image = None

    def __init__(self, shooter, target_x, target_y, speed=1.0):
        if BombsheeMissile.image is None:
            BombsheeMissile.image = load_image('resource/missile/bombshee_missile.png')

        self.shooter = shooter
        self.x = self.shooter.x if shooter else 0
        self.y = self.shooter.y if shooter else 0
        self.speed = speed
        self.is_alive = True
        self.exploding = False
        self.frame = 0
        self.animation_time = 0

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
        self.sound = SoundManager()
        self.sound.load_sfx('resource/sound/mob/bombshee_missile.wav', 'bombshee_missile')
        self.sound.play_sfx('bombshee_missile', volume=0.3)

    def update(self):
        if not self.is_alive:
            return

        if not self.exploding:
            # 이동 상태 - 첫 번째 프레임으로 이동
            self.x += self.dir_x * self.speed * game_framework.frame_time * RUN_SPEED_PPS
            self.y += self.dir_y * self.speed * game_framework.frame_time * RUN_SPEED_PPS

            # 화면 밖으로 나가면 제거
            if self.x < -50 or self.x > 1330 or self.y < -50 or self.y > 770:
                self._remove_missile()
        else:
            # 폭발 애니메이션 진행
            self.animation_time += game_framework.frame_time
            if self.animation_time > TIME_PER_ACTION / FRAMES_PER_ACTION:
                self.animation_time = 0
                self.frame += 1

                # 애니메이션이 끝나면 제거
                if self.frame >= len(bombshee_missile_animation):
                    self._remove_missile()

    def draw(self):
        if not self.is_alive:
            return

        if not self.exploding:
            # 이동 중일 때는 첫 번째 프레임
            frame_data = bombshee_missile_animation[0]
        else:
            # 폭발 중일 때는 현재 프레임
            frame_index = min(int(self.frame), len(bombshee_missile_animation) - 1)
            frame_data = bombshee_missile_animation[frame_index]

        sx, sy, sw, sh = frame_data

        if not self.exploding:
            self.image.clip_composite_draw(sx, sy, sw, sh, self.angle, '',
                                           self.x, self.y, sw, sh)
        else:
            self.image.clip_draw(sx, sy, sw, sh, self.x, self.y)


    def get_bb(self):
        if not self.is_alive:
            return 0, 0, 0, 0

        if not self.exploding:
            return self.x - 12, self.y - 12, self.x + 12, self.y + 12
        else:
            # 폭발 중일 때는 더 큰 히트박스
            frame_index = min(int(self.frame), len(bombshee_missile_animation) - 1)
            frame_data = bombshee_missile_animation[frame_index]
            sw, sh = frame_data[2], frame_data[3]
            return self.x - sw // 2, self.y - sh // 2, self.x + sw // 2, self.y + sh // 2

    def handle_collision(self, group, other):
        if not self.is_alive:
            return

        if group == 'player:mob_missile' and not self.exploding:
            # 플레이어와 충돌하면 폭발 상태로 전환
            self.exploding = True
            self.frame = 1  # 두 번째 프레임부터 시작
            self.animation_time = 0

            # 플레이어에게 데미지와 디버프 적용
            if hasattr(other, 'take_damage'):
                if other.current_state == 'IDLE' or other.current_state == 'WALK' or other.current_state == 'ATTACK':
                    other.take_damage(self.shooter.damage)  # 데미지

            if hasattr(other, 'apply_slow_debuff'):
                other.apply_slow_debuff(3.0, 0.8)  # 3초간 50% 속도 저하

        elif group == 'object:wall':
            self._remove_missile()

    def _remove_missile(self):
        if self.is_alive:
            self.is_alive = False
            game_world.remove_object(self)