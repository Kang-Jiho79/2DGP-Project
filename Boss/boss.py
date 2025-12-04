from pico2d import *
import game_framework
import game_world
import random
import time
import math
from state_machine import StateMachine
from behavior_tree import BehaviorTree, Node, Condition, Action, Selector, Sequence
from damage_text import DamageText
from Missile.missile import Missile
from Missile.element import Element

# 애니메이션 데이터
idle_animation = (
    (0, 0, 24, 39), (28, 0, 24, 38), (56, 0, 24, 37), (84, 0, 24, 37)
)

death_animation = (
    (0, 0, 30, 39), (34, 0, 30, 39)
)

hit_animation = (
    (0, 0, 30, 39), (34, 0, 30, 39)
)

attack_animation = (
    (0, 0, 35, 41), (39, 0, 29, 41), (72, 0, 24, 41), (100, 0, 29, 41),
    (133, 0, 35, 41), (172, 0, 33, 40), (209, 0, 35, 41)
)

charge_attack_animation = (
    (0, 0, 24, 39), (28, 0, 24, 38), (56, 0, 24, 37), (84, 0, 24, 37)
)

walk_animation = (
    ((0, 44, 24, 39), (28, 44, 28, 40), (60, 44, 28, 36), (92, 44, 25, 39), (121, 44, 28, 40), (153, 44, 28, 38)),
    # down
    ((0, 0, 25, 39), (29, 0, 28, 40), (61, 0, 27, 36), (92, 0, 25, 39), (121, 0, 28, 40), (153, 0, 28, 38)),  # right
    ((0, 44, 24, 39), (28, 44, 28, 40), (60, 44, 28, 36), (92, 44, 25, 39), (121, 44, 28, 40), (153, 44, 28, 38)),  # up
    ((0, 0, 25, 39), (29, 0, 28, 40), (61, 0, 27, 36), (92, 0, 25, 39), (121, 0, 28, 40), (153, 0, 28, 38))  # left
)

roll_animation = (
    ((0, 0, 24, 39), (28, 0, 24, 38), (56, 0, 24, 37), (84, 0, 24, 37)),  # down
    ((0, 44, 24, 39), (28, 44, 28, 40), (60, 44, 28, 36), (92, 44, 25, 39)),  # right
    ((121, 44, 28, 40), (153, 44, 28, 38), (181, 44, 28, 36), (209, 44, 25, 39)),  # up
    ((0, 44, 24, 39), (28, 44, 28, 40), (60, 44, 28, 36), (92, 44, 25, 39)),     # left
)

set_trap_animation = (
(0, 2, 19, 22), (21, 0, 19, 20), (42, 3, 19, 17), (63, 7, 22, 22),
(86, 8, 21, 22), (109, 9, 21, 22), (132, 4, 25, 19), (159, 2, 21, 19),
(182, 2, 21, 24), (205, 10, 20, 22), (227, 9, 18, 22), (247, 4, 21, 24),
(270, 3, 22, 21)
)


# 상태 이벤트 헬퍼
def Toidle_event(state_event, boss):
    return state_event[0] == "TOIDLE"


def Todeath_event(state_event, boss):
    return state_event[0] == "TODEATH"


def Tohit_event(state_event, boss):
    return state_event[0] == "TOHIT"


def Toattack_normal_event(state_event, boss):
    return state_event[0] == "TOATTACK"


def Toattack_cheese_event(state_event, boss):
    return state_event[0] == "TOCHEESEATTACK"


def Toattack_element_event(state_event, boss):
    return state_event[0] == "TOELEMENTATTACK"


def Towalk_event(state_event, boss):
    return state_event[0] == "TOWALK"


def Toroll_event(state_event, boss):
    return state_event[0] == "TOROLL"

def Tosettrap_event(state_event, boss):
    return state_event[0] == "TOSETTRAP"


# 속도/애니메이션 상수
PIXEL_PER_METER = (21.0 / 1.7)
RUN_SPEED_KMPH = 20.0
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
        if not hasattr(self.boss, 'attack_time'):
            self.boss.attack_time = time.time()

    def exit(self, event):
        pass

    def do(self):
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(
            idle_animation)

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
            self.anim_index = 1 if dx > 0 else 3  # right or left
            self.flip = dx < 0
        else:
            self.anim_index = 2 if dy > 0 else 0  # up or down
            self.flip = False

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.boss.x += self.boss.walk_dx * dt
        self.boss.y += self.boss.walk_dy * dt

        frames = len(walk_animation[self.anim_index])
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % frames

        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.boss.state_machine.handle_state_event(('TOIDLE', None))
            if random.random() < 0.001:  # 0.1% 확률로 함정 설치
                self.boss.state_machine.handle_state_event(('TOSETTRAP', None))

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

        # 랜덤 방향 선택
        direction = random.randint(0, 7)  # 8방향 (0~7)
        angle = direction * (math.pi / 4)  # 45도씩
        speed = random.uniform(100, 150)
        duration = random.uniform(0.8, 1.2)

        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed

        self.boss.walk_dx = dx
        self.boss.walk_dy = dy
        self.duration = duration

        # 애니메이션 방향 결정
        if abs(dx) > abs(dy):
            self.anim_index = 1 if dx > 0 else 3  # right or left
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

        # 화면 경계 체크
        self.boss.x = max(50, min(self.boss.x, get_canvas_width() - 50))
        self.boss.y = max(50, min(self.boss.y, get_canvas_height() - 50))

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
            self.boss.next_attack_type = None
            self.boss.attack_time = time.time()
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
        if int(self.boss.frame) >= len(charge_attack_animation):
            self.boss.frame = 0
            self.boss.fire_cheese_missile()
            self.boss.next_attack_type = None
            self.boss.attack_time = time.time()
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = charge_attack_animation[int(self.boss.frame) % len(charge_attack_animation)]
        self.boss.charge_attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
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
        if int(self.boss.frame) >= len(charge_attack_animation):
            self.boss.frame = 0
            self.boss.fire_element_attack()
            self.boss.next_attack_type = None
            self.boss.attack_time = time.time()
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = charge_attack_animation[int(self.boss.frame) % len(charge_attack_animation)]
        self.boss.charge_attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
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
        frame_data = hit_animation[int(self.boss.frame) % len(hit_animation)]
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
        frame_data = death_animation[int(self.boss.frame) % len(death_animation)]
        self.boss.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                        self.boss.x, self.boss.y, 50, 60)

class SetTrap:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.current_state = 'SET_TRAP'
        self.boss.frame = 0
        self.boss.xdir = 0
        self.boss.ydir = 0
        self.trap_created = False

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.boss.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * dt

        # 9번째 프레임에서 함정 생성
        if int(self.boss.frame) == 8 and not self.trap_created:
            from Boss.trap import Trap
            trap = Trap(self.boss.x, self.boss.y, self.boss)
            game_world.add_object(trap, 1)
            game_world.add_collision_pair('trap:player', trap, None)
            self.trap_created = True
            print("보스가 함정을 설치했습니다!")

        if int(self.boss.frame) >= len(settrap_animation):
            self.boss.state_machine.handle_state_event(('TOWALK', None))

    def draw(self):
        frame_data = settrap_animation[int(self.boss.frame) % len(settrap_animation)]
        self.boss.settrap_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                          self.boss.x, self.boss.y, 40, 50)

class Boss:
    def __init__(self, x=640, y=360, level=5):
        # 기본 스탯
        self.hp = 50 * level
        self.max_hp = 50 * level
        self.damage = level * 2
        self.attack_cooldown = 2.0

        # 위치/애니메이션 상태
        self.x, self.y = x, y
        self.frame = 0

        # 리소스 로드
        self.font = load_font('ENCR10B.TTF', 30)
        self.idle_image = load_image('resource/boss/boss_idle.png')
        self.attack_image = load_image('resource/boss/boss_attack.png')
        self.charge_attack_image = load_image('resource/boss/boss_charge_attack.png')
        self.death_image = load_image('resource/boss/boss_death.png')
        self.hit_image = load_image('resource/boss/boss_hit.png')
        self.walk_image = load_image('resource/boss/boss_walk.png')
        self.roll_image = load_image('resource/boss/boss_roll.png')
        self.settrap_image = load_image('resource/Boss/boss_settrap.png')

        # 상태 초기화
        self.IDLE = Idle(self)
        self.ATTACK = Attack(self)
        self.CHEESE_ATTACK = CheeseAttack(self)
        self.ELEMENT_ATTACK = ElementAttack(self)
        self.DEATH = Death(self)
        self.HIT = Hit(self)
        self.WALK = Walk(self)
        self.ROLL = Roll(self)
        self.SET_TRAP = SetTrap(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    Toattack_normal_event: self.ATTACK,
                    Toattack_cheese_event: self.CHEESE_ATTACK,
                    Toattack_element_event: self.ELEMENT_ATTACK,
                    Tohit_event: self.HIT,
                    Towalk_event: self.WALK,
                    Toroll_event: self.ROLL
                },
                self.ATTACK: {Toidle_event: self.IDLE, Tohit_event: self.HIT},
                self.CHEESE_ATTACK: {Toidle_event: self.IDLE, Tohit_event: self.HIT},
                self.ELEMENT_ATTACK: {Toidle_event: self.IDLE, Tohit_event: self.HIT},
                self.DEATH: {},
                self.HIT: {Toidle_event: self.IDLE, Todeath_event: self.DEATH},
                self.WALK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT,
                    Toattack_normal_event: self.ATTACK,
                    Toattack_cheese_event: self.CHEESE_ATTACK,
                    Toattack_element_event: self.ELEMENT_ATTACK,
                    Toroll_event: self.ROLL,
                    Tosettrap_event: self.SET_TRAP
                },
                self.ROLL: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT
                },
                self.SET_TRAP: {Towalk_event: self.WALK, Tohit_event: self.HIT}
            }
        )

        # behavior-tree 관련 초기화
        self.next_attack_type = None
        self.attack_time = time.time()
        self.behavior_tree = self._build_behavior_tree()

    def _build_behavior_tree(self):
        def cond_attack_ready(boss):
            ready = (time.time() - boss.attack_time) > boss.attack_cooldown
            return BehaviorTree.SUCCESS if ready else BehaviorTree.FAIL

        def action_normal_attack(boss):
            if boss.next_attack_type == 'normal' and boss.state_machine.cur_state == boss.ATTACK:
                return BehaviorTree.RUNNING

            r = random.random()
            if r < 0.4:  # 40% 확률
                boss.next_attack_type = 'normal'
                boss.state_machine.handle_state_event(('TOATTACK',))
                return BehaviorTree.RUNNING
            return BehaviorTree.FAIL

        def action_cheese_attack(boss):
            if boss.next_attack_type == 'cheese' and boss.state_machine.cur_state == boss.CHEESE_ATTACK:
                return BehaviorTree.RUNNING

            r = random.random()
            if r < 0.3:  # 30% 확률
                boss.next_attack_type = 'cheese'
                boss.state_machine.handle_state_event(('TOCHEESEATTACK',))
                return BehaviorTree.RUNNING
            return BehaviorTree.FAIL

        def action_element_attack(boss):
            if boss.next_attack_type == 'element' and boss.state_machine.cur_state == boss.ELEMENT_ATTACK:
                return BehaviorTree.RUNNING

            boss.next_attack_type = 'element'
            boss.state_machine.handle_state_event(('TOELEMENTATTACK',))
            return BehaviorTree.RUNNING

        def action_roll(boss):
            boss.state_machine.handle_state_event(('TOROLL', None))
            return BehaviorTree.SUCCESS

        def action_wander(boss):
            raw_dx = random.uniform(-30, 30)
            raw_dy = random.uniform(-30, 30)
            speed = random.uniform(30, 60)
            length = (raw_dx ** 2 + raw_dy ** 2) ** 0.5
            if length == 0:
                dx = dy = 0.0
            else:
                dx = raw_dx / length * speed
                dy = raw_dy / length * speed
            duration = random.uniform(0.5, 1.5)
            boss.state_machine.handle_state_event(('TOWALK', (dx, dy, duration)))
            return BehaviorTree.SUCCESS

        cond_node = Condition('AttackReady', cond_attack_ready, self)
        attack_choice = Selector('AttackChoice',
                                 Action('NormalAttack', action_normal_attack, self),
                                 Action('CheeseAttack', action_cheese_attack, self),
                                 Action('ElementAttack', action_element_attack, self))
        attack_seq = Sequence('AttackSeq', cond_node, attack_choice)

        movement_choice = Selector('MovementChoice',
                                   Action('Roll', action_roll, self),
                                   Action('Wander', action_wander, self))

        root = Selector('Root', attack_seq, movement_choice)

        return BehaviorTree(root)

    def update(self):
        if hasattr(self, 'behavior_tree'):
            self.behavior_tree.run()
        self.state_machine.update()

    def handle_events(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

        # HP바 그리기
        bar_width = 100
        bar_height = 10
        hp_ratio = self.hp / self.max_hp

        # 배경 (검은색)
        draw_rectangle(self.x - bar_width // 2, self.y + 40,
                       self.x + bar_width // 2, self.y + 40 + bar_height,
                       0, 0, 0, 255, 1)

        # HP (빨간색)
        if hp_ratio > 0:
            draw_rectangle(self.x - bar_width // 2, self.y + 40,
                           self.x - bar_width // 2 + bar_width * hp_ratio, self.y + 40 + bar_height,
                           255, 0, 0, 255, 1)

    def get_bb(self):
        return self.x - 25, self.y - 30, self.x + 25, self.y + 30

    def handle_collision(self, group, other):
        if group == 'attack:boss' or group == 'player_missile:boss' or group == 'cheese_missile:boss':
            if group == 'attack:boss':
                damage = other.player.damage
            elif group == 'player_missile:boss':
                damage = other.shooter.damage
            elif group == 'cheese_missile:boss':
                damage = 10  # 치즈 미사일 데미지

            self.take_damage(damage)

    def take_damage(self, damage):
        damage_text = DamageText(self.x, self.y, damage)
        game_world.add_object(damage_text, 1)
        self.hp -= damage
        self.state_machine.handle_state_event(('TOHIT', None))

    def get_player_position(self):
        for layer in game_world.world:
            for obj in layer:
                if obj.__class__.__name__ == 'Player':
                    return obj.x, obj.y
        return self.x, self.y

    def fire_missile(self):
        player_x, player_y = self.get_player_position()
        missile = Missile(self, player_x, player_y)
        game_world.add_object(missile, 1)
        game_world.add_collision_pair("player:mob_missile", None, missile)
        game_world.add_collision_pair("object:wall", missile, None)

    def fire_cheese_missile(self):
        from Missile.cheese_missile import CheeseMissile
        cheese_missile = CheeseMissile(self.x, self.y, self, 150)
        game_world.add_object(cheese_missile, 1)
        game_world.add_collision_pair("cheese_missile:boss", cheese_missile, None)
        game_world.add_collision_pair("player:mob_missile", None, cheese_missile)

    def fire_element_attack(self):
        # 8방향으로 Element 생성
        for direction in range(8):
            element = Element(self.x, self.y, direction, self)
            game_world.add_object(element, 1)
            game_world.add_collision_pair("element:player", element, None)
            game_world.add_collision_pair("object:wall", element, None)
