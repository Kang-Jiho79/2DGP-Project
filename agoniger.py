from pico2d import *
import game_framework
import game_world
from missile import Missile
from guided_missile import GuidedMissile
from state_machine import StateMachine
import time
from damage_text import DamageText

death_animation = (
(0,0,46,61), (51,0,46,60), (102,0,46,60)
)

attack_animation = (
(0,0,46,61), (51,0,46,61), (102,0,46,60), (153,0,46,60), (204,0,45,60), (254,0,44,60), (303,0,45,60), (353,0,44,60))

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
        # 자동 공격 동작 추가
        if time.time() - self.mob.attack_time > self.mob.attack_cooldown:  # 2초마다 공격
            self.mob.current_state = 'ATTACK'
            self.mob.state_machine.handle_state_event(('TOATTACK',None))

    def draw(self):
        self.mob.idle_image.clip_draw(0, 0, 48, 61, self.mob.x, self.mob.y, 80, 80)

class Attack:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
    def exit(self, event):
        pass
    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.mob.frame >= len(attack_animation):
            self.mob.current_state = 'IDLE'
            self.mob.state_machine.handle_state_event(('TOIDLE',None))
            self.mob.fire_missile()
    def draw(self):
        frame_data = attack_animation[int(self.mob.frame)]
        self.mob.attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 80, 80)

class Death:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
    def exit(self, event):
        pass
    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.mob.frame >= len(death_animation):
            game_world.remove_object(self.mob)
    def draw(self):
        frame_data = death_animation[int(self.mob.frame)]
        self.mob.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 80, 80)

class Hit:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
    def exit(self, event):
        pass
    def do(self):
        if self.mob.hp <= 0:
            self.mob.current_state = 'DEATH'
            self.mob.state_machine.handle_state_event(('TODEATH',None))
        else:
            self.mob.current_state = 'IDLE'
            self.mob.state_machine.handle_state_event(('TOIDLE',None))
    def draw(self):
        self.mob.hit_image.clip_draw(0,0,46,61, self.mob.x, self.mob.y, 80, 80)

class Agoniger:
    def __init__(self,x = 640, y = 360, level=1):
        self.hp = 30 * level
        self.damage = level
        self.attack_cooldown = 4.0 / level

        self.near_thing = False
        self.current_thing = None

        self.x, self.y = x, y
        self.frame = 0

        self.font = load_font('ENCR10B.TTF', 30)

        self.idle_image = load_image('resource/mob/agoniger/agoniger_idle.png')
        self.attack_image = load_image('resource/mob/agoniger/agoniger_attack.png')
        self.death_image = load_image('resource/mob/agoniger/agoniger_death.png')
        self.hit_image = load_image('resource/mob/agoniger/agoniger_hit.png')

        self.IDLE = Idle(self)
        self.ATTACK = Attack(self)
        self.DEATH = Death(self)
        self.HIT = Hit(self)
        self.state_machine = StateMachine(
            self.IDLE,
        {
            self.IDLE: {Toattack_event: self.ATTACK, Tohit_event: self.HIT},
            self.ATTACK: {Toidle_event: self.IDLE, Tohit_event: self.HIT},
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
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40

    def handle_collision(self, group, other):
        if group == 'attack:mob':
            damage = other.player.damage
            self.take_damage(damage)
        if group == 'player_missile:mob' or group == 'player_guided_missile:mob':
            damage = other.shooter.damage / 2
            self.take_damage(damage)

    def take_damage(self, damage):
        print("Dummy took", damage, "damage!")
        damage_text = DamageText(self.x, self.y, damage)
        game_world.add_object(damage_text, 1)
        self.hp -= damage
        self.state_machine.handle_state_event(('TOHIT', None))

    def fire_missile(self):
        for i in range(16):
            angle = (2 * math.pi * i) / 16
            target_x = self.x + math.cos(angle) * 500
            target_y = self.y + math.sin(angle) * 500

            missile = Missile(self, target_x, target_y)
            game_world.add_object(missile, 1)
            game_world.add_collision_pair("player:mob_missile", None, missile)