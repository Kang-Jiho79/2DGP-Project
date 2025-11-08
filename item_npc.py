from pico2d import *
import game_framework

itemnpc_animation = (
    (0, 0, 15, 20), (16,0,15,20), (32,0,15,20), (48,0,15,20),
)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class ItemNPC:
    def __init__(self, x = 245, y = 180):
        self.image = load_image('resource/npc/item_npc.png')
        self.x = x
        self.y = y
        self.frame = 0

    def draw(self):
        frame_data = itemnpc_animation[int(self.frame)]
        self.image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.x, self.y, 30, 40)

    def update(self):
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.frame >= len(itemnpc_animation):
            self.frame = 0