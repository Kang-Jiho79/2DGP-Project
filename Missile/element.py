element_animation = (
(0, 3, 40, 44), (41, 0, 48, 47), (90, 5, 37, 37), (128, 5, 37, 37), (166, 3, 40, 39), (205, 1, 40, 41)
)

import math
import random
from pico2d import *
import game_framework
import game_world


class Element:
    image = None
    sound_loaded = False
    def __init__(self, x, y, direction, boss):
        self.x = x
        self.y = y
        self.boss = boss
        self.direction = direction  # 0~7 (8방향)
        self.damaged = False

        # 방향별 벡터 계산 (반시계방향, 아래부터 시작)
        angle = self.direction * (math.pi / 4) + (math.pi / 2)  # 아래부터 시작
        self.velocity_x = math.cos(angle) * 100  # 속도
        self.velocity_y = -math.sin(angle) * 100

        # 이동 관련
        self.travel_distance = random.uniform(100, 300)  # 랜덤 이동 거리
        self.moved_distance = 0
        self.is_moving = True

        # 폭발 관련
        self.frame = 0
        self.explosion_timer = 0
        self.explosion_delay = random.uniform(1.0, 3.0)  # 랜덤 폭발 시간
        self.is_exploding = False

        if Element.image is None:
            Element.image = load_image('resource/boss/boss_element.png')

        from sound_manager import SoundManager
        if not Element.sound_loaded:
            sound = SoundManager()
            try:
                sound.load_sfx('resource/sound/boss/element_shot.wav', 'element_shot')
                sound.load_sfx('resource/sound/boss/element.wav', 'element')
                Element.sound_loaded = True
            except Exception:
                pass

        # 사운드 재생만 수행
        self.sound = SoundManager()
        try:
            self.sound.play_sfx('element_shot', volume=0.3)
        except Exception:
            pass

    def update(self):
        dt = game_framework.frame_time

        if self.is_moving:
            # 이동
            move_distance = ((self.velocity_x ** 2 + self.velocity_y ** 2) ** 0.5) * dt
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt
            self.moved_distance += move_distance

            # 설정된 거리만큼 이동했으면 정지
            if self.moved_distance >= self.travel_distance:
                self.is_moving = False
                self.explosion_timer = 0
        else:
            # 정지 상태에서 폭발 대기
            self.explosion_timer += dt
            if self.explosion_timer >= self.explosion_delay:
                self.sound.play_sfx('element', volume=0.1)
                self.is_exploding = True

        # 폭발 애니메이션
        if self.is_exploding:
            self.frame += 10 * dt  # 폭발 애니메이션 속도
            if self.frame >= 8:  # 폭발 완료
                game_world.remove_object(self)

    def draw(self):
        if self.is_exploding and self.frame >= 1:
            # 폭발 프레임 (1~5번 프레임 사용)
            frame_index = min(int(self.frame) - 1, 5)  # 1~5번을 0~4 인덱스로
            frame_data = element_animation[frame_index]
            self.image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                 self.x, self.y, frame_data[2], frame_data[3])
        else:
            # 대기 상태 (0번 프레임)
            frame_data = element_animation[0]
            self.image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                 self.x, self.y, frame_data[2], frame_data[3])
    def get_bb(self):
        if self.is_exploding and self.frame >= 1:
            # 폭발 중일 때만 더 큰 hitbox
            return self.x - 20, self.y - 20, self.x + 20, self.y + 20
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'player:mob_missile':
            if self.is_exploding and self.frame >= 1:
                # 폭발 중에만 데미지
                if hasattr(other, 'take_damage') and not self.damaged:
                    if other.current_state == 'IDLE' or other.current_state == 'WALK' or other.current_state == 'ATTACK':
                        self.damaged = True  # 한 번만 데미지 주도록 설정
                        other.take_damage(self.boss.damage * 2)

                return
        elif group == 'object:wall':
            if self.is_moving:
                # 벽에 부딪히면 즉시 폭발 시작
                self.is_moving = False
                self.is_exploding = True
                self.frame = 0