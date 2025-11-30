import game_framework
from pico2d import *

import game_world
from upgrade_shop import UpgradeShop
import common

upgrade_shop = None

def init():
    global upgrade_shop
    upgrade_shop = UpgradeShop(common.player)
    game_world.add_object(upgrade_shop, 1)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, get_canvas_height() - event.y
            print(f"Mouse Clicked at: ({x}, {y})")
            upgrade_shop.handle_click(x, y)



def update():
    game_world.update()
    game_world.handle_collision()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.remove_object(upgrade_shop)

def pause():
    pass

def resume():
    pass
