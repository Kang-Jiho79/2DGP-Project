import game_framework
from pico2d import *

from Npc.dummy import Dummy
from Npc.item_npc import ItemNPC
import game_world
from Npc.upgrade_npc import UpgradeNPC
from Village.village import Village
from dungeon_gate import DungeonGate
from sound_manager import SoundManager
from wall import Wall
import common

walls_info = (
    (265, 430, 520, 240),
    (775, 430, 1030, 240),
)

def init():
    # player 추가
    if common.player is None:
        from player import Player
        common.player = Player()
    else:
        common.player.x = 640
        common.player.y = 600
    game_world.add_object(common.player, 1)
    game_world.add_collision_pair("player:object", common.player, None)
    game_world.add_collision_pair("object:wall", common.player, None)

    # 배경 추가
    village = Village()
    game_world.add_object(village, 0)
    # NPC 추가
    item_npc = ItemNPC()
    game_world.add_object(item_npc, 1)
    game_world.add_collision_pair("player:object", None, item_npc)
    upgrade_npc = UpgradeNPC()
    game_world.add_object(upgrade_npc, 1)
    game_world.add_collision_pair("player:object", None, upgrade_npc)
    # 더미 추가
    dummy = Dummy()
    game_world.add_object(dummy, 1)
    game_world.add_collision_pair('attack:mob',None,dummy)
    # 던전 게이트 추가
    dungeon_gate = DungeonGate(640, 600)
    game_world.add_object(dungeon_gate, 1)
    game_world.add_collision_pair("player:object", None, dungeon_gate)
    # 벽 추가
    for wall_info in walls_info:
        wall = Wall(*wall_info)
        game_world.add_object(wall, 1)
        game_world.add_collision_pair("object:wall", None, wall)
    sm = SoundManager()
    sm.play_music("resource/sound/bgm/village_bgm.mp3")
    sm.set_music_volume(0.1)


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
