from pico2d import *
import game_framework
import game_world
from Missile.missile import Missile
from state_machine import StateMachine
import time
from damage_text import DamageText
import common

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

    def exit(self, event):
        pass

    def do(self):
       pass

    def draw(self):
        self.mob.idle_image.clip_draw(0, 0, 48, 61, self.mob.x, self.mob.y, 80, 80)

class Attack:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
    def exit(self, event):
        self.mob.attack_time = time.time()

    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.mob.frame >= len(attack_animation):
            self.mob.state_machine.handle_state_event(('TOIDLE', None))
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
            common.player.gold += 1000
            game_world.remove_object(self.mob)
    def draw(self):
        frame_data = death_animation[int(self.mob.frame)]
        self.mob.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 80, 80)

class Hit:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
        self.mob.sound.play_sfx("agoniger_hit", volume= 0.5)
    def exit(self, event):
        pass
    def do(self):
        if self.mob.hp <= 0:
            self.mob.state_machine.handle_state_event(('TODEATH',None))
        else:
            self.mob.state_machine.handle_state_event(('TOIDLE',None))
    def draw(self):
        self.mob.hit_image.clip_draw(0,0,46,61, self.mob.x, self.mob.y, 80, 80)

class Agoniger:
    def __init__(self,x = 640, y = 360, level=1):
        self.hp = 30 * level
        self.max_hp = 30 * level
        self.damage = level
        self.attack_cooldown = 4.0 / level

        self.near_thing = False
        self.current_thing = None

        self.x, self.y = x, y
        self.frame = 0

        self.attack_time = time.time()

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

        from sound_manager import SoundManager
        self.sound = SoundManager()
        self.sound.load_sfx("resource/sound/mob/agoniger_hit.wav", "agoniger_hit")

    def update(self):
        self.state_machine.update()
        if (isinstance(self.state_machine.cur_state, Idle) and
                time.time() - self.attack_time > self.attack_cooldown):
            self.state_machine.handle_state_event(('TOATTACK', None))
    def handle_events(self, event):
        pass

    def draw(self):
        self.state_machine.draw()

        # HP바 그리기
        bar_width = 50
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y + 45

        # 최대 HP 사용 (저장된 max_hp 또는 계산된 값)
        max_hp = getattr(self, 'max_hp', 30 * getattr(self, 'level', 1))
        hp_ratio = max(0, min(1, self.hp / max_hp))

        # 배경 (검은색 테두리)
        draw_rectangle(bar_x - 1, bar_y - 1, bar_x + bar_width + 1, bar_y + bar_height + 1)

        # HP바 (현재 HP에 따라)
        if hp_ratio > 0:
            hp_width = int(bar_width * hp_ratio)
            draw_rectangle(bar_x, bar_y, bar_x + hp_width, bar_y + bar_height,255, 0, 0, 255, 1)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40

    def handle_collision(self, group, other):
        if group == 'attack:mob':
            if other.player.parring_damage_boost:
                damage = other.player.damage * 2
                other.player.parring_damage_boost = False
            else:
                damage = other.player.damage
            self.take_damage(damage)
        if group == 'player_missile:mob':
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
            game_world.add_collision_pair("object:wall", missile, None)