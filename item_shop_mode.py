import game_framework
from pico2d import *

import game_world
import village_mode
from item_shop import ItemShop

item_shop_image = None

def init():
    global item_shop_image
    item_shop_image = ItemShop()
    game_world.add_object(item_shop_image, 1)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()



def update():
    game_world.update()
    game_world.handle_collision()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.remove_object(item_shop_image)

def pause():
    pass

def resume():
    pass
