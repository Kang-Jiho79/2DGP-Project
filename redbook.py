from pico2d import *
import game_framework
import game_world
from state_machine import StateMachine

idle_animation = (
(0,0,13,14), (16,0,13,14), (32,0,13,14), (48,0,13,14)
)
death_animation = (
(0,0,13,14), (16,0,15,16)
)
hit_animation = (
(0,0,13,14), (16,0,13,14),(32,0,13,14)
)
attack_animation = (
(0,0,13,14), (16,0,13,14), (32,0,13,16), (48,0,13,18), (64,0,12,18), (79,0,12,14), (94,0,12,14),
(109,0,19,15), (131,0,19,14), (153,0,19,12), (175,0,19,12), (197,0,19,12), (219,0,19,12)
)
attack_end_animation = (
(0,0,17,18), (20,0,8,23), (31,0,9,23), (42,0,12,19), (58,0,7,19), (68,0,7,20), (78,0,12,18),
(93,0,13,18), (109,0,13,16)
)


PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    def __init__(self, mob):
        self.mob = mob
    def enter(self):
        pass
    def exit(self):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Attack:
    def __init__(self, mob):
        self.mob = mob
    def enter(self):
        pass
    def exit(self):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Death:
    def __init__(self, mob):
        self.mob = mob
    def enter(self):
        pass
    def exit(self):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Hit:
    def __init__(self, mob):
        self.mob = mob
    def enter(self):
        pass
    def exit(self):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class RedBook:
    def __init__(self):
        self.hp = 5
        self.max_hp = 10
        self.damage = 5

        self.near_thing = False
        self.current_thing = None

        self.x, self.y = 640, 360
        self.frame = 0
        self.face_dir = 3   # down:0, right:1, up:2, left:3
        self.xdir = 0
        self.ydir = 0

        self.font = load_font('ENCR10B.TTF', 30)

        self.idle_image = load_image('resource/mob/redbook/redbook_idle.png')
        self.attack_image = load_image('resource/mob/redbook/redbook_attack.png')
        self.attack_end_image = load_image('resource/mob/redbook/redbook_attackend.png')
        self.death_image = load_image('resource/mob/redbook/redbook_death.png')
        self.hit_image = load_image('resource/mob/redbook/redbook_hit.png')

        self.current_state = 'IDLE'
        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE,
        {
            self.IDLE: {},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_events(self, event):
        pass

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 20

    def handle_collision(self, group, other):
        pass