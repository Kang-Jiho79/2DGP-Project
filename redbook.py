from pico2d import *
import game_framework
import game_world
from missile import Missile
from state_machine import StateMachine
import time

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

def Toidle_event(state_event, mob):
    return state_event[0] == "TOIDLE"
def Todeath_event(state_event, mob):
    return state_event[0] == "TODEATH"
def Tohit_event(state_event, mob):
    return state_event[0] == "TOHIT"
def Toattack_event(state_event, mob):
    return state_event[0] == "TOATTACK"

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
    def enter(self, event):
        self.mob.frame = 0
        self.mob.attack_time = time.time()

    def exit(self, event):
        pass

    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(idle_animation)
        # 자동 공격 동작 추가
        if time.time() - self.mob.attack_time > self.mob.attack_cooldown:  # 2초마다 공격
            self.mob.current_state = 'ATTACK'
            self.mob.state_machine.handle_state_event(('TOATTACK',None))

    def draw(self):
        frame_data = idle_animation[int(self.mob.frame)]
        self.mob.idle_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 50, 50)

class Attack:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
        self.attack_started = False
    def exit(self, event):
        pass
    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.mob.frame >= len(attack_animation) and not self.attack_started:
            self.mob.frame = 0
            self.attack_started = True
            self.mob.fire_missile()
        elif self.mob.frame >= len(attack_end_animation) and self.attack_started:
            self.mob.current_state = 'IDLE'
            self.mob.state_machine.handle_state_event(('TOIDLE',None))
    def draw(self):
        if not self.attack_started:
            frame_data = attack_animation[int(self.mob.frame)]
            self.mob.attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 50, 50)
        else:
            frame_data = attack_end_animation[int(self.mob.frame)]
            self.mob.attack_end_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 50, 50)

class Death:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        pass
    def exit(self, event):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Hit:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        pass
    def exit(self, event):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class RedBook:
    def __init__(self,x = 640, y = 360, level=1):
        self.hp = 3 * level
        self.damage = level
        self.attack_cooldown = 3.0 / level

        self.near_thing = False
        self.current_thing = None

        self.x, self.y = x, y
        self.frame = 0

        self.font = load_font('ENCR10B.TTF', 30)

        self.idle_image = load_image('resource/mob/redbook/redbook_idle.png')
        self.attack_image = load_image('resource/mob/redbook/redbook_attack.png')
        self.attack_end_image = load_image('resource/mob/redbook/redbook_attackend.png')
        self.death_image = load_image('resource/mob/redbook/redbook_death.png')
        self.hit_image = load_image('resource/mob/redbook/redbook_hit.png')

        self.current_state = 'IDLE'
        self.IDLE = Idle(self)
        self.ATTACK = Attack(self)
        self.DEATH = Death(self)
        self.HIT = Hit(self)
        self.state_machine = StateMachine(
            self.IDLE,
        {
            self.IDLE: {Toattack_event: self.ATTACK},
            self.ATTACK: {Toidle_event: self.IDLE},
            self.DEATH: {},
            self.HIT: {Toidle_event: self.IDLE, Todeath_event: self.DEATH}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_events(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 20

    def handle_collision(self, group, other):
        pass

    def get_player_position(self):
        """게임월드에서 플레이어 찾기"""
        for layer in game_world.world:
            for obj in layer:
                if obj.__class__.__name__ == 'Player':
                    return obj.x, obj.y
        return self.x, self.y

    def fire_missile(self):
        player_x, player_y = self.get_player_position()
        missile = Missile(self.x, self.y, player_x, player_y)
        game_world.add_object(missile, 1)