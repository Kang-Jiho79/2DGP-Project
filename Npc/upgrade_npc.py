from pico2d import *
import game_framework

upgrade_npc_animation = (
    (0, 0, 19, 19), (21,0,19,18), (42,0,19,18), (63,0,19,18), (84,0,19,19)
)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class UpgradeNPC:
    def __init__(self, x = 920, y = 210):
        self.image = load_image('resource/npc/upgrade_npc.png')
        self.x = x
        self.y = y
        self.frame = 0

    def draw(self):
        frame_data = upgrade_npc_animation[int(self.frame)]
        self.image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.x, self.y, 30, 40)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.frame >= len(upgrade_npc_animation):
            self.frame = 0

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def handle_collision(self, other, group):
        pass