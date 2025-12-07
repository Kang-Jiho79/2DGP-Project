from pico2d import *

import game_framework
import game_world
from sound_manager import SoundManager
from state_machine import StateMachine
from attack import Attack
from damage_text import DamageText

player_idle_animation = (
    ((0, 80, 15, 21), (17, 80, 15, 21), (34, 80, 15, 20), (51, 80, 15, 21), (68, 80, 15, 21), (85, 80, 15, 21)),
    ((0, 54, 15, 20), (17, 54, 15, 20), (33, 54, 15, 20), (49, 54, 15, 20)),
    ((0, 27, 15, 21), (17, 27, 15, 21), (34, 27, 15, 21), (51, 27, 15, 21), (68, 27, 15, 21), (85, 27, 15, 21)),
    ((0, 54, 15, 20), (17, 54, 15, 20), (33, 54, 15, 20), (49, 54, 15, 20))
)
player_death_animation = (
    (0, 31, 17, 21), (19, 31, 18, 21), (39, 31, 16, 21), (57, 31, 16, 21),
    (75, 31, 16, 21), (93, 31, 16, 21), (108, 31, 16, 21), (123, 31, 16, 21),
    (138, 31, 16, 21)
)
player_hit_animation = (
    ((0,60,17,16),(19,60,15,20),(36,60,17,20),(55,60,17,19),(74,60,17,19),(93,60,17,19)),
    ((0,27,13,20),(15,27,13,18),(30,27,16,21),(48,27,16,21),(66,27,16,21)),
    ((0,0,15,21),(17,0,15,19),(34,0,15,17),(51,0,19,25),(72,0,19,25),(93,0,19,21),(114,0,17,18)),
    ((0,27,13,21),(15,27,13,18),(30,27,16,21),(48,27,16,21),(66,27,16,21))
)
player_parring_animation = (
    (0,52,54,102), (54,52,54,102), (108,52,54,102), (162,52,54,102), (216,52,54,102),
    (0,0,54,102), (54,0,54,102), (108,0,54,102), (162,0,54,102)
)
player_roll_animation = (
    ((0, 86, 15, 21), (14, 86, 15, 21), (29, 86, 15, 21), (44, 86, 15, 21), (59, 86, 15, 21), (74, 86, 15, 21), (90, 86, 15, 21), (108, 86, 15, 21), (123, 86, 15, 21)),
    ((0, 57, 20, 24), (20, 57, 22, 24), (43, 57, 20, 24), (67, 57, 18, 24), (87, 57, 18, 24), (105, 57, 16, 24), (121, 57, 16, 24), (138, 57, 16, 24), (155, 57, 18, 24)),
    ((0, 27, 15, 21), (14, 27, 15, 21), (29, 27, 15, 21), (44, 27, 15, 21), (59, 27, 15, 21), (74, 27, 15, 21), (90, 27, 14, 21), (103, 27, 14, 21), (118, 27, 14, 21)),
    ((0, 57, 20, 24), (20, 57, 22, 24), (43, 57, 20, 24), (67, 57, 18, 24), (87, 57, 18, 24), (105, 57, 16, 24), (121, 57, 16, 24), (138, 57, 16, 24), (155, 57, 18, 24))
)
player_walk_animation = (
    ((0, 87, 15, 25), (17, 87, 15, 25), (35, 87, 15, 25), (56, 87, 15, 25), (74, 87, 15, 25), (95, 87, 15, 25)),
    ((0, 58, 15, 25), (14, 58, 15, 25), (31, 58, 15, 25), (49, 58, 15, 25), (63, 58, 15, 25), (79, 58, 15, 25)),
    ((0, 30, 17, 25), (17, 30, 17, 25), (35, 30, 17, 25), (51, 30, 17, 25), (71, 30, 17, 25), (87, 30, 17, 25)),
    ((0, 58, 15, 25), (14, 58, 15, 25), (31, 58, 15, 25), (49, 58, 15, 25), (63, 58, 15, 25), (79, 58, 15, 25))
)

def up_key_down(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_UP
def up_key_up(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_UP
def down_key_down(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_DOWN
def down_key_up(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_DOWN
def left_key_down(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_LEFT
def left_key_up(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_LEFT
def right_key_down(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_RIGHT
def right_key_up(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_RIGHT
def space_key_down_with_stamina(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_SPACE and player.stamina > 0
def s_key_down_with_stamina(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_s and player.stamina > 0
def a_key_down_with_stamina(state_event, player):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_a and player.stamina > 0

def Toidle_event(state_event, player):
    return state_event[0] == "TOIDLE"
def Towalk_event(state_event, player ):
    return state_event[0] == "TOWALK"
def Todeath_event(state_event, player):
    return state_event[0] == "TODEATH"
def Tohit_event(state_event, player):
    return state_event[0] == "TOHIT"

PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
        self.player.current_state = 'IDLE'
        self.player.stamina_time = get_time()
        self.player.xdir = 0
        self.player.ydir = 0
        self.player.frame = 0

    def exit(self, event):
        if a_key_down_with_stamina(event, self.player):
            self.player.attack()

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(player_idle_animation[self.player.face_dir])
        # 처음 0.5초 대기 후 애니메이션 주기마다 회복
        if get_time() - self.player.stamina_time > 0.5:
            animation_duration = len(player_idle_animation[self.player.face_dir]) / (
                        FRAMES_PER_ACTION * ACTION_PER_TIME)
            elapsed_since_first_recovery = get_time() - self.player.stamina_time - 0.5

            if elapsed_since_first_recovery >= 0 and int(elapsed_since_first_recovery / animation_duration) > int(
                    (elapsed_since_first_recovery - game_framework.frame_time) / animation_duration):
                if self.player.stamina < self.player.max_stamina:
                    self.player.stamina += 1

    def draw(self):
        frame_data = player_idle_animation[self.player.face_dir][int(self.player.frame)]
        if self.player.face_dir == 3:  # left
            self.player.idle_image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], 0, 'h',
                                                       self.player.x, self.player.y, frame_data[2] * 2 , frame_data[3] * 2)
        else:
            self.player.idle_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                         self.player.x, self.player.y, frame_data[2] * 2 , frame_data[3] * 2)

class Death:
    def __init__(self, player):
        self.player = player
    def enter(self, event):
        self.player.current_state = 'DEATH'
        self.player.frame = 0
        # 죽음 효과음 재생
        try:
            self.player.sound.play_sfx("death")
        except Exception:
            pass
    def exit(self, event):
        pass
    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.player.frame >= len(player_death_animation):
            game_world.remove_object(self.player)
    def draw(self):
        frame_data = player_death_animation[int(self.player.frame)]
        self.player.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                         self.player.x, self.player.y, frame_data[2] * 2 , frame_data[3] * 2)

class Hit:
    def __init__(self, player):
        self.player = player
    def enter(self, event):
        self.player.current_state = 'HIT'
        self.player.frame = 0
    def exit(self, event):
        pass
    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.player.frame >= len(player_hit_animation[self.player.face_dir]):
            if self.player.hp <= 0:
                self.player.state_machine.handle_state_event(("TODEATH", None))
            else:
                if not any(self.player.keys_pressed.values()):
                    self.player.state_machine.handle_state_event(("TOIDLE", None))
                else:
                    self.player.state_machine.handle_state_event(("TOWALK", None))
    def draw(self):
        frame_data = player_hit_animation[self.player.face_dir][int(self.player.frame)]
        if self.player.face_dir == 3:  # left
            self.player.hit_image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], 0,
                                                       'h',
                                                       self.player.x, self.player.y, frame_data[2] * 2,
                                                       frame_data[3] * 2)
        else:
            self.player.hit_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                             self.player.x, self.player.y, frame_data[2] * 2, frame_data[3] * 2)

class Parrying:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
        self.player.current_state = 'PARRING'
        self.player.stamina -= 2
        self.player.xdir = 0
        self.player.ydir = 0
        self.player.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * self.player.parring_speed)
        if self.player.frame >= len(player_parring_animation):
            if not any(self.player.keys_pressed.values()):
                self.player.state_machine.handle_state_event(("TOIDLE", None))
            else:
                self.player.state_machine.handle_state_event(("TOWALK", None))

    def draw(self):
        character_frame_data = player_idle_animation[self.player.face_dir][0]
        frame_data = player_parring_animation[int(self.player.frame)]
        if self.player.face_dir == 3:  # left
            self.player.idle_image.clip_composite_draw(character_frame_data[0], character_frame_data[1], character_frame_data[2], character_frame_data[3], 0,
                                                       'h',
                                                       self.player.x, self.player.y, character_frame_data[2] * 2,
                                                       character_frame_data[3] * 2)
        else:
            self.player.idle_image.clip_draw(character_frame_data[0], character_frame_data[1], character_frame_data[2], character_frame_data[3],
                                             self.player.x, self.player.y, character_frame_data[2] * 2, character_frame_data[3] * 2)
        self.player.parring_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],self.player.x, self.player.y, character_frame_data[2] * 3, character_frame_data[3] * 3)

class Roll:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
        self.player.current_state = 'ROLL'
        self.player.stamina -= 1
        if self.player.face_dir == 0:
            self.player.xdir = 0
            self.player.ydir = -1
        elif self.player.face_dir == 1:
            self.player.xdir = 1
            self.player.ydir = 0
        elif self.player.face_dir == 2:
            self.player.xdir = 0
            self.player.ydir = 1
        elif self.player.face_dir == 3:
            self.player.xdir = -1
            self.player.ydir = 0
        self.player.frame = 0
        # 롤 효과음 재생
        try:
            self.player.sound.play_sfx("roll",volume=0.3)
        except Exception:
            pass

    def exit(self, event):
        pass

    def do(self):
        speed = RUN_SPEED_PPS * 2 * game_framework.frame_time * self.player.speed_multiplier

        # 이동 후 위치 계산
        new_x = self.player.x + self.player.xdir * speed
        new_y = self.player.y + self.player.ydir * speed

        # 화면 경계 체크
        new_x = max(15, min(new_x, get_canvas_width() - 15))
        new_y = max(20, min(new_y, get_canvas_height() - 20))

        # 실제 이동
        self.player.x = new_x
        self.player.y = new_y

        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.player.frame >= len(player_roll_animation[self.player.face_dir]):
            if not any(self.player.keys_pressed.values()):
                self.player.state_machine.handle_state_event(("TOIDLE", None))
            else:
                self.player.state_machine.handle_state_event(("TOWALK", None))

    def draw(self):
        frame_data = player_roll_animation[self.player.face_dir][int(self.player.frame)]
        if self.player.face_dir == 3:  # left
            self.player.roll_image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], 0,
                                                       'h',
                                                       self.player.x, self.player.y, frame_data[2] * 2,
                                                       frame_data[3] * 2)
        else:
            self.player.roll_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                             self.player.x, self.player.y, frame_data[2] * 2, frame_data[3] * 2)

class Walk:
    def __init__(self, player):
        self.player = player
        self.last_step_time = 0
        self.step_interval = 0.6  # 0.6초마다 발걸음 소리

    def enter(self, event):
        self.player.current_state = 'WALK'
        self.player.stamina_time = get_time()
        self.player.frame = 0
        self.last_step_time = 0

    def exit(self, event):
        if a_key_down_with_stamina(event, self.player):
            self.player.attack()

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(
            player_walk_animation[self.player.face_dir])
        current_time = get_time()
        if current_time - self.last_step_time >= self.step_interval:
            try:
                self.player.sound.play_sfx("walk", volume=0.1)
                self.last_step_time = current_time
            except Exception:
                pass
        # 처음 1.0초 대기 후 애니메이션 주기마다 회복
        if get_time() - self.player.stamina_time > 1.0:
            animation_duration = len(player_walk_animation[self.player.face_dir]) / (
                        FRAMES_PER_ACTION * ACTION_PER_TIME)
            elapsed_since_first_recovery = get_time() - self.player.stamina_time - 1.0

            if elapsed_since_first_recovery >= 0 and int(elapsed_since_first_recovery / animation_duration) > int(
                    (elapsed_since_first_recovery - game_framework.frame_time) / animation_duration):
                if self.player.stamina < self.player.max_stamina:
                    self.player.stamina += 1

        speed = RUN_SPEED_PPS * game_framework.frame_time * self.player.speed_multiplier

        self.player.xdir = 0
        self.player.ydir = 0

        if self.player.keys_pressed[SDLK_RIGHT]:
            self.player.xdir += 1
            self.player.face_dir = 1
        if self.player.keys_pressed[SDLK_LEFT]:
            self.player.xdir -= 1
            self.player.face_dir = 3
        if self.player.keys_pressed[SDLK_UP]:
            self.player.ydir += 1
            self.player.face_dir = 2
        if self.player.keys_pressed[SDLK_DOWN]:
            self.player.ydir -= 1
            self.player.face_dir = 0

        # 이동 후 위치 계산
        new_x = self.player.x + self.player.xdir * speed
        new_y = self.player.y + self.player.ydir * speed

        # 화면 경계 체크
        new_x = max(15, min(new_x, get_canvas_width() - 15))
        new_y = max(20, min(new_y, get_canvas_height() - 20))

        # 실제 이동
        self.player.x = new_x
        self.player.y = new_y

        # 아무 키도 누르지 않으면 IDLE로 전환
        if not any(self.player.keys_pressed.values()):
            self.player.state_machine.handle_state_event(("TOIDLE", None))
    def draw(self):
        frame_data = player_walk_animation[self.player.face_dir][int(self.player.frame)]
        if self.player.face_dir == 3:  # left
            self.player.walk_image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], 0,
                                                       'h',
                                                       self.player.x, self.player.y, frame_data[2] * 2,
                                                       frame_data[3] * 2)
        else:
            self.player.walk_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                             self.player.x, self.player.y, frame_data[2] * 2, frame_data[3] * 2)


class Player:
    def __init__(self):
        self.hp = 10
        self.max_hp = 10
        self.stamina = 10
        self.max_stamina = 10
        self.damage = 5
        self.gold = 100
        self.sword_level = 1
        self.parring_speed = 1.0

        self.current_hp = 10  # 현재 표시되는 HP (애니메이션용)
        self.hp_animation_speed = 5.0  # HP 감소 속도
        self.hp_shake_time = 0  # HP바 흔들림 시간
        self.hp_shake_duration = 0.5  # 흔들림 지속시간
        self.hp_shake_intensity = 3  # 흔들림 강도

        self.current_stamina = 10.0  # 현재 표시되는 스테미나 (애니메이션용)
        self.stamina_animation_speed = 8.0  # 스테미나 변화 속도

        self.accessory_count = 0
        self.equipped_accessories = [None,None]
        self.cleared_dungeon = 0

        self.near_thing = False
        self.current_thing = None

        # 디버프 시스템 추가
        self.speed_debuff_active = False
        self.speed_debuff_end_time = 0
        self.speed_multiplier = 1.0  # 기본 속도 배율

        self.x, self.y = 640, 360
        self.frame = 0
        self.face_dir = 3   # down:0, right:1, up:2, left:3
        self.xdir = 0
        self.ydir = 0
        self.keys_pressed = {
            SDLK_UP: False,
            SDLK_DOWN: False,
            SDLK_LEFT: False,
            SDLK_RIGHT: False
        }
        self.attacking = False
        self.deflected_missile_info = None

        self.font = load_font('ENCR10B.TTF', 30)

        self.idle_image = load_image('resource/player/player_idle.png')
        self.death_image = load_image('resource/player/player_death.png')
        self.hit_image = load_image('resource/player/player_hit.png')
        self.parring_image = load_image('resource/player/player_parring.png')
        self.roll_image = load_image('resource/player/player_roll.png')
        self.walk_image = load_image('resource/player/player_walk.png')

        self.hp_image = load_image('resource/player/hp.png')
        self.stamina_image = load_image('resource/player/stamina.png')
        self.damage_image = load_image('resource/player/damage.png')
        self.coin_image = load_image('resource/player/coin.png')
        self.F_image = load_image('resource/player/F_key.png')

        self.sound = SoundManager()
        self.sound.load_sfx("resource/sound/player/player_walk.mp3", "walk")
        self.sound.load_sfx("resource/sound/player/player_hit.wav", "hit")
        self.sound.load_sfx("resource/sound/player/player_attack.mp3", "attack")
        self.sound.load_sfx("resource/sound/player/player_roll.wav", "roll")
        self.sound.load_sfx("resource/sound/player/player_parring.mp3", "parring")
        self.sound.load_sfx("resource/sound/player/player_death.wav", "death")

        self.current_state = 'IDLE'
        self.IDLE = Idle(self)
        self.DEATH = Death(self)
        self.HIT = Hit(self)
        self.PARRING = Parrying(self)
        self.ROLL = Roll(self)
        self.WALK = Walk(self)
        self.state_machine = StateMachine(
            self.IDLE,
        {
            self.IDLE: {up_key_down: self.WALK, down_key_down: self.WALK,
                        left_key_down: self.WALK, right_key_down: self.WALK,
                        space_key_down_with_stamina: self.ROLL, s_key_down_with_stamina: self.PARRING,
                        a_key_down_with_stamina: self.IDLE, Tohit_event: self.HIT},
            self.WALK: {Toidle_event: self.IDLE, space_key_down_with_stamina: self.ROLL,
                        s_key_down_with_stamina: self.PARRING, a_key_down_with_stamina: self.WALK,
                        Tohit_event: self.HIT},
            self.ROLL: {Toidle_event: self.IDLE, Towalk_event: self.WALK},
            self.PARRING: {Toidle_event: self.IDLE, Towalk_event: self.WALK},
            self.DEATH:{},
            self.HIT: {Toidle_event: self.IDLE, Towalk_event: self.WALK, Todeath_event: self.DEATH}
            }
        )

    def update(self):
        self.state_machine.update()

        self.update_debuffs()

        self.update_ui_animation()

        if self.deflected_missile_info:
            info = self.deflected_missile_info
            if info['type'] == 'missile':
                from Missile.missile import Missile
                missile = Missile(self, info['target'].x, info['target'].y, info['speed'], True, info['target'])
                missile.x, missile.y = info['pos']
                game_world.add_object(missile, 1)
                game_world.add_collision_pair('player_missile:mob', missile, None)
            elif info['type'] == 'guided_missile':
                from Missile.guided_missile import GuidedMissile
                guided_missile = GuidedMissile(self, info['speed'], info['tracking_strength'],
                                               info['lifetime'], True, info['target'])
                guided_missile.x, guided_missile.y = info['pos']
                game_world.add_object(guided_missile, 1)
                game_world.add_collision_pair('player_missile:mob', guided_missile, None)
            elif info['type'] == 'bouncing_missile':
                from Missile.bouncing_missile import BouncingMissile
                bouncing_missile = BouncingMissile(self,info['pos'][0], info['pos'][1],
                                                   info['velocity_x'], info['velocity_y'], True, info['target'])
                game_world.add_object(bouncing_missile, 1)
                game_world.add_collision_pair('player_missile:mob', bouncing_missile, None)
                game_world.add_collision_pair('object:wall', bouncing_missile, None)
            self.sound.play_sfx("parring", volume=0.5)
            self.deflected_missile_info = None

    def update_ui_animation(self):
        # HP 감소 애니메이션
        if self.current_hp > self.hp:
            self.current_hp -= self.hp_animation_speed * game_framework.frame_time
            if self.current_hp < self.hp:
                self.current_hp = self.hp

        # HP 증가 애니메이션 (회복 시)
        elif self.current_hp < self.hp:
            self.current_hp += self.hp_animation_speed * game_framework.frame_time
            if self.current_hp > self.hp:
                self.current_hp = self.hp

        # 스테미나 감소 애니메이션
        if self.current_stamina > self.stamina:
            self.current_stamina -= self.stamina_animation_speed * game_framework.frame_time
            if self.current_stamina < self.stamina:
                self.current_stamina = self.stamina

        # 스테미나 증가 애니메이션 (회복 시)
        elif self.current_stamina < self.stamina:
            self.current_stamina += self.stamina_animation_speed * game_framework.frame_time
            if self.current_stamina > self.stamina:
                self.current_stamina = self.stamina

        # HP바 흔들림 타이머 업데이트
        if self.hp_shake_time > 0:
            self.hp_shake_time -= game_framework.frame_time

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = True
            if event.key == SDLK_f and self.near_thing:
                self.keys_pressed = {
                    SDLK_UP: False,
                    SDLK_DOWN: False,
                    SDLK_LEFT: False,
                    SDLK_RIGHT: False
                }
                if self.current_thing.__class__.__name__ == 'ItemNPC':
                    from Npc import item_shop_mode
                    game_framework.push_mode(item_shop_mode)
                elif self.current_thing.__class__.__name__ == 'UpgradeNPC':
                    from Npc import upgrade_shop_mode
                    game_framework.push_mode(upgrade_shop_mode)
                elif self.current_thing.__class__.__name__ == 'DungeonGate':
                    if self.cleared_dungeon == 0:
                        import dungeon_1_mode
                        game_framework.change_mode(dungeon_1_mode)
                    elif self.cleared_dungeon == 1:
                        import dungeon_2_mode
                        game_framework.change_mode(dungeon_2_mode)
                    elif self.cleared_dungeon == 2:
                        import dungeon_3_mode
                        game_framework.change_mode(dungeon_3_mode)
                    elif self.cleared_dungeon == 3:
                        import dungeon_boss_mode
                        game_framework.change_mode(dungeon_boss_mode)
                elif self.current_thing.__class__.__name__ == 'VillageGate':
                    from Village import village_mode
                    game_framework.change_mode(village_mode)
            elif event.key == SDLK_q:
                # 모든 악세사리 해제
                self.hp = 5
                for i in range(2):
                    if self.equipped_accessories[i] is not None:
                        accessory = self.unequip_accessory(i)
                        if accessory:
                            print(f"{accessory.__class__.__name__} 해제됨")
                print("모든 악세사리가 해제되었습니다!")
        elif event.type == SDL_KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = False
        self.state_machine.handle_state_event(("INPUT", event), self)

    def draw(self):
        self.state_machine.draw()
        self.ui_draw()

    def ui_draw(self):
        import math

        # HP바 흔들림 계산
        shake_x = 0
        shake_y = 0
        if self.hp_shake_time > 0:
            shake_intensity = self.hp_shake_intensity * (self.hp_shake_time / self.hp_shake_duration)
            shake_x = math.sin(self.hp_shake_time * 30) * shake_intensity
            shake_y = math.cos(self.hp_shake_time * 25) * shake_intensity

        # HP
        self.hp_image.composite_draw(0, '', 30 + shake_x, get_canvas_height() - 30 + shake_y, 30, 30)

        # max hp bar (배경)
        draw_rectangle(45 + shake_x, get_canvas_height() - 45 + shake_y,
                       45 + self.max_hp * 20 + shake_x, get_canvas_height() - 15 + shake_y,
                       0, 0, 0, 255, 1)

        # current hp bar (애니메이션되는 HP)
        if self.current_hp > 0:
            draw_rectangle(45 + shake_x, get_canvas_height() - 45 + shake_y,
                           45 + self.current_hp * 20 + shake_x, get_canvas_height() - 15 + shake_y,
                           255, 0, 0, 255, 1)

        # Stamina
        self.stamina_image.composite_draw(0,'',30, get_canvas_height()-75, 30, 30)
        # max stamina bar
        draw_rectangle(45, get_canvas_height()-90, 45 + self.max_stamina * 20, get_canvas_height()-60,0, 0, 0, 255, 1)
        # stamina bar
        if self.current_stamina > 0:
            draw_rectangle(45, get_canvas_height() - 90, 45 + self.current_stamina * 20, get_canvas_height() - 60, 0, 255, 0, 255, 1)

        # Damage
        self.damage_image.composite_draw(0,'',30, get_canvas_height()-120, 30, 30)
        self.font.draw(45, get_canvas_height()-120, f'{self.damage}', (0, 0, 0))

        # Gold
        self.coin_image.composite_draw(0,'',30, get_canvas_height()-160, 30, 30)
        self.font.draw(45, get_canvas_height()-160, f'{self.gold}', (0, 0, 0))

        if self.near_thing:
            self.F_image.composite_draw(0,'', self.x, self.y + 40, 30, 30)

    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.stamina -= 1
            attack = Attack(self.x, self.y, self.face_dir, self)
            game_world.add_object(attack, 1)
            game_world.add_collision_pair('attack:mob', attack, None)
            self.sound.play_sfx("attack", volume=0.5)

    def end_attack(self):
        self.attacking = False

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 20

    def handle_collision(self, group, other):

        if group == 'player:mob_missile':
            if other.__class__.__name__ == 'Missile':
                if self.current_state == 'IDLE' or self.current_state == 'WALK':
                    damage = other.shooter.damage
                    self.take_damage(damage)
                elif self.current_state == 'PARRING':
                    # 즉시 생성하지 않고 정보만 저장
                    self.deflected_missile_info = {
                        'type': 'missile',
                        'pos': (other.x, other.y),
                        'target': other.original_mob,
                        'speed': other.speed
                    }
            if other.__class__.__name__ == 'GuidedMissile':
                if self.current_state == 'IDLE' or self.current_state == 'WALK':
                    damage = other.shooter.damage
                    self.take_damage(damage)
                elif self.current_state == 'PARRING':
                    # 즉시 생성하지 않고 정보만 저장
                    self.deflected_missile_info = {
                        'type': 'guided_missile',
                        'pos': (other.x, other.y),
                        'target': other.original_mob,
                        'speed': other.speed,
                        'tracking_strength': other.tracking_strength,
                        'lifetime': other.lifetime
                    }
            elif other.__class__.__name__ == 'BouncingMissile':
                if self.current_state == 'IDLE' or self.current_state == 'WALK':
                    damage = other.shooter.damage  # 바운싱 미사일 기본 데미지
                    self.take_damage(damage)
                elif self.current_state == 'PARRING':
                    # 바운싱 미사일도 패링 가능
                    self.deflected_missile_info = {
                        'type': 'bouncing_missile',
                        'pos': (other.x, other.y),
                        'velocity_x': -other.velocity_x,  # 반대 방향으로
                        'velocity_y': -other.velocity_y,
                        'target': other.original_mob
                    }

        if group == 'player:object':
            if self.current_thing != other:
                self.current_thing = other
                self.near_thing = True
                print(f"{other.__class__.__name__}와 가까이 있습니다!")

        if group == 'object:wall':
            # 벽과 충돌 시 이전 위치로 되돌리기
            player_left = self.x - 15
            player_right = self.x + 15
            player_bottom = self.y - 20
            player_top = self.y + 20

            wall_left = other.left
            wall_right = other.right
            wall_bottom = other.bottom
            wall_top = other.top

            # 겹침 정도 계산
            overlap_x = min(player_right - wall_left, wall_right - player_left)
            overlap_y = min(player_top - wall_bottom, wall_top - player_bottom)

            # 더 적게 겹친 축으로만 밀어내기
            if overlap_x < overlap_y:
                # x축으로 밀어내기
                if self.x < other.x:
                    self.x = wall_left - 15  # 왼쪽으로 밀어내기
                else:
                    self.x = wall_right + 15  # 오른쪽으로 밀어내기
            else:
                # y축으로 밀어내기
                if self.y < other.y:
                    self.y = wall_bottom - 20  # 아래로 밀어내기
                else:
                    self.y = wall_top + 20  # 위로 밀어내기

    def object_unhandle_collision(self, group, other):
        if self.current_thing != other:
            return
        else:
            self.current_thing = None
            self.near_thing = False
            print(f"{ other.__class__.__name__ }에서 멀어졌습니다!")

    def equip_accessory(self, accessory):
        # 빈 슬롯 찾기
        for i in range(2):
            if self.equipped_accessories[i] is None:
                self.equipped_accessories[i] = accessory
                accessory.equip(self)
                accessory.equipped = True
                self.accessory_count += 1
                return True
        return False  # 슬롯이 가득참

    def unequip_accessory(self, slot_index):
        if 0 <= slot_index < 2 and self.equipped_accessories[slot_index] is not None:
            accessory = self.equipped_accessories[slot_index]
            accessory.unequip(self)
            accessory.equipped = False
            self.equipped_accessories[slot_index] = None
            self.accessory_count -= 1
            return accessory
        return None

    def take_damage(self, damage):
        print("Dummy took", damage, "damage!")
        damage_text = DamageText(self.x, self.y, damage)
        game_world.add_object(damage_text, 1)
        self.hp -= damage
        self.hp_shake_time = self.hp_shake_duration
        self.state_machine.handle_state_event(('TOHIT', None))
        self.sound.play_sfx("hit", volume=0.5)

    def apply_slow_debuff(self, duration, slow_ratio):
        self.speed_debuff_active = True
        self.speed_debuff_end_time = get_time() + duration
        self.speed_multiplier = slow_ratio
        print(f"속도 디버프 적용! {duration}초간 {int((1-slow_ratio)*100)}% 속도 감소")

    def update_debuffs(self):
        """디버프 상태 업데이트"""
        if self.speed_debuff_active and get_time() > self.speed_debuff_end_time:
            self.speed_debuff_active = False
            self.speed_multiplier = 1.0
            print("속도 디버프 해제됨!")
