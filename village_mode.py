import game_framework
from pico2d import *

from dummy import Dummy
from item_npc import ItemNPC
from player import Player
import game_world
from upgrade_npc import UpgradeNPC
from village import Village
from dungeon_gate import DungeonGate
import common

def init():
    if common.player is None:
        from player import Player
        common.player = Player()
    else:
        common.player.x = 640
        common.player.y = 600
    game_world.add_object(common.player, 1)
    game_world.add_collision_pair("player:object", common.player, None)
    village = Village()
    game_world.add_object(village, 0)
    item_npc = ItemNPC()
    game_world.add_object(item_npc, 1)
    game_world.add_collision_pair("player:object", None, item_npc)
    upgrade_npc = UpgradeNPC()
    game_world.add_object(upgrade_npc, 1)
    game_world.add_collision_pair("player:object", None, upgrade_npc)
    dummy = Dummy()
    game_world.add_object(dummy, 1)
    game_world.add_collision_pair('attack:mob',None,dummy)
    dungeon_gate = DungeonGate(640, 600, common.player.cleared_dungeons)
    game_world.add_object(dungeon_gate, 1)
    game_world.add_collision_pair("player:object", None, dungeon_gate)

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
