import random
import time

from pico2d import *
import game_framework
import game_world
from damage_text import DamageText
from state_machine import StateMachine

cheese_attack_animation = (
(0, 0, 24, 21), (26, 0, 24, 22), (51, 0, 24, 21), (78, 0, 24, 21),
(104, 0, 24, 21), (130, 0, 24, 22), (156, 0, 24, 21), (182, 0, 24, 22),
(208, 0, 24, 21), (234, 0, 24, 21), (260, 0, 24, 21), (286, 0, 24, 22)
)

death_animation = (
(0, 3, 21, 20), (23, 4, 22, 19), (47, 3, 25, 17), (74, 1, 25, 16),
(101, 0, 27, 16)
)

element_attack_animation = (
(0, 38, 20, 20), (22, 41, 22, 20), (46, 42, 26, 20), (74, 37, 26, 20),
(102, 37, 22, 18), (126, 36, 16, 20), (144, 36, 16, 19), (162, 36, 16, 20),
(183, 36, 18, 23), (203, 37,18, 21), (223, 36, 16, 22), (0, 1, 16, 22),
(18, 1, 24, 21), (44, 1, 31, 23), (77, 1, 30, 25), (109, 2, 16, 28),
(127, 1, 28, 26), (157, 0, 27, 24), (186, 1, 16, 22), (204, 2, 16, 21),
(222, 4, 24, 20), (248, 1, 16, 20), (266, 1, 16, 19), (284, 1, 16, 20)
)

hit_animation = (
(0, 0, 22, 20), (23, 0, 21, 22), (46, 0, 22, 21)
)

idle_animation = (
(0, 0, 16, 21), (18, 0, 16, 21), (36, 0, 16, 20), (54, 0, 16, 21)
)

attack_animation = (
(0, 0, 24, 21), (27, 5, 16, 23), (45, 6, 18, 22), (65, 11, 19, 22),
(86, 9, 18, 22), (106, 5, 21, 24), (129, 1, 22, 21), (153, 1, 28, 17),
(183, 1, 26, 18)
)

roll_animation = (
((0, 116, 18, 18), (20, 119, 20, 16), (42, 121, 20, 14), (64, 112, 16, 22), (82, 107, 18, 20), (102, 108, 19, 15), (123, 108, 21, 9), (146, 107, 18, 16), (166, 108, 16, 19)),  # down
((0, 79, 26, 21), (29, 83, 27, 18), (58, 83, 29, 17), (89, 76, 22, 22), (114, 69, 19, 17), (135, 69, 19, 13), (156, 69, 15, 17), (173, 70, 17, 19), (192, 70, 20,21)),          # right
((0, 39, 16, 24), (18, 45, 18, 17), (38, 47, 16, 13), (56, 42, 14, 15), (72, 36, 16, 14), (90, 37, 20, 10), (112, 37, 18, 14), (133, 36, 16, 19), (151, 26, 16, 21)),           # up
)

set_trap_animation = (
(0, 2, 19, 22), (21, 0, 19, 20), (42, 3, 19, 17), (63, 7, 22, 22),
(86, 8, 21, 22), (109, 9, 21, 22), (132, 4, 25, 19), (159, 2, 21, 19),
(182, 2, 21, 24), (205, 10, 20, 22), (227, 9, 18, 22), (247, 4, 21, 24), (270, 3, 22, 21)
)

walk_animation = (
    ((0, 102, 16, 20), (18, 99, 18, 20), (38, 98, 16, 18), (56, 102, 16, 20), (74, 99, 18, 20), (94, 98, 16, 18)),          # down
    ((0, 71, 25, 21), (27, 67, 23, 22), (52, 66, 22, 21), (76, 71, 20, 21), (98, 67, 21, 22), (121, 66, 19, 21)),           # right
    ((0, 37, 16, 23), (18, 37, 18, 20), (38, 34, 16, 20), (57, 37, 16, 23), (75, 37, 18, 20), (95, 34, 16, 20)),            # up
)

# 상태 이벤트 헬퍼
def Toidle_event(state_event, boss):
    return state_event[0] == "TOIDLE"


def Todeath_event(state_event, boss):
    return state_event[0] == "TODEATH"


def Tohit_event(state_event, boss):
    return state_event[0] == "TOHIT"


def Toattack_event(state_event, boss):
    return state_event[0] == "TOATTACK"


def Tocheese_attack_event(state_event, boss):
    return state_event[0] == "TOCHEESEATTACK"


def Toelement_attack_event(state_event, boss):
    return state_event[0] == "TOELEMENTATTACK"


def Toset_trap_event(state_event, boss):
    return state_event[0] == "TOSETTRAP"


def Towalk_event(state_event, boss):
    return state_event[0] == "TOWALK"


def Toroll_event(state_event, boss):
    return state_event[0] == "TOROLL"


# 속도/애니메이션 상수
PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 15.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Idle:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.frame = 0
        self.boss.action_timer = time.time()

    def exit(self, event):
        pass

    def do(self):
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(
            idle_animation)

        # 3초 후 랜덤 행동 결정
        if time.time() - self.boss.action_timer > 3.0:
            self.boss.decide_next_action()

    def draw(self):
        frame_data = idle_animation[int(self.boss.frame)]
        self.boss.idle_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                       self.boss.x, self.boss.y, 50, 60)


class Walk:
    def __init__(self, boss):
        self.boss = boss
        self.duration = 0.0
        self.elapsed = 0.0
        self.frame = 0
        self.anim_index = 0
        self.flip = False

    def enter(self, event):
        self.frame = 0
        self.elapsed = 0.0
        if event and len(event) > 1 and event[1]:
            dx, dy, duration = event[1]
        else:
            dx = dy = 0.0
            duration = 1.0
        self.boss.walk_dx = dx
        self.boss.walk_dy = dy
        self.duration = duration

        # 애니메이션 방향 결정
        if abs(dx) > abs(dy):
            self.anim_index = 1 if dx > 0 else 1  # right
            self.flip = dx < 0
        else:
            self.anim_index = 2 if dy > 0 else 0  # up or down
            self.flip = False

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        # 이동
        self.boss.x += self.boss.walk_dx * dt
        self.boss.y += self.boss.walk_dy * dt

        # 애니메이션 프레임 업데이트
        frames = len(walk_animation[self.anim_index])
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % frames

        # 시간 카운트, 시간이 끝나면 IDLE로 복귀
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = walk_animation[self.anim_index][int(self.frame)]
        left, top, w, h = frame_data
        if self.flip:
            self.boss.walk_image.clip_composite_draw(left, top, w, h, 0, 'h',
                                                     self.boss.x, self.boss.y, 50, 60)
        else:
            self.boss.walk_image.clip_draw(left, top, w, h, self.boss.x, self.boss.y, 50, 60)


class Roll:
    def __init__(self, boss):
        self.boss = boss
        self.duration = 0.0
        self.elapsed = 0.0
        self.frame = 0
        self.anim_index = 0
        self.flip = False

    def enter(self, event):
        self.frame = 0
        self.elapsed = 0.0
        if event and len(event) > 1 and event[1]:
            dx, dy, duration = event[1]
        else:
            dx = dy = 0.0
            duration = 1.0
        self.boss.walk_dx = dx * 2  # 롤링은 더 빠르게
        self.boss.walk_dy = dy * 2
        self.duration = duration

        # 애니메이션 방향 결정
        if abs(dx) > abs(dy):
            self.anim_index = 1  # right
            self.flip = dx < 0
        else:
            self.anim_index = 2 if dy > 0 else 0  # up or down
            self.flip = False

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        # 빠른 이동
        self.boss.x += self.boss.walk_dx * dt
        self.boss.y += self.boss.walk_dy * dt

        # 애니메이션 프레임 업데이트
        frames = len(roll_animation[self.anim_index])
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt * 1.5) % frames

        # 시간 카운트
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = roll_animation[self.anim_index][int(self.frame)]
        left, top, w, h = frame_data
        if self.flip:
            self.boss.roll_image.clip_composite_draw(left, top, w, h, 0, 'h',
                                                     self.boss.x, self.boss.y, 50, 60)
        else:
            self.boss.roll_image.clip_draw(left, top, w, h, self.boss.x, self.boss.y, 50, 60)


class Attack:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.frame = 0

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt)
        if int(self.boss.frame) >= len(attack_animation):
            self.boss.frame = 0
            self.boss.fire_missile()
            self.boss.action_timer = time.time()
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = attack_animation[int(self.boss.frame) % len(attack_animation)]
        self.boss.attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                         self.boss.x, self.boss.y, 50, 60)


class CheeseAttack:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.frame = 0

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt)
        if int(self.boss.frame) >= len(cheese_attack_animation):
            self.boss.frame = 0
            self.boss.fire_cheese_missile()
            self.boss.action_timer = time.time()
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = cheese_attack_animation[int(self.boss.frame) % len(cheese_attack_animation)]
        self.boss.cheese_attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                                self.boss.x, self.boss.y, 50, 60)


class ElementAttack:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.frame = 0

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt)
        if int(self.boss.frame) >= len(element_attack_animation):
            self.boss.frame = 0
            self.boss.fire_element_missile()
            self.boss.action_timer = time.time()
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = element_attack_animation[int(self.boss.frame) % len(element_attack_animation)]
        self.boss.element_attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                                 self.boss.x, self.boss.y, 50, 60)


class SetTrap:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.frame = 0

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt)
        if int(self.boss.frame) >= len(set_trap_animation):
            self.boss.frame = 0
            self.boss.place_trap()
            self.boss.action_timer = time.time()
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = set_trap_animation[int(self.boss.frame) % len(set_trap_animation)]
        self.boss.set_trap_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                           self.boss.x, self.boss.y, 50, 60)


class Hit:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.boss.frame >= len(hit_animation):
            if self.boss.hp <= 0:
                self.boss.state_machine.handle_state_event(('TODEATH', None))
            else:
                self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = hit_animation[int(self.boss.frame)]
        self.boss.hit_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                      self.boss.x, self.boss.y, 50, 60)


class Death:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.boss.frame >= len(death_animation):
            game_world.remove_object(self.boss)

    def draw(self):
        frame_data = death_animation[int(self.boss.frame)]
        self.boss.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                        self.boss.x, self.boss.y, 50, 60)


class Boss:
    def __init__(self, x=640, y=360, level=1):
        # 기본 스탯
        self.hp = 100 * level
        self.max_hp = 100 * level
        self.damage = 3 * level
        self.level = level

        # 위치/애니메이션 상태
        self.x, self.y = x, y
        self.frame = 0
        self.action_timer = time.time()

        # 이동 관련
        self.walk_dx = 0
        self.walk_dy = 0

        # 리소스 로드
        self.font = load_font('ENCR10B.TTF', 30)
        self.idle_image = load_image('resource/boss/boss_idle.png')
        self.attack_image = load_image('resource/boss/boss_attack.png')
        self.cheese_attack_image = load_image('resource/boss/boss_cheese_attack.png')
        self.element_attack_image = load_image('resource/boss/boss_element_attack.png')
        self.set_trap_image = load_image('resource/boss/boss_set_trap.png')
        self.death_image = load_image('resource/boss/boss_death.png')
        self.hit_image = load_image('resource/boss/boss_hit.png')
        self.walk_image = load_image('resource/boss/boss_walk.png')
        self.roll_image = load_image('resource/boss/boss_roll.png')

        # 상태 클래스 생성
        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.ROLL = Roll(self)
        self.ATTACK = Attack(self)
        self.CHEESE_ATTACK = CheeseAttack(self)
        self.ELEMENT_ATTACK = ElementAttack(self)
        self.SET_TRAP = SetTrap(self)
        self.HIT = Hit(self)
        self.DEATH = Death(self)

        # 상태 머신 설정
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    Toattack_event: self.ATTACK,
                    Tocheese_attack_event: self.CHEESE_ATTACK,
                    Toelement_attack_event: self.ELEMENT_ATTACK,
                    Toset_trap_event: self.SET_TRAP,
                    Towalk_event: self.WALK,
                    Toroll_event: self.ROLL,
                    Tohit_event: self.HIT
                },
                self.WALK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT
                },
                self.ROLL: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT
                },
                self.ATTACK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT
                },
                self.CHEESE_ATTACK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT
                },
                self.ELEMENT_ATTACK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT
                },
                self.SET_TRAP: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT
                },
                self.HIT: {
                    Toidle_event: self.IDLE,
                    Todeath_event: self.DEATH
                },
                self.DEATH: {}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_events(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        # HP 바 그리기
        self.draw_hp_bar()

    def draw_hp_bar(self):
        # HP바 배경 (검은색)
        draw_rectangle(self.x - 50, self.y + 50, self.x + 50, self.y + 60, 0, 0, 0, 255, 1)
        # HP바 (빨간색)
        hp_ratio = self.hp / self.max_hp
        draw_rectangle(self.x - 50, self.y + 50, self.x - 50 + 100 * hp_ratio, self.y + 60, 255, 0, 0, 255, 1)

    def get_bb(self):
        return self.x - 25, self.y - 30, self.x + 25, self.y + 30

    def decide_next_action(self):
        """다음 행동을 랜덤으로 결정"""
        actions = ['attack', 'cheese_attack', 'element_attack', 'set_trap', 'walk', 'roll']
        weights = [25, 20, 20, 15, 10, 10]  # 확률 가중치

        action = random.choices(actions, weights=weights)[0]

        if action == 'attack':
            self.state_machine.handle_state_event(('TOATTACK', None))
        elif action == 'cheese_attack':
            self.state_machine.handle_state_event(('TOCHEESEATTACK', None))
        elif action == 'element_attack':
            self.state_machine.handle_state_event(('TOELEMENTATTACK', None))
        elif action == 'set_trap':
            self.state_machine.handle_state_event(('TOSETTRAP', None))
        elif action == 'walk':
            # 랜덤 방향으로 이동
            dx = random.uniform(-30, 30)
            dy = random.uniform(-30, 30)
            duration = random.uniform(1.0, 2.0)
            self.state_machine.handle_state_event(('TOWALK', (dx, dy, duration)))
        elif action == 'roll':
            # 랜덤 방향으로 빠른 이동
            dx = random.uniform(-50, 50)
            dy = random.uniform(-50, 50)
            duration = random.uniform(0.5, 1.0)
            self.state_machine.handle_state_event(('TOROLL', (dx, dy, duration)))

    def get_player_position(self):
        for layer in game_world.world:
            for obj in layer:
                if obj.__class__.__name__ == 'Player':
                    return obj.x, obj.y
        return self.x, self.y

    def fire_missile(self):
        """일반 미사일 발사"""
        from Missile.missile import Missile
        player_x, player_y = self.get_player_position()
        missile = Missile(self, player_x, player_y)
        game_world.add_object(missile, 1)
        game_world.add_collision_pair("player:mob_missile", None, missile)
        game_world.add_collision_pair("object:wall", missile, None)

    def fire_cheese_missile(self):
        """치즈 미사일 발사 (유도 미사일)"""
        from Missile.guided_missile import GuidedMissile
        missile = GuidedMissile(self, 100, 2.0, 5.0)
        game_world.add_object(missile, 1)
        game_world.add_collision_pair("player:mob_missile", None, missile)

    def fire_element_missile(self):
        """원소 미사일 발사 (바운싱 미사일)"""
        from Missile.bouncing_missile import BouncingMissile
        player_x, player_y = self.get_player_position()
        dx = player_x - self.x
        dy = player_y - self.y
        length = (dx * dx + dy * dy) ** 0.5
        if length > 0:
            dx /= length
            dy /= length
        missile = BouncingMissile(self, self.x, self.y, dx * 100, dy * 100)
        game_world.add_object(missile, 1)
        game_world.add_collision_pair("player:mob_missile", None, missile)
        game_world.add_collision_pair("object:wall", missile, None)

    def place_trap(self):
        """트랩 설치"""
        print("트랩이 설치되었습니다!")
        # 여기에 트랩 객체 생성 로직 추가 가능

    def handle_collision(self, group, other):
        if group == 'attack:mob':
            damage = other.player.damage
            self.take_damage(damage)
        if group == 'player_missile:mob':
            damage = other.shooter.damage // 2
            self.take_damage(damage)

    def take_damage(self, damage):
        damage_text = DamageText(self.x, self.y, damage)
        game_world.add_object(damage_text, 1)
        self.hp -= damage
        self.state_machine.handle_state_event(('TOHIT', None))

