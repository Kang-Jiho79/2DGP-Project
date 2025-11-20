import random

import game_framework
from pico2d import *

from agoniger import Agoniger
from bluebook import BlueBook
from dungeon_1 import Dungeon1
from greenbook import GreenBook
from redbook import RedBook
import game_world
from villiage_gate import VillageGate

player = None
dungeon = None

def init(p = None):
    global player, dungeon
    if p is None:
        from player import Player
        player = Player()
    else:
        player = p
    game_world.add_object(player, 1)
    game_world.add_collision_pair("player:mob_missile", player,None)
    game_world.add_collision_pair("player:mob_guided_missile", player, None)
    player.x = 640
    player.y = 150
    dungeon = Dungeon1()
    game_world.add_object(dungeon, 0)
    mobs = [RedBook(random.randint(100, 1180), random.randint(300, 550)),
            GreenBook(random.randint(100, 1180), random.randint(300, 550)),
            BlueBook(random.randint(100, 1180), random.randint(300, 550)),
            Agoniger(random.randint(100, 1180), random.randint(300, 550))]
    game_world.add_objects(mobs, 1)
    for mob in mobs:
        game_world.add_collision_pair("attack:mob", None, mob)
        game_world.add_collision_pair("player_missile:mob", None, mob)
        game_world.add_collision_pair("player_guided_missile:mob", None, mob)


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_events(event)  # handle_event -> handle_events로 수정


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
            if obj.__class__.__name__ in ['BlueBook', 'RedBook', 'GreenBook']:
                monster_count += 1

    # 모든 몬스터가 제거되었으면 던전 상태를 end로 변경
    if monster_count == 0 and dungeon.get_state() == 'fighting':
        dungeon.state = 'end'
        villiagegate = VillageGate(640,150)
        game_world.add_object(villiagegate,1)