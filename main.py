from pico2d import *
from player import Player

def reset_world():
    global world  # 이 줄 추가
    global player
    world = []
    player = Player()
    world.append(player)

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_events(event)  # handle_event -> handle_events로 수정


def update_world():
    for object in world:
        object.update()


def render_world():
    clear_canvas()
    for object in world:
        object.draw()
    update_canvas()


running = True

open_canvas()

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
