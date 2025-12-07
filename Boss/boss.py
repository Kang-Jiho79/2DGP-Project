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
((0, 79, 26, 21), (29, 83, 27, 18), (58, 83, 29, 17), (89, 76, 22, 22), (114, 69, 19, 17), (135, 69, 19, 13), (156, 69, 15, 17), (173, 70, 17, 19), (192, 70, 20,21))
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
    ((0, 71, 25, 21), (27, 67, 23, 22), (52, 66, 22, 21), (76, 71, 20, 21), (98, 67, 21, 22), (121, 66, 19, 21)),
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

        if random.random() < 0.001:  # 0.5% 확률
            self.boss.state_machine.handle_state_event(('TOSETTRAP', None))
            return

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
        self.last_missile_time = 0
        self.missile_interval = 0.1

    def enter(self, event):
        self.boss.frame = 0
        self.last_missile_time = 0
        self.missile_interval = 0.05
        self.boss.sound.play_sfx("boss_cheese_attack", volume=0.5)

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt * 0.5)
        self.last_missile_time += dt
        if self.last_missile_time >= self.missile_interval:
            self.boss.fire_cheese_missile()
            self.last_missile_time = 0

        # 플레이어를 보스 쪽으로 끌어당기기 (블랙홀 효과)
        player_x, player_y = self.boss.get_player_position()
        if player_x != self.boss.x or player_y != self.boss.y:
            dx = self.boss.x - player_x
            dy = self.boss.y - player_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 0:
                # 플레이어를 조금씩 끌어당김
                pull_strength = 50.0  # 끌어당기는 힘
                pull_x = (dx / distance) * pull_strength * dt
                pull_y = (dy / distance) * pull_strength * dt

                # 플레이어 위치 업데이트
                for layer in game_world.world:
                    for obj in layer:
                        if obj.__class__.__name__ == 'Player':
                            obj.x += pull_x
                            obj.y += pull_y
                            break

        if int(self.boss.frame) >= len(cheese_attack_animation):
            self.boss.frame = 0
            self.boss.next_attack_type = None
            self.boss.attack_time = time.time()
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data =cheese_attack_animation[int(self.boss.frame) % len(cheese_attack_animation)]
        self.boss.cheese_attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                                self.boss.x, self.boss.y, 50, 60)


class ElementAttack:
    def __init__(self, boss):
        self.boss = boss
        self.fired_frames = set()

    def enter(self, event):
        self.boss.frame = 0
        self.fired_frames.clear()

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.boss.frame = (self.boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt)
        current_frame = int(self.boss.frame)
        if 11 <= current_frame <= 18:
            if current_frame not in self.fired_frames:
                direction = current_frame - 11  # 0~6 방향
                self.boss.fire_element_attack(direction)
                self.fired_frames.add(current_frame)
        if int(self.boss.frame) >= len(element_attack_animation):
            self.boss.frame = 0
            self.boss.next_attack_type = None
            self.boss.attack_time = time.time()
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = element_attack_animation[int(self.boss.frame) % len(element_attack_animation)]
        self.boss.element_attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                                self.boss.x, self.boss.y, 50, 60)


class Hit:
    def __init__(self, boss):
        self.boss = boss

    def enter(self, event):
        self.boss.frame = 0
        self.boss.sound.play_sfx("boss_hit", volume=0.5)

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
        self.boss.sound.play_sfx("boss_set_trap", volume=0.5)

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

        if int(self.boss.frame) >= len(set_trap_animation):
            self.boss.frame = 0
            self.boss.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = set_trap_animation[int(self.boss.frame) % len(set_trap_animation)]
        self.boss.set_trap_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                          self.boss.x, self.boss.y, 40, 50)

class Boss:
    def __init__(self, x=640, y=360, level=5):
        # 기본 스탯
        self.hp = 50 * level
        self.max_hp = 50 * level
        self.damage = 5
        self.attack_cooldown = 1.5

        # 위치/애니메이션 상태
        self.x, self.y = x, y
        self.frame = 0

        # 리소스 로드
        self.font = load_font('ENCR10B.TTF', 30)
        self.idle_image = load_image('resource/boss/boss_idle.png')
        self.attack_image = load_image('resource/boss/boss_missile_attack.png')
        self.element_attack_image = load_image('resource/boss/boss_element_attack.png')
        self.cheese_attack_image = load_image('resource/boss/boss_cheese_attack.png')
        self.death_image = load_image('resource/boss/boss_death.png')
        self.hit_image = load_image('resource/boss/boss_hit.png')
        self.walk_image = load_image('resource/boss/boss_walk.png')
        self.roll_image = load_image('resource/boss/boss_roll.png')
        self.set_trap_image = load_image('resource/Boss/boss_set_trap.png')

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
                self.ATTACK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT,
                    Toroll_event: self.ROLL
                },
                self.CHEESE_ATTACK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT,
                    Toroll_event: self.ROLL
                },
                self.ELEMENT_ATTACK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT,
                    Toroll_event: self.ROLL
                },
                self.DEATH: {},
                self.HIT: {
                    Toidle_event: self.IDLE,
                    Todeath_event: self.DEATH,
                    Toroll_event: self.ROLL
                },
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
                self.SET_TRAP: {
                    Towalk_event: self.WALK,
                    Tohit_event: self.HIT,
                    Toidle_event: self.IDLE,
                    Toroll_event: self.ROLL
                }
            }
        )

        # behavior-tree 관련 초기화
        self.next_attack_type = None
        self.attack_time = time.time()
        self._build_behavior_tree()

        from sound_manager import SoundManager
        self.sound = SoundManager()
        self.sound.load_sfx("resource/sound/boss/boss_hit.wav", "boss_hit")
        self.sound.load_sfx("resource/sound/boss/boss_set_trap.wav", "boss_set_trap")
        self.sound.load_sfx("resource/sound/boss/boss_cheese_attack.wav", "boss_cheese_attack")

    def cond_attack_ready(self):
        ready = (time.time() - self.attack_time) > self.attack_cooldown
        return BehaviorTree.SUCCESS if ready else BehaviorTree.FAIL

    # --- 공격 액션들 ---

    def action_normal_attack(self):
        r = random.random()
        if r < 0.4:  # 40% 확률
            self.next_attack_type = 'normal'
            self.state_machine.handle_state_event(('TOATTACK', None))
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def action_cheese_attack(self):
        r = random.random()
        if r < 0.5:  # 30% 확률
            self.next_attack_type = 'cheese'
            self.state_machine.handle_state_event(('TOCHEESEATTACK', None))
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def action_element_attack(self):
        # 마지막 보정 공격
        self.next_attack_type = 'element'
        self.state_machine.handle_state_event(('TOELEMENTATTACK', None))
        return BehaviorTree.SUCCESS

    def action_wander(self):
        # 이미 Walk 상태면 그대로 둠
        if self.state_machine.cur_state == self.WALK:
            return BehaviorTree.SUCCESS

        # 랜덤 방향/속도/시간 결정
        raw_dx = random.uniform(-50, 50)
        raw_dy = random.uniform(-50, 50)
        speed = random.uniform(40, 80)
        length = (raw_dx ** 2 + raw_dy ** 2) ** 0.5
        if length == 0:
            dx = dy = 0.0
        else:
            dx = raw_dx / length * speed
            dy = raw_dy / length * speed
        duration = random.uniform(1.0, 2.0)

        # Walk 상태로 한 번만 전환
        self.state_machine.handle_state_event(('TOWALK', (dx, dy, duration)))
        return BehaviorTree.SUCCESS

    def _build_behavior_tree(self):
        # --- 트리 구성 ---

        attack_ready = Condition('AttackReady', self.cond_attack_ready)

        attack_choice = Selector(
            'AttackChoice',
            Action('NormalAttack', self.action_normal_attack),
            Action('CheeseAttack', self.action_cheese_attack),
            Action('ElementAttack', self.action_element_attack)
        )
        attack_seq = Sequence('AttackSeq', attack_ready, attack_choice)

        wander = Action('Wander', self.action_wander)

        root = Selector('Root', attack_seq, wander)

        self.behavior_tree = BehaviorTree(root)

    def update(self):
        if self.state_machine.cur_state == self.IDLE and hasattr(self, 'behavior_tree'):
            self.behavior_tree.run()

        # 실제 애니메이션/이동/공격 실행
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
        if group == 'attack:mob' or group == 'player_missile:mob':
            # 70% 확률로 롤 회피
            if (self.state_machine.cur_state == self.IDLE or
                    self.state_machine.cur_state == self.WALK):
                if random.random() < 0.7:
                    # 롤 상태로 전환하여 데미지 무효화
                    self.state_machine.handle_state_event(('TOROLL', None))
                    return  # 데미지를 받지 않고 종료
            if group == 'attack:mob':
                if other.player.parring_damage_boost:
                    damage = other.player.damage * 2
                    other.player.parring_damage_boost = False
                else:
                    damage = other.player.damage
            elif group == 'player_missile:mob':
                damage = other.shooter.damage
            self.take_damage(damage)
        if group == 'object:wall':
            # 벽과 충돌 시 이전 위치로 되돌리기 (플레이어와 동일한 로직)
            boss_left = self.x - 25
            boss_right = self.x + 25
            boss_bottom = self.y - 30
            boss_top = self.y + 30

            wall_left = other.left
            wall_right = other.right
            wall_bottom = other.bottom
            wall_top = other.top

            # 겹침 정도 계산
            overlap_x = min(boss_right - wall_left, wall_right - boss_left)
            overlap_y = min(boss_top - wall_bottom, wall_top - boss_bottom)

            # 더 적게 겹친 축으로만 밀어내기
            if overlap_x < overlap_y:
                # x축으로 밀어내기
                if self.x < other.x:
                    self.x = wall_left - 25  # 왼쪽으로 밀어내기
                else:
                    self.x = wall_right + 25  # 오른쪽으로 밀어내기
            else:
                # y축으로 밀어내기
                if self.y < other.y:
                    self.y = wall_bottom - 30  # 아래로 밀어내기
                else:
                    self.y = wall_top + 30  # 위로 밀어내기


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

        # 플레이어 방향 각도 계산
        dx = player_x - self.x
        dy = player_y - self.y
        base_angle = math.atan2(dy, dx)

        # 부채꼴 각도 범위 (총 60도)
        spread_angle = math.pi / 3  # 60도

        # 5개 미사일을 부채꼴 모양으로 발사
        for i in range(5):
            # -30도 ~ +30도 범위에서 균등하게 배치
            offset_angle = (i - 2) * (spread_angle / 4)  # -30, -15, 0, +15, +30도
            missile_angle = base_angle + offset_angle

            # 목표 지점 계산
            distance = 800  # 충분히 먼 거리
            target_x = self.x + math.cos(missile_angle) * distance
            target_y = self.y + math.sin(missile_angle) * distance

            # 미사일 생성
            missile = Missile(self, target_x, target_y)
            game_world.add_object(missile, 1)
            game_world.add_collision_pair("player:mob_missile", None, missile)
            game_world.add_collision_pair("object:wall", missile, None)

    def fire_cheese_missile(self):
        from Missile.cheese_missile import CheeseMissile

        # 맵 밖 랜덤 위치에서 생성
        canvas_width = get_canvas_width()
        canvas_height = get_canvas_height()

        # 4방향 중 하나 선택
        side = random.randint(0, 3)
        if side == 0:  # 위쪽에서
            start_x = random.randint(0, canvas_width)
            start_y = canvas_height + 50
        elif side == 1:  # 오른쪽에서
            start_x = canvas_width + 50
            start_y = random.randint(0, canvas_height)
        elif side == 2:  # 아래쪽에서
            start_x = random.randint(0, canvas_width)
            start_y = -50
        else:  # 왼쪽에서
            start_x = -50
            start_y = random.randint(0, canvas_height)

        # 보스를 타겟으로 하는 치즈 미사일 생성
        cheese_missile = CheeseMissile(start_x, start_y, self, 500)
        game_world.add_object(cheese_missile, 1)
        game_world.add_collision_pair("cheese_missile:boss", cheese_missile, None)
        game_world.add_collision_pair("player:mob_missile", None, cheese_missile)
    def fire_element_attack(self, direction):
        # 8방향으로 Element 생성
        element = Element(self.x, self.y, direction, self)
        game_world.add_object(element, 1)
        game_world.add_collision_pair("player:mob_missile", None, element)
        game_world.add_collision_pair("object:wall", element, None)
