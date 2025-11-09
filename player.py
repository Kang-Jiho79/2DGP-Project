from pico2d import *

import game_framework
import game_world
from state_machine import StateMachine
from attack import Attack

import item_shop_mode
import upgrade_shop_mode
from item_npc import ItemNPC
from upgrade_npc import UpgradeNPC

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
    ((0,53,17,21),(19,53,17,21),(36,53,17,21),(55,53,17,21),(74,53,17,21),(93,53,17,21)),
    ((0,27,13,21),(15,27,13,21),(30,27,16,21),(48,27,16,21),(66,27,16,21)),
    ((0,0,17,21),(17,0,17,21),(34,0,17,21),(51,0,17,21),(72,0,17,21),(93,0,17,21),(114,0,17,21)),
    ((0,27,13,21),(15,27,13,21),(30,27,16,21),(48,27,16,21),(66,27,16,21))
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
        if get_time() - self.player.stamina_time > 1.0:
            if self.player.stamina < self.player.max_stamina:
                self.player.stamina += 1
                self.player.stamina_time = get_time()

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


class Hit:
    def __init__(self, player):
        self.player = player


class Parrying:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
        self.player.current_state = 'PARRING'
        self.player.stamina -= 1
        self.player.xdir = 0
        self.player.ydir = 0
        self.player.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
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

    def exit(self, event):
        pass

    def do(self):
        speed = RUN_SPEED_PPS * 1.5 * game_framework.frame_time
        self.player.x += self.player.xdir * speed
        self.player.y += self.player.ydir * speed
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

    def enter(self, event):
        self.player.current_state = 'WALK'
        self.player.stamina_time = get_time()
        self.player.frame = 0

    def exit(self, event):
        if a_key_down_with_stamina(event, self.player):
            self.player.attack()

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(player_walk_animation[self.player.face_dir])
        if get_time() - self.player.stamina_time > 1.0:
            if self.player.stamina < self.player.max_stamina:
                self.player.stamina += 1
                self.player.stamina_time = get_time()

        speed = RUN_SPEED_PPS * game_framework.frame_time


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

        # 실제 이동
        self.player.x += self.player.xdir * speed
        self.player.y += self.player.ydir * speed

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
        self.hp = 5
        self.max_hp = 10
        self.stamina = 10
        self.max_stamina = 10
        self.damage = 5
        self.gold = 1000
        self.sword_level = 0

        self.accessory_count = 0
        self.equipped_accessories = [None,None]

        self.near_npc = False
        self.current_npc = None

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
                        a_key_down_with_stamina: self.IDLE},
            self.WALK: {Toidle_event: self.IDLE, space_key_down_with_stamina: self.ROLL,
                        s_key_down_with_stamina: self.PARRING, a_key_down_with_stamina: self.WALK},
            self.ROLL: {Toidle_event: self.IDLE, Towalk_event: self.WALK},
            self.PARRING: {Toidle_event: self.IDLE, Towalk_event: self.WALK},
            }
        )

    def update(self):
        self.state_machine.update()
        self.check_npc_proximity()

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = True
            if event.key == SDLK_f and self.near_npc:
                print(f"{self.current_npc} 모드로 이동합니다!")
                self.keys_pressed = {
                    SDLK_UP: False,
                    SDLK_DOWN: False,
                    SDLK_LEFT: False,
                    SDLK_RIGHT: False
                }
                if self.current_npc.__class__.__name__ == 'ItemNPC':
                    game_framework.push_mode(item_shop_mode)
                elif self.current_npc.__class__.__name__ == 'UpgradeNPC':
                    game_framework.push_mode(upgrade_shop_mode)
        elif event.type == SDL_KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = False
        self.state_machine.handle_state_event(("INPUT", event), self)

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 10, self.y + 50, f'X: {self.x:02f} Y: {self.y:02f}', (255, 255, 0))
        self.ui_draw()

    def ui_draw(self):
        # HP
        self.hp_image.composite_draw(0,'',30, get_canvas_height()-30, 30, 30)
        # max hp bar
        draw_rectangle(45, get_canvas_height()-45, 45 + self.max_hp * 20, get_canvas_height()-15,0, 0, 0, 255, 1)
        # hp bar
        draw_rectangle(45, get_canvas_height()-45, 45 + self.hp * 20, get_canvas_height()-15,255, 0, 0, 255, 1)

        # Stamina
        self.stamina_image.composite_draw(0,'',30, get_canvas_height()-75, 30, 30)
        # max stamina bar
        draw_rectangle(45, get_canvas_height()-90, 45 + self.max_stamina * 20, get_canvas_height()-60,0, 0, 0, 255, 1)
        # stamina bar
        draw_rectangle(45, get_canvas_height()-90, 45 + self.stamina * 20, get_canvas_height()-60,0, 255, 0, 255, 1)

        # Damage
        self.damage_image.composite_draw(0,'',30, get_canvas_height()-120, 30, 30)
        self.font.draw(45, get_canvas_height()-120, f'{self.damage}', (0, 0, 0))

        # Gold
        self.coin_image.composite_draw(0,'',30, get_canvas_height()-160, 30, 30)
        self.font.draw(45, get_canvas_height()-160, f'{self.gold}', (0, 0, 0))

    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.stamina -= 1
            attack = Attack(self.x, self.y, self.face_dir, self)
            game_world.add_object(attack, 1)

    def end_attack(self):
        self.attacking = False

    def get_bb(self):
        return self.x - 15, self.y - 20, self.x + 15, self.y + 20

    def handle_collision(self, group, other):
        pass

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

    def check_npc_proximity(self):
        """매 프레임마다 NPC와의 거리를 체크"""

        # 이전 상태 저장
        was_near = self.near_npc

        # 초기화
        self.near_npc = False
        self.current_npc = None

        # NPC가 있는 레이어에서 직접 확인
        npcs = game_world.world[1]  # 또는 NPC가 있는 적절한 레이어 인덱스
        for obj in npcs:
            if isinstance(obj, ItemNPC) or isinstance(obj, UpgradeNPC):
                distance = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5
                if distance < 50:
                    self.near_npc = True
                    self.current_npc = obj
                    break

        # 상태 변화 감지
        if not was_near and self.near_npc:
            print("NPC 근처에 왔습니다!")
        elif was_near and not self.near_npc:
            print("NPC에서 멀어졌습니다!")