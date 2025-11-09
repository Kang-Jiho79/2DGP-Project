from pico2d import *

dummy_animation = (
    (0, 101, 78,86), (92,101,78,86), (182,101,78,86), (270,101,78,86), (358,101,78,86), (447,101,78,86),
    (0, 0,78,86), (88,0,78,86), (177,0,78,86), (265,0,78,86), (354,0,78,86), (443,0,78,86)
)

class Dummy:
    def __init__(self, x = 640, y = 100):
        self.x = x
        self.y = y
        self.image = load_image('resource/npc/dummy.png')
        self.frame = 0

    def draw(self):
        frame_data = dummy_animation[int(self.frame)]
        self.image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.x, self.y, 78, 86)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + 1) % len(dummy_animation)

    def get_bb(self):
        return 0, 0, 0, 0

    def handle_collision(self, other, group):
        pass