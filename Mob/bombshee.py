import random

from pico2d import *
import game_framework
import game_world
from Missile.bombshee_misssile import BombsheeMissile
from state_machine import StateMachine
import time
from damage_text import DamageText

idle_animation = (
(0,0,18,29), (22,0,18,29), (44,0,18,29), (64,0,18,29)
)
death_animation = (
(0,0,18,27), (22,0,34,34)
)
hit_animation = (
(0,0,18,28),
)
attack_animation = (
(0,0,18,27), (22,0,18,23), (44,0,18,28)
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

TIME_PER_ACTION = 0.8
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
        self.mob.idle_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 40)

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
            self.mob.frame = 0
            self.attack_started = True
            self.mob.fire_missile()
            self.mob.current_state = 'IDLE'
            self.mob.state_machine.handle_state_event(('TOIDLE',None))
    def draw(self):
        frame_data = attack_animation[int(self.mob.frame)]
        self.mob.attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

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
            import common
            common.player.gold += 1000
            game_world.remove_object(self.mob)
    def draw(self):
        frame_data = death_animation[int(self.mob.frame)]
        self.mob.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

class Hit:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
        self.mob.sound.play_sfx("bulletman_hit", volume= 0.5)
    def exit(self, event):
        pass
    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.mob.frame >= len(hit_animation):
            if self.mob.hp <= 0:
                self.mob.current_state = 'DEATH'
                self.mob.state_machine.handle_state_event(('TODEATH',None))
            else:
                self.mob.current_state = 'IDLE'
                self.mob.state_machine.handle_state_event(('TOIDLE',None))
    def draw(self):
        frame_data = hit_animation[int(self.mob.frame)]
        self.mob.hit_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

class Bombshee:
    def __init__(self,x = 640, y = 360, level=1):
        self.hp = 10 * level
        self.max_hp = 10 * level
        self.damage = level
        self.attack_cooldown = 3.0 / level

        self.near_thing = False
        self.current_thing = None

        self.x, self.y = x, y
        self.frame = 0

        self.font = load_font('ENCR10B.TTF', 30)

        self.idle_image = load_image('resource/mob/bombshee/bombshee_idle.png')
        self.attack_image = load_image('resource/mob/bombshee/bombshee_attack.png')
        self.death_image = load_image('resource/mob/bombshee/bombshee_death.png')
        self.hit_image = load_image('resource/mob/bombshee/bombshee_hit.png')

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
        self.sound.load_sfx("resource/sound/mob/bulletman_hit.wav", "bulletman_hit")

    def update(self):
        self.state_machine.update()

    def handle_events(self, event):
        pass

    def draw(self):
        self.state_machine.draw()

        # HP바 그리기
        bar_width = 40
        bar_height = 4
        bar_x = self.x - bar_width // 2
        bar_y = self.y + 25

        # 저장된 max_hp 사용
        max_hp = getattr(self, 'max_hp', 10 * getattr(self, 'level', 1))
        hp_ratio = max(0, min(1, self.hp / max_hp))

        # 배경
        draw_rectangle(bar_x - 1, bar_y - 1, bar_x + bar_width + 1, bar_y + bar_height + 1)

        # HP바
        if hp_ratio > 0:
            hp_width = int(bar_width * hp_ratio)
            draw_rectangle(bar_x, bar_y, bar_x + hp_width, bar_y + bar_height,255, 0, 0, 255, 1)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'attack:mob':
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

    def get_player_position(self):
        """게임월드에서 플레이어 찾기"""
        for layer in game_world.world:
            for obj in layer:
                if obj.__class__.__name__ == 'Player':
                    return obj.x, obj.y
        return self.x, self.y

    def fire_missile(self):
        player_x, player_y = self.get_player_position()
        missile = BombsheeMissile(self, player_x, player_y)
        game_world.add_object(missile, 1)
        game_world.add_collision_pair("player:mob_missile", None, missile)
        game_world.add_collision_pair("object:wall", missile, None)