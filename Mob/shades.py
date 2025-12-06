import random
import time

from pico2d import *
import game_framework
import game_world
from damage_text import DamageText
from state_machine import StateMachine
from behavior_tree import BehaviorTree, Selector, Sequence, Action, Condition
from Missile.missile import Missile

idle_animation = (
(0,0,24,39), (28,0,24,38), (56,0,24,38), (84,0,24,39)
)
death_animation = (
(0,0,33,32), (37,0,31,32), (72,0,36,32), (112,0,33,32),
(149,0,32,32), (185,0,36,32), (225,0,36,32), (265,0,36,32)

)
hit_animation = (
(0,0,30,39), (34,0,30,39)
)
attack_animation = (
(0,0,35,41), (39,0,29,41), (72,0,24,41), (100,0,29,41),
(133,0,35,41), (172,0,33,40), (209,0,35,41)
)
charge_attack_animation = (
(0,0,24,39), (28,0,24,38), (56, 0, 24, 37), (84,0,24,37)
)
walk_animation = (
    ((0,44,24,39), (28,44,28,40), (60,44,28,36), (92,44,25,39), (121,44,28,40), (153,44,28,38)), # 오른쪽 아래
    ((0,0,25,39), (29,0,28,40), (61,0,27,36), (92,0,25,39), (121,0,28,40), (153,0,28,38)),       # 오른쪽 위
)

# 상태 이벤트 헬퍼
def Toidle_event(state_event, mob):
    return state_event[0] == "TOIDLE"
def Todeath_event(state_event, mob):
    return state_event[0] == "TODEATH"
def Tohit_event(state_event, mob):
    return state_event[0] == "TOHIT"

def Toattack_normal_event(state_event, mob):
    return state_event[0] == "TOATTACK"

def Toattack_charge_event(state_event, mob):
    return state_event[0] == "TOCHARGEATTACK"

def Towalk_event(state_event, mob):
    return state_event[0] == "TOWALK"

# 속도/애니메이션 상수 (필요하면 조정)
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
        # behavior tree에서 공격 타이밍을 관리하므로 초기화만 유지
        if not hasattr(self.mob, 'attack_time'):
            self.mob.attack_time = time.time()

    def exit(self, event):
        pass

    def do(self):
        # 기존 애니메이션 갱신 유지 (애니메이션 변수는 파일 상단에 정의되어 있어야 함)
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % len(idle_animation)
        # Idle에서 직접 ATTACK으로 전환하지 않음 (behavior tree가 맡음)

    def draw(self):
        frame_data = idle_animation[int(self.mob.frame)]
        self.mob.idle_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 40)

class Walk:
    def __init__(self, mob):
        self.mob = mob
        self.duration = 0.0
        self.elapsed = 0.0
        self.frame = 0
        self.anim_index = 0
        self.flip = False

    def enter(self, event):
        # event expected: ('TOWALK', (dx, dy, duration))
        self.frame = 0
        self.elapsed = 0.0
        if event and len(event) > 1 and event[1]:
            dx, dy, duration = event[1]
        else:
            dx = dy = 0.0
            duration = 0.5
        self.mob.walk_dx = dx
        self.mob.walk_dy = dy
        self.duration = duration

        # 애니메이션 행 선택: dy > 0 -> index 1 (오른쪽 위), else 0 (오른쪽 아래)
        self.anim_index = 1 if dy > 0 else 0
        # 왼쪽으로 이동하면 좌우 반전
        self.flip = True if dx < 0 else False

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        # 이동
        self.mob.x += self.mob.walk_dx * dt
        self.mob.y += self.mob.walk_dy * dt

        # 애니메이션 프레임 업데이트 (walk 애니메이션은 6프레임)
        frames = len(walk_animation[self.anim_index])
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % frames

        # 시간 카운트, 시간이 끝나면 IDLE로 복귀
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.mob.current_state = 'IDLE'
            self.mob.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = walk_animation[self.anim_index][int(self.frame)]
        left, top, w, h = frame_data
        if self.flip:
            # 좌우 반전해서 그리기 (pico2d clip_composite_draw 사용)
            self.mob.walk_image.clip_composite_draw(left, top, w, h, 0, 'h', self.mob.x, self.mob.y, 30, 40)
        else:
            self.mob.walk_image.clip_draw(left, top, w, h, self.mob.x, self.mob.y, 30, 40)

class Attack:
    def __init__(self, mob):
        self.mob = mob

    def enter(self, event):
        self.mob.frame = 0

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt)
        if int(self.mob.frame) >= len(attack_animation):
            self.mob.frame = 0
            self.mob.fire_missile()
            self.mob.next_attack_type = None  # 공격 완료 신호
            self.mob.attack_time = time.time()
            self.mob.current_state = 'IDLE'
            self.mob.state_machine.handle_state_event(('TOIDLE', None))
            if hasattr(self.mob, 'start_random_walk'):
                self.mob.start_random_walk()

    def draw(self):
        frame_data = attack_animation[int(self.mob.frame) % len(attack_animation)]
        self.mob.attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                        self.mob.x, self.mob.y, 30, 40)


class ChargeAttack:
    def __init__(self, mob):
        self.mob = mob
        self.charge_duration = 2.0  # 차지 시간 2초
        self.charge_elapsed = 0.0
        self.missile_timer = 0.0
        self.missile_interval = 0.8  # 0.2초마다 미사일 발사

    def enter(self, event):
        self.mob.frame = 0
        self.charge_elapsed = 0.0
        self.missile_timer = 0.0

    def exit(self, event):
        pass

    def do(self):
        dt = game_framework.frame_time

        # 애니메이션이 마지막 프레임에 도달하지 않았으면 정상 애니메이션
        if int(self.mob.frame) < len(charge_attack_animation) - 1:
            self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt)
        else:
            # 마지막 프레임에서 머물면서 차지 공격 실행
            self.mob.frame = len(charge_attack_animation) - 1
            self.charge_elapsed += dt
            self.missile_timer += dt

            # 0.2초마다 사방으로 미사일 발사
            if self.missile_timer >= self.missile_interval:
                self.fire_radial_missiles()
                self.missile_timer = 0.0

            # 2초 후 공격 종료
            if self.charge_elapsed >= self.charge_duration:
                self.mob.next_attack_type = None
                self.mob.attack_time = time.time()
                self.mob.current_state = 'IDLE'
                self.mob.state_machine.handle_state_event(('TOIDLE', None))
                if hasattr(self.mob, 'start_random_walk'):
                    self.mob.start_random_walk()

    def fire_radial_missiles(self):
        import math

        # 회전 각도 추가 (22.5도씩 회전)
        if not hasattr(self, 'rotation_offset'):
            self.rotation_offset = 0.0

        # 8방향으로 일반 미사일 발사
        directions = 8
        for i in range(directions):
            # 기본 각도에 회전 오프셋 추가
            angle = (2 * math.pi / directions) * i + self.rotation_offset

            # 각 방향의 목표 위치 계산
            distance = 500  # 충분히 먼 거리
            target_x = self.mob.x + math.cos(angle) * distance
            target_y = self.mob.y + math.sin(angle) * distance

            missile = Missile(self.mob, target_x, target_y)
            game_world.add_object(missile, 1)
            game_world.add_collision_pair("player:mob_missile", None, missile)
            game_world.add_collision_pair("object:wall", missile, None)

        # 다음 발사를 위해 22.5도(π/8) 반시계 방향으로 회전
        self.rotation_offset += math.pi / 16
        # 2π를 넘으면 초기화
        if self.rotation_offset >= 2 * math.pi:
            self.rotation_offset -= 2 * math.pi

    def draw(self):
        frame_data = charge_attack_animation[int(self.mob.frame) % len(charge_attack_animation)]
        self.mob.charge_attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                               self.mob.x, self.mob.y, 30, 40)

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
                self.mob.state_machine.handle_state_event(('TODEATH', None))
            else:
                self.mob.current_state = 'IDLE'
                self.mob.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = hit_animation[int(self.mob.frame)]
        self.mob.hit_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 40)

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
            game_world.remove_object(self.mob)

    def draw(self):
        frame_data = death_animation[int(self.mob.frame)]
        self.mob.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 40)

class Shades:
    def __init__(self, x=640, y=360, level=1):
        # 기본 스탯
        self.hp = 12 * level
        self.max_hp = 12 * level
        self.damage = level
        self.attack_cooldown = 3.0 / level

        # 위치/애니메이션 상태
        self.x, self.y = x, y
        self.frame = 0

        # 리소스 로드 (파일 경로는 프로젝트에 맞게)
        self.font = load_font('ENCR10B.TTF', 30)
        self.idle_image = load_image('resource/mob/shades/shades_idle.png')
        self.attack_image = load_image('resource/mob/shades/shades_attack.png')
        self.charge_attack_image = load_image('resource/mob/shades/shades_charge_attack.png')
        self.death_image = load_image('resource/mob/shades/shades_death.png')
        self.hit_image = load_image('resource/mob/shades/shades_hit.png')
        self.walk_image = load_image('resource/mob/shades/shades_walk.png')

        self.IDLE = Idle(self)
        self.ATTACK = Attack(self)
        self.CHARGE_ATTACK = ChargeAttack(self)  # <- 반드시 추가
        self.DEATH = Death(self)
        self.HIT = Hit(self)
        self.WALK = Walk(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    Toattack_normal_event: self.ATTACK,
                    Toattack_charge_event: self.CHARGE_ATTACK,
                    Tohit_event: self.HIT,
                    Towalk_event: self.WALK
                },
                self.ATTACK: {Toidle_event: self.IDLE, Tohit_event: self.HIT},
                self.CHARGE_ATTACK: {Toidle_event: self.IDLE, Tohit_event: self.HIT},
                self.DEATH: {},
                self.HIT: {Toidle_event: self.IDLE, Todeath_event: self.DEATH},
                self.WALK: {
                    Toidle_event: self.IDLE,
                    Tohit_event: self.HIT,
                    Toattack_normal_event: self.ATTACK,
                    Toattack_charge_event: self.CHARGE_ATTACK
                }
            }
        )

        # behavior-tree 관련 초기화
        self.next_attack_type = None
        self.attack_time = time.time()
        self.behavior_tree = self._build_behavior_tree()

    def _build_behavior_tree(self):
        def cond_attack_ready(mob):
            ready = (time.time() - mob.attack_time) > mob.attack_cooldown
            return BehaviorTree.SUCCESS if ready else BehaviorTree.FAIL

        def action_normal_attack(mob):
            if mob.next_attack_type == 'normal' and mob.state_machine.cur_state == mob.ATTACK:
                return BehaviorTree.RUNNING  # 공격 진행 중

            r = random.random()
            will = r < 0.7
            if will:
                mob.next_attack_type = 'normal'
                mob.state_machine.handle_state_event(('TOATTACK',))
                return BehaviorTree.RUNNING  # 공격 시작
            return BehaviorTree.FAIL

        def action_charge_attack(mob):
            if mob.next_attack_type == 'charge' and mob.state_machine.cur_state == mob.CHARGE_ATTACK:
                return BehaviorTree.RUNNING  # 공격 진행 중

            mob.next_attack_type = 'charge'
            mob.state_machine.handle_state_event(('TOCHARGEATTACK',))
            return BehaviorTree.RUNNING

        def action_wander(mob):
            raw_dx = random.uniform(-20, 20)
            raw_dy = random.uniform(-20, 20)
            speed = random.uniform(20, 40)
            length = (raw_dx ** 2 + raw_dy ** 2) ** 0.5
            if length == 0:
                dx = dy = 0.0
            else:
                dx = raw_dx / length * speed
                dy = raw_dy / length * speed
            duration = random.uniform(0.4, 1.0)
            mob.state_machine.handle_state_event(('TOWALK', (dx, dy, duration)))
            return BehaviorTree.SUCCESS

        cond_node = Condition('AttackReady', cond_attack_ready, self)
        attack_choice = Selector('AttackChoice',
                                 Action('NormalAttack', action_normal_attack, self),
                                 Action('ChargeAttack', action_charge_attack, self))
        attack_seq = Sequence('AttackSeq', cond_node, attack_choice)
        root = Selector('Root', attack_seq, Action('Wander', action_wander, self))

        return BehaviorTree(root)

    def update(self):
        # Behavior Tree 먼저 실행하여 행동 결정
        if hasattr(self, 'behavior_tree'):
            self.behavior_tree.run()
        # 그 다음 상태 기계 업데이트
        self.state_machine.update()

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

        # 저장된 max_hp 사용
        max_hp = getattr(self, 'max_hp', 12 * getattr(self, 'level', 1))
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

    def start_random_walk(self):
        # 방향과 속도, 지속시간을 난수로 선택하여 Walk 상태로 전환
        raw_dx = random.uniform(-20, 20)
        raw_dy = random.uniform(-20, 20)
        speed = random.uniform(20, 40)
        length = (raw_dx ** 2 + raw_dy ** 2) ** 0.5
        if length == 0:
            dx = 0.0
            dy = 0.0
        else:
            dx = raw_dx / length * speed
            dy = raw_dy / length * speed
        duration = random.uniform(0.4, 1.0)
        self.state_machine.handle_state_event(('TOWALK', (dx, dy, duration)))