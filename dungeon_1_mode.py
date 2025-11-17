import game_framework
from pico2d import *
from dungeon_1 import Dungeon1
from redbook import RedBook
import game_world

player = None

def init(p = None):
    global player
    if p is None:
        from player import Player
        player = Player()
    else:
        player = p
    game_world.add_object(player, 1)
    game_world.add_collision_pair("player:mob_missile", player,None)
    player.x = 640
    player.y = 150
    dungeon_1 = Dungeon1()
    game_world.add_object(dungeon_1, 0)
    mobs = [RedBook()]
    game_world.add_objects(mobs, 1)
    for mob in mobs:
        game_world.add_collision_pair("attack:mob", None, mob)


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
