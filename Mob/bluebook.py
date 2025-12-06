from pico2d import *
import game_framework
import game_world
from Missile.bouncing_missile import BouncingMissile
from state_machine import StateMachine
import time
from damage_text import DamageText

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

    def exit(self, event):
        pass

    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(idle_animation)

    def draw(self):
        frame_data = idle_animation[int(self.mob.frame)]
        self.mob.idle_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

class Attack:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
        self.attack_started = False
    def exit(self, event):
        self.mob.attack_time = time.time()
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
            self.mob.attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)
        else:
            frame_data = attack_end_animation[int(self.mob.frame)]
            self.mob.attack_end_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

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
            common.player.gold += 100
            game_world.remove_object(self.mob)
    def draw(self):
        frame_data = death_animation[int(self.mob.frame)]
        self.mob.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

class Hit:
    def __init__(self, mob):
        self.mob = mob
    def enter(self, event):
        self.mob.frame = 0
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

class BlueBook:
    def __init__(self,x = 640, y = 360, level=1):
        self.hp = 10 * level
        self.damage = level
        self.attack_cooldown = 3.0 / level

        self.near_thing = False
        self.current_thing = None

        self.x, self.y = x, y
        self.frame = 0

        self.attack_time = time.time()

        self.font = load_font('ENCR10B.TTF', 30)

        self.idle_image = load_image('resource/mob/bluebook/bluebook_idle.png')
        self.attack_image = load_image('resource/mob/bluebook/bluebook_attack.png')
        self.attack_end_image = load_image('resource/mob/bluebook/bluebook_attackend.png')
        self.death_image = load_image('resource/mob/bluebook/bluebook_death.png')
        self.hit_image = load_image('resource/mob/bluebook/bluebook_hit.png')

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
        if (isinstance(self.state_machine.cur_state, Idle) and
                time.time() - self.attack_time > self.attack_cooldown):
            self.state_machine.handle_state_event(('TOATTACK', None))

    def handle_events(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

        # HP바 그리기
        bar_width = 40
        bar_height = 4
        bar_x = self.x - bar_width // 2
        bar_y = self.y + 25

        max_hp = 10 * getattr(self, 'level', 1)
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
        print(f"Collision detected: {group}, HP: {self.hp}, State: {type(self.state_machine.cur_state).__name__}")
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

        # 플레이어 방향으로 초기 속도 계산
        dx = player_x - self.x
        dy = player_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            velocity_x = (dx / distance) * 200  # 속도 조정
            velocity_y = (dy / distance) * 200
        else:
            velocity_x = 200
            velocity_y = 0

        # 바운싱 미사일만 발사
        missile = BouncingMissile(
            self,
            self.x, self.y,
            velocity_x, velocity_y,
        )

        game_world.add_object(missile, 1)
        game_world.add_collision_pair("player:mob_missile", None, missile)
        game_world.add_collision_pair("object:wall", missile, None)