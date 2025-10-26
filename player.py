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
    (0,102,54,102), (54,102,54,102), (108,102,54,102), (162,102,54,102), (216,102,54,102),
    (0,0,54,102), (54,0,54,102), (108,0,54,102), (162,0,54,102)
)
player_roll_animation = (
    ((0, 63, 17, 21), (17, 63, 17, 21), (34, 63, 17, 21), (51, 63, 17, 21), (68, 63, 17, 21), (85, 63, 17, 21), (102, 63, 17, 21), (119, 63, 17, 21), (136, 63, 17, 21)),
    ((0, 42, 17, 21), (17, 42, 17, 21), (34, 42, 17, 21), (51, 42, 17, 21), (68, 42, 17, 21), (85, 42, 17, 21), (102, 42, 17, 21), (119, 42, 17, 21), (136, 42, 17, 21), (153, 42, 17, 21), (170, 42, 17, 21)),
    ((0, 21, 17, 21), (17, 21, 17, 21), (34, 21, 17, 21), (51, 21, 17, 21), (68, 21, 17, 21), (85, 21, 17, 21), (102, 21, 17, 21), (119, 21, 17, 21), (136, 21, 17, 21)),
    ((0, 42, 17, 21), (17, 42, 17, 21), (34, 42, 17, 21), (51, 42, 17, 21), (68, 42, 17, 21), (85, 42, 17, 21), (102, 42, 17, 21), (119, 42, 17, 21), (136, 42, 17, 21), (153, 42, 17, 21), (170, 42, 17, 21))
)
player_walk_animation = (
    ((0, 87, 15, 25), (17, 87, 15, 25), (35, 87, 15, 25), (56, 87, 15, 25), (74, 87, 15, 25), (95, 87, 15, 25)),
    ((0, 58, 15, 25), (14, 58, 15, 25), (31, 58, 15, 25), (49, 58, 15, 25), (63, 58, 15, 25), (79, 58, 15, 25)),
    ((0, 30, 17, 25), (17, 30, 17, 25), (35, 30, 17, 25), (51, 30, 17, 25), (71, 30, 17, 25), (87, 30, 17, 25)),
    ((0, 58, 15, 25), (14, 58, 15, 25), (31, 58, 15, 25), (49, 58, 15, 25), (63, 58, 15, 25), (79, 58, 15, 25))
)

def up_key_down(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_UP
def up_key_up(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_UP
def down_key_down(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYDOWN and state_event[1].key == SDLK_DOWN
def down_key_up(state_event):
    return state_event[0] == "INPUT" and state_event[1].type == SDL_KEYUP and state_event[1].key == SDLK_DOWN



class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
        self.player.dir = 0
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


class Roll:
    def __init__(self, player):
        self.player = player


class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, event):
        self.player.dir = 0
        self.player.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % len(player_walk_animation[self.player.face_dir])

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
        self.face_dir = 2   # up:0, right:1, down:2, left:3
        self.dir = 0
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
            self.WALK,
        {
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_events(self):
        self.state_machine.handle_state_event(("INPUT", event))

    def draw(self):
        self.state_machine.draw()
