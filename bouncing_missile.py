import math
from pico2d import *
import game_world
import game_framework

bouncing_missile_image = (
    (0,0,12,23),    # down
    (14,0,16,26),    # right down
    (32,0,17,24),    # right
    (51,0,18,28),    # right up
    (71,0,14,27),    # up
    (51,0,18,28),    # left up
    (32,0,17,24),    # left
    (14,0,16,26),    # left down
)
class BouncingMissile:
    def __init__(self, x, y, velocity_x, velocity_y, image_file):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.image = load_image(image_file)

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
        # 이동
        self.x += self.velocity_x * game_framework.frame_time
        self.y += self.velocity_y * game_framework.frame_time

        # 벽에 충돌 검사 및 튕기기
        screen_width = get_canvas_width()
        screen_height = get_canvas_height()

        bounced = False

        # 좌우 벽 충돌
        if self.x <= 0 or self.x >= screen_width:
            self.velocity_x = -self.velocity_x
            self.x = max(0, min(self.x, screen_width))
            bounced = True

        # 상하 벽 충돌
        if self.y <= 0 or self.y >= screen_height:
            self.velocity_y = -self.velocity_y
            self.y = max(0, min(self.y, screen_height))
            bounced = True

        # 튕겼을 때 각도 재계산
        if bounced:
            angle = math.atan2(self.velocity_y, self.velocity_x)
            self.frame, self.flip_horizontal = self.get_frame_from_angle(angle)

    def draw(self):
        sx, sy, sw, sh = bouncing_missile_image[self.frame]

        if self.flip_horizontal:
            # 좌우반전으로 그리기
            self.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',  # 'h'는 수평 반전
                self.x, self.y, sw, sh
            )
        else:
            # 일반적으로 그리기
            self.image.clip_draw(
                sx, sy, sw, sh,
                self.x, self.y
            )

    def remove(self):
        game_world.remove_object(self)