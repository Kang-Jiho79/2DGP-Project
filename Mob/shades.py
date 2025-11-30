import random
import time

from pico2d import *
import game_framework
import game_world
from damage_text import DamageText
from state_machine import StateMachine
from behavior_tree import BehaviorTree, Selector, Sequence, Action as BTAction, Condition as BTCondition

idle_animation = (
(0,0,24,39), (28,0,24,38), (56,0,24,38), (84,0,24,39),
(137,0,24,39), (165,0,24,38), (193,0,24,38), (221,0,24,39)
)
death_animation = (
(0,0,33,32), (37,0,31,29), (72,0,36,24), (112,0,33,24),
(149,0,32,26), (185,0,36,20), (225,0,36,22), (265,0,36,21)

)
hit_animation = (
(0,0,30,39), (34,0,30,39)
)
attack_animation = (
(0,0,35,38), (39,0,29,36), (72,0,24,36), (100,0,29,38),
(133,0,35,41), (172,0,33,40), (209,0,35,41)
)
charge_attack_animation = (
(0,0,24,39), (28,0,24,38), (56, 0, 24, 37), (84,0,24,37)
)
walk_animation = (
(0,44,24,39), (28,44,28,40), (60,44,28,36), (92,44,25,39), (121,44,28,40), (153,44,28,38),
(0,0,25,39), (29,0,28,40), (61,0,27,36), (92,0,25,39), (121,0,28,40), (153,0,28,38),
)

# 상태 이벤트 헬퍼
def Toidle_event(state_event, mob):
    return state_event[0] == "TOIDLE"
def Todeath_event(state_event, mob):
    return state_event[0] == "TODEATH"
def Tohit_event(state_event, mob):
    return state_event[0] == "TOHIT"
def Toattack_event(state_event, mob):
    return state_event[0] == "TOATTACK"

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
            # 실제 발사는 여기서 한 번만 수행
            if getattr(self.mob, 'next_attack_type', None) == 'charge':
                orig_damage = self.mob.damage
                # 차지 데미지 배수 (필요하면 조정)
                self.mob.damage = int(self.mob.damage * 3)
                self.mob.fire_missile()
                self.mob.damage = orig_damage
            else:
                self.mob.fire_missile()

            # 발사 후 공통 처리
            self.mob.next_attack_type = None
            self.mob.attack_time = time.time()

            self.mob.current_state = 'IDLE'
            self.mob.state_machine.handle_state_event(('TOIDLE', None))

    def draw(self):
        frame_data = attack_animation[int(self.mob.frame)]
        self.mob.attack_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

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
        self.mob.hit_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

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
        self.mob.death_image.clip_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3], self.mob.x, self.mob.y, 30, 30)

class Shades:
    def __init__(self, x=640, y=360, level=1):
        # 기본 스탯
        self.hp = 12 * level
        self.damage = level
        self.attack_cooldown = 3.0 / level

        # 위치/애니메이션 상태
        self.x, self.y = x, y
        self.frame = 0

        # 리소스 로드 (파일 경로는 프로젝트에 맞게)
        self.font = load_font('ENCR10B.TTF', 30)
        self.idle_image = load_image('resource/mob/shades/shades_idle.png')
        self.attack_image = load_image('resource/mob/shades/shades_attack.png')
        self.death_image = load_image('resource/mob/shades/shades_death.png')
        self.hit_image = load_image('resource/mob/shades/shades_hit.png')

        # 상태들 및 상태기계
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

        # behavior-tree 관련 초기화
        self.next_attack_type = None
        self.attack_time = time.time()
        self.behavior_tree = self._build_behavior_tree()

    def _build_behavior_tree(self):
        # 조건: 공격 준비(쿨타임 지남)
        def cond_attack_ready(mob):
            return BehaviorTree.SUCCESS if (time.time() - mob.attack_time) > mob.attack_cooldown else BehaviorTree.FAIL

        # 일반 공격 액션 70%
        def action_normal_attack(mob):
            if random.random() < 0.7:
                mob.next_attack_type = 'normal'
                mob.state_machine.handle_state_event(('TOATTACK', None))
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL

        # 차지 공격 액션 (나머지)
        def action_charge_attack(mob):
            mob.next_attack_type = 'charge'
            mob.state_machine.handle_state_event(('TOATTACK', None))
            return BehaviorTree.SUCCESS

        # 쿨다운 중 wander
        def action_wander(mob):
            dx = random.uniform(-20, 20) * 0.02
            dy = random.uniform(-20, 20) * 0.02
            mob.x += dx
            mob.y += dy
            return BehaviorTree.SUCCESS

        cond_node = BTCondition('AttackReady', cond_attack_ready, self)
        attack_choice = Selector('AttackChoice',
                                 BTAction('NormalAttack', action_normal_attack, self),
                                 BTAction('ChargeAttack', action_charge_attack, self))
        attack_seq = Sequence('AttackSeq', cond_node, attack_choice)
        root = Selector('Root', attack_seq, BTAction('Wander', action_wander, self))

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
        missile = ShadesMissile(self, player_x, player_y)
        game_world.add_object(missile, 1)
        game_world.add_collision_pair("player:mob_missile", None, missile)
        game_world.add_collision_pair("object:wall", missile, None)