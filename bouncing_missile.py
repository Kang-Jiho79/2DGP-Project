import math
from pico2d import *
import game_world
import game_framework

bouncing_missile_image = (
    (0, 0, 12, 23),  # down
    (14, 0, 16, 26),  # right down
    (32, 0, 17, 24),  # right
    (51, 0, 18, 28),  # right up
    (71, 0, 14, 27),  # up
    (51, 0, 18, 28),  # left up
    (32, 0, 17, 24),  # left
    (14, 0, 16, 26),  # left down
)


class BouncingMissile:
    mob_image = None
    player_image = None

    def __init__(self, shooter, x, y, velocity_x, velocity_y, playered=False, original_mob=None):
        if BouncingMissile.mob_image is None:
            BouncingMissile.mob_image = load_image('resource/missile/bouncing_missile.png')
        if BouncingMissile.player_image is None:
            BouncingMissile.player_image = load_image('resource/missile/player_bouncing_missile.png')

        self.shooter = shooter
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.playered = playered
        self.original_mob = original_mob if original_mob else shooter
        self.is_alive = True
        self.size_multiplier = 2.0  # 크기 배수

        # 초기 각도에 따른 프레임과 반전 설정
        angle = math.atan2(velocity_y, velocity_x)
        self.frame, self.flip_horizontal = self.get_frame_from_angle(angle)

    def get_frame_from_angle(self, angle_rad):
        """각도에 따른 프레임과 반전 여부 결정"""
        angle_deg = math.degrees(angle_rad) % 360

        if angle_deg < 22.5 or angle_deg >= 337.5:  # 오른쪽
            return 2, False
        elif angle_deg < 67.5:  # 오른쪽 위
            return 3, False
        elif angle_deg < 112.5:  # 위
            return 4, False
        elif angle_deg < 157.5:  # 왼쪽 위
            return 3, True
        elif angle_deg < 202.5:  # 왼쪽
            return 2, True
        elif angle_deg < 247.5:  # 왼쪽 아래
            return 1, True
        elif angle_deg < 292.5:  # 아래
            return 0, False
        else:  # 오른쪽 아래
            return 1, False

    def update(self):
        if not self.is_alive:
            return

        # 이동
        self.x += self.velocity_x * game_framework.frame_time
        self.y += self.velocity_y * game_framework.frame_time

        # 화면 밖으로 나가면 제거
        screen_width = get_canvas_width()
        screen_height = get_canvas_height()

        if self.x < -100 or self.x > screen_width + 100 or self.y < -100 or self.y > screen_height + 100:
            self._remove_missile()

    def draw(self):
        if not self.is_alive:
            return

        # playered에 따라 다른 이미지 사용
        current_image = self.player_image if self.playered else self.mob_image

        sx, sy, sw, sh = bouncing_missile_image[self.frame]
        # 크기를 키워서 그리기
        draw_width = int(sw * self.size_multiplier)
        draw_height = int(sh * self.size_multiplier)

        if self.flip_horizontal:
            # 좌우반전으로 그리기
            current_image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',  # 'h'는 수평 반전
                self.x, self.y, draw_width, draw_height
            )
        else:
            # 일반적으로 그리기
            current_image.clip_draw(
                sx, sy, sw, sh,
                self.x, self.y, draw_width, draw_height
            )

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_alive:
            return 0, 0, 0, 0
        # 크기에 맞춰 바운딩 박스 조정
        width = int(16 * self.size_multiplier)
        height = int(24 * self.size_multiplier)
        return self.x - width // 2, self.y - height // 2, self.x + width // 2, self.y + height // 2

    def handle_collision(self, group, other):
        if not self.is_alive:
            return
        if group == ('object:wall'):
            # 충돌한 벽의 위치에 따라 튕기는 방향 결정
            wall_left, wall_bottom, wall_right, wall_top = other.get_bb()
            missile_left, missile_bottom, missile_right, missile_top = self.get_bb()

            # 충돌 방향 판단
            overlap_left = missile_right - wall_left
            overlap_right = wall_right - missile_left
            overlap_top = wall_top - missile_bottom
            overlap_bottom = missile_top - wall_bottom

            # 가장 작은 겹침으로 충돌 방향 결정
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

            if min_overlap == overlap_left or min_overlap == overlap_right:
                # 좌우 충돌
                self.velocity_x = -self.velocity_x
            else:
                # 상하 충돌
                self.velocity_y = -self.velocity_y

            # 각도 재계산
            angle = math.atan2(self.velocity_y, self.velocity_x)
            self.frame, self.flip_horizontal = self.get_frame_from_angle(angle)

        if group == 'player:mob_missile':
            self._remove_missile()
        elif group == 'player_missile:mob':
            self._remove_missile()

    def _remove_missile(self):
        if self.is_alive:
            self.is_alive = False
            game_world.remove_object(self)

    def remove(self):
        self._remove_missile()