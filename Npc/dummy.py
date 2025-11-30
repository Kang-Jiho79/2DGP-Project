from pico2d import *
import game_framework
import game_world
from damage_text import DamageText

dummy_animation = (
    (0, 101, 78,86), (92,101,78,86), (182,101,78,86), (270,101,78,86), (358,101,78,86), (447,101,78,86),
    (0, 0,78,86), (88,0,78,86), (177,0,78,86), (265,0,78,86), (354,0,78,86), (443,0,78,86)
)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Dummy:
    def __init__(self, x = 640, y = 100):
        self.hp = 100
        self.x = x
        self.y = y
        self.image = load_image('resource/npc/dummy.png')
        self.frame = 0

    def draw(self):
        frame_data = dummy_animation[int(self.frame)]
        self.image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.frame >= len(dummy_animation):
            self.frame = 0

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'attack:mob':
            damage = other.player.damage
            self.take_damage(damage)

    def take_damage(self, damage):
        print("Dummy took", damage, "damage!")
        damage_text = DamageText(self.x, self.y, damage)
        game_world.add_object(damage_text, 1)
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 100