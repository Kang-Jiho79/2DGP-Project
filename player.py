from pico2d import *

from state_machine import StateMachine

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
player_slash_animation = (
    (0,0,42,33), (42,0,40,33), (82,0,40,33), (122,0,40,33)
)
def up_key_down(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_UP
def up_key_up(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_UP
def down_key_down(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_DOWN
def down_key_up(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_DOWN
def left_key_down(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_LEFT
def left_key_up(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_LEFT
def right_key_down(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_RIGHT
def right_key_up(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_RIGHT
def space_key_down(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_SPACE
def s_key_down(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_s



def Toidle_event(state_event):
    return state_event[0] == "TOIDLE"
def Towalk_event(state_event):
    return state_event[0] == "TOWALK"


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
        self.player.xdir = 0
        self.player.ydir = 0
        self.player.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % len(player_idle_animation[self.player.face_dir])

    def draw(self):
        frame_data = player_idle_animation[self.player.face_dir][self.player.frame]
        if self.player.face_dir == 3:  # left
            self.player.idle_image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], 0, 'h',
                                                       self.player.x, self.player.y, frame_data[2] * 4 , frame_data[3] * 4)
        else:
            self.player.idle_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                         self.player.x, self.player.y, frame_data[2] * 4 , frame_data[3] * 4)


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
        self.player.xdir = 0
        self.player.ydir = 0
        self.player.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1)
        if self.player.frame >= len(player_parring_animation):
            if not any(self.player.keys_pressed.values()):
                self.player.state_machine.handle_state_event(("TOIDLE", None))
            else:
                self.player.state_machine.handle_state_event(("TOWALK", None))

    def draw(self):
        character_frame_data = player_idle_animation[self.player.face_dir][0]
        frame_data = player_parring_animation[self.player.frame]
        if self.player.face_dir == 3:  # left
            self.player.idle_image.clip_composite_draw(character_frame_data[0], character_frame_data[1], character_frame_data[2], character_frame_data[3], 0,
                                                       'h',
                                                       self.player.x, self.player.y, character_frame_data[2] * 4,
                                                       character_frame_data[3] * 4)
        else:
            self.player.idle_image.clip_draw(character_frame_data[0], character_frame_data[1], character_frame_data[2], character_frame_data[3],
                                             self.player.x, self.player.y, character_frame_data[2] * 4, character_frame_data[3] * 4)
        self.player.parring_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],self.player.x, self.player.y, character_frame_data[2] * 6, character_frame_data[3] * 6)

class Roll:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
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
        speed = 10
        self.player.x += self.player.xdir * speed
        self.player.y += self.player.ydir * speed
        self.player.frame = (self.player.frame + 1)
        if self.player.frame >= len(player_roll_animation[self.player.face_dir]):
            if not any(self.player.keys_pressed.values()):
                self.player.state_machine.handle_state_event(("TOIDLE", None))
            else:
                self.player.state_machine.handle_state_event(("TOWALK", None))

    def draw(self):
        frame_data = player_roll_animation[self.player.face_dir][self.player.frame]
        if self.player.face_dir == 3:  # left
            self.player.roll_image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], 0,
                                                       'h',
                                                       self.player.x, self.player.y, frame_data[2] * 4,
                                                       frame_data[3] * 4)
        else:
            self.player.roll_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                             self.player.x, self.player.y, frame_data[2] * 4, frame_data[3] * 4)

class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
        self.player.frame = 0

    def exit(self, event):
        pass

    def do(self):
        # 애니메이션 업데이트
        self.player.frame = (self.player.frame + 1) % len(player_walk_animation[self.player.face_dir])

        # 키 상태에 따른 이동 처리
        speed = 5

        # 현재 누르고 있는 키들을 확인하여 이동

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
        frame_data = player_walk_animation[self.player.face_dir][self.player.frame]
        if self.player.face_dir == 3:  # left
            self.player.walk_image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], 0,
                                                       'h',
                                                       self.player.x, self.player.y, frame_data[2] * 4,
                                                       frame_data[3] * 4)
        else:
            self.player.walk_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                             self.player.x, self.player.y, frame_data[2] * 4, frame_data[3] * 4)

class Player:
    def __init__(self):
        self.x, self.y = 400, 300
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
        self.idle_image = load_image('resource/player/player_idle.png')
        self.death_image = load_image('resource/player/player_death.png')
        self.hit_image = load_image('resource/player/player_hit.png')
        self.parring_image = load_image('resource/player/player_parring.png')
        self.roll_image = load_image('resource/player/player_roll.png')
        self.walk_image = load_image('resource/player/player_walk.png')
        
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
                        space_key_down: self.ROLL, s_key_down: self.PARRING},
            self.WALK: {Toidle_event: self.IDLE, space_key_down: self.ROLL, s_key_down: self.PARRING},
            self.ROLL: {Toidle_event: self.IDLE, Towalk_event: self.WALK},
            self.PARRING: {Toidle_event: self.IDLE, Towalk_event: self.WALK},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = True
        elif event.type == SDL_KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = False
        self.state_machine.handle_state_event(("INPUT", event))

    def draw(self):
        self.state_machine.draw()
