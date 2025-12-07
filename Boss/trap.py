import game_framework
import game_world
from pico2d import *

trap_animation = (
    (0, 4, 19, 9), (21, 4, 20, 8), (43, 17, 15, 13), (60, 17, 16, 14),
    (79, 19, 16, 14), (98, 20, 5, 17), (107, 23, 10, 15), (121, 24, 14, 8),
    (138, 17, 15, 10), (156, 2, 20, 13), (183, 3, 20, 11), (210, 4, 20, 11),
    (236, 4, 18, 12), (261, 4, 16, 9), (281, 3, 18, 9)
)


class Trap:
    image = None
    sound_loaded = False
    def __init__(self, x, y, boss):
        self.x = x
        self.y = y
        self.boss = boss
        self.frame = 0
        self.activated = False
        self.lifetime = 10.0  # 10초 후 자동 제거
        self.elapsed_time = 0

        if Trap.image is None:
            Trap.image = load_image('resource/Boss/boss_trap.png')

        from sound_manager import SoundManager
        if not Trap.sound_loaded:
            sound = SoundManager()
            try:
                sound.load_sfx("resource/sound/boss/boss_trap.wav", "trap")
                Trap.sound_loaded = True
            except Exception:
                pass

        # 사운드 재생만 수행
        self.sound = SoundManager()

    def update(self):
        dt = game_framework.frame_time

        if not self.activated:
            # 대기 상태 애니메이션 (처음 3프레임 반복)
            self.frame = (self.frame + 5 * dt) % 1
        else:
            # 활성화 애니메이션 (4번째 프레임부터)
            if self.frame < 1:
                self.frame = 1
            else:
                self.frame = min(self.frame + 10 * dt, len(trap_animation) - 1)
                # 애니메이션이 끝나면 제거
                if int(self.frame) >= len(trap_animation) - 1:
                    game_world.remove_object(self)
                    return

        # 시간 경과로 제거
        self.elapsed_time += dt
        if self.elapsed_time >= self.lifetime:
            game_world.remove_object(self)

    def draw(self):
        frame_data = trap_animation[int(self.frame)]
        self.image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                             self.x, self.y, frame_data[2] * 2, frame_data[3] * 2)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 15, self.x + 20, self.y + 15

    def handle_collision(self, group, other):
        if group == 'trap:player' and not self.activated:
            self.activated = True
            try:
                self.sound.play_sfx('trap', volume=0.3)
            except Exception:
                pass
            # 플레이어에게 데미지와 이동 불가 디버프 적용
            if hasattr(other, 'take_damage'):
                if other.current_state == 'IDLE' or other.current_state == 'WALK' or other.current_state == 'ATTACK':
                    other.take_damage(self.boss.damage) # 데미지

            if hasattr(other, 'apply_slow_debuff'):
                other.apply_slow_debuff(1.0, 1.0)  # 3초간 50% 속도 저하
