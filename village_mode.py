import game_framework
from pico2d import *

from item_npc import ItemNPC
from player import Player
import game_world
from village import Village

player = None

def init():
    global player
    player = Player()
    game_world.add_object(player, 1)
    village = Village()
    game_world.add_object(village, 0)
    item_npc = ItemNPC()
    game_world.add_object(item_npc, 1)
    game_world.add_collision_pair("player:item_npc", player, None)
    game_world.add_collision_pair("player:item_npc", None, item_npc)

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
