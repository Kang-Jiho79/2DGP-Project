
import random

import game_framework
from pico2d import *


from Mob.agoniger import Agoniger
from Mob.bluebook import BlueBook
from Mob.bombshee import Bombshee
from Mob.greenbook import GreenBook
from Mob.redbook import RedBook
from Mob.shades import Shades
from Mob.smilely import Smilely

from dungeon import Dungeon
from wall import Wall
import game_world
from dungeon_gate import DungeonGate
from villiage_gate import VillageGate
import common

walls_info = (
    (0,720, 1280,590),
    (0,720, 160, 0),
    (0,135, 1280,0),
    (1120,720, 1280, 0)
)

def init(p = None):
    global dungeon
    # player 추가
    if common.player is None:
        from player import Player
        common.player = Player()
    game_world.add_object(common.player, 1)
    game_world.add_collision_pair("player:object", common.player,None)
    game_world.add_collision_pair("player:mob_missile", common.player,None)
    game_world.add_collision_pair("object:wall", common.player, None)
    common.player.x = 640
    common.player.y = 150
    common.player.current_thing = None
    common.player.near_thing = False

    # 배경 추가
    dungeon = Dungeon(common.player.cleared_dungeon + 1)
    game_world.add_object(dungeon, 0)
    # 몬스터 추가
    mobs = []
    game_world.add_objects(mobs, 1)
    for mob in mobs:
        game_world.add_collision_pair("attack:mob", None, mob)
        game_world.add_collision_pair("player_missile:mob", None, mob)

    # 벽 추가
    for wall_info in walls_info:
        wall = Wall(*wall_info)
        game_world.add_object(wall, 1)
        game_world.add_collision_pair("object:wall", None, wall)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            common.player.handle_events(event)  # handle_event -> handle_events로 수정


def update():
    game_world.update()
    game_world.handle_collision()
    check_monsters_remaining()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def check_monsters_remaining():
    """남은 몬스터 수 확인하고 모든 몬스터가 제거되면 던전 상태를 end로 변경"""
    global dungeon
    monster_count = 0
    for layer in game_world.world:
        for obj in layer:
            # 몬스터 클래스들 확인 (BlueBook, RedBook 등)
            if obj.__class__.__name__ in ['BlueBook', 'RedBook', 'GreenBook', 'Agoniger', 'Bombshee', 'Shades', 'Smilely']:
                monster_count += 1

    # 모든 몬스터가 제거되었으면 던전 상태를 end로 변경
    if monster_count == 0 and dungeon.get_state() == 'fighting':
        dungeon.state = 'end'
        common.player.cleared_dungeon += 1
        dungeon_gate = DungeonGate(640, 570)
        game_world.add_object(dungeon_gate,1)
        game_world.add_collision_pair("player:object", None, dungeon_gate)
        villiage_gate = VillageGate(640,155)
        game_world.add_object(villiage_gate,1)
        game_world.add_collision_pair("player:object", None, villiage_gate)