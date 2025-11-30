from pico2d import *
import math
import game_world
import game_framework

bouncing_missile_image = (
    (0, 0, 12, 23),
    (14, 0, 16, 26),
    (32, 0, 17, 24),
    (51, 0, 18, 28),
    (71, 0, 14, 27),
    (51, 0, 18, 28),
    (32, 0, 17, 24),
    (14, 0, 16, 26),
)


class BouncingMissile:
    mob_image = None
    player_image = None
    BOUNCE_MARGIN = 1.0
    BOUNCE_COOLDOWN = 0.05  # 초

    def __init__(self, shooter, x, y, velocity_x, velocity_y, playered=False, original_mob=None, size_multiplier=1.6):
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
        self.size_multiplier = size_multiplier

        angle = math.atan2(velocity_y, velocity_x)
        self.frame, self.flip_horizontal = self.get_frame_from_angle(angle)

        self.collision_cooldown = 0.0
        self.bounce_count = 0  # 추가: 튕긴 횟수

    def get_frame_from_angle(self, angle_rad):
        angle_deg = math.degrees(angle_rad) % 360
        if angle_deg < 22.5 or angle_deg >= 337.5:
            return 2, False
        elif angle_deg < 67.5:
            return 3, False
        elif angle_deg < 112.5:
            return 4, False
        elif angle_deg < 157.5:
            return 3, True
        elif angle_deg < 202.5:
            return 2, True
        elif angle_deg < 247.5:
            return 1, True
        elif angle_deg < 292.5:
            return 0, False
        else:
            return 1, False

    def update(self):
        if not self.is_alive:
            return

        dt = game_framework.frame_time

        if self.collision_cooldown > 0.0:
            self.collision_cooldown = max(0.0, self.collision_cooldown - dt)

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        screen_width = get_canvas_width()
        screen_height = get_canvas_height()

        if self.x < -100 or self.x > screen_width + 100 or self.y < -100 or self.y > screen_height + 100:
            self._remove_missile()

    def draw(self):
        if not self.is_alive:
            return

        current_image = self.player_image if self.playered else self.mob_image

        sx, sy, sw, sh = bouncing_missile_image[self.frame]
        draw_width = int(sw * self.size_multiplier)
        draw_height = int(sh * self.size_multiplier)

        if self.flip_horizontal:
            current_image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.x, self.y, draw_width, draw_height
            )
        else:
            current_image.clip_draw(
                sx, sy, sw, sh,
                self.x, self.y, draw_width, draw_height
            )

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_alive:
            return 0, 0, 0, 0
        sx, sy, sw, sh = bouncing_missile_image[self.frame]
        width = int(sw * self.size_multiplier)
        height = int(sh * self.size_multiplier)
        half_w = width / 2.0
        half_h = height / 2.0
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        if not self.is_alive:
            return

        if self.collision_cooldown > 0.0:
            return

        if group == 'object:wall':
            wall_left, wall_bottom, wall_right, wall_top = other.get_bb()
            m_left, m_bottom, m_right, m_top = self.get_bb()

            x_overlap = min(m_right, wall_right) - max(m_left, wall_left)
            y_overlap = min(m_top, wall_top) - max(m_bottom, wall_bottom)

            if x_overlap <= 0 or y_overlap <= 0:
                return

            bounced = False

            if x_overlap < y_overlap:
                if m_right > wall_left and m_left < wall_left:
                    self.x -= (x_overlap + BouncingMissile.BOUNCE_MARGIN)
                    bounced = True
                elif m_left < wall_right and m_right > wall_right:
                    self.x += (x_overlap + BouncingMissile.BOUNCE_MARGIN)
                    bounced = True
                if bounced:
                    self.velocity_x = -self.velocity_x
            else:
                if m_top > wall_bottom and m_bottom < wall_bottom:
                    self.y -= (y_overlap + BouncingMissile.BOUNCE_MARGIN)
                    bounced = True
                elif m_bottom < wall_top and m_top > wall_top:
                    self.y += (y_overlap + BouncingMissile.BOUNCE_MARGIN)
                    bounced = True
                if bounced:
                    self.velocity_y = -self.velocity_y

            if not bounced:
                return

            # 튕긴 횟수 증가 및 2번 이상이면 제거
            self.bounce_count += 1
            if self.bounce_count >= 3:
                self._remove_missile()
                return

            angle = math.atan2(self.velocity_y, self.velocity_x)
            self.frame, self.flip_horizontal = self.get_frame_from_angle(angle)

            self.collision_cooldown = BouncingMissile.BOUNCE_COOLDOWN

        if group == 'player:mob_missile' or group == 'player_missile:mob':
            self._remove_missile()

    def _remove_missile(self):
        if self.is_alive:
            self.is_alive = False
            game_world.remove_object(self)

    def remove(self):
        self._remove_missile()