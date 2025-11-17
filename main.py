import game_framework
from pico2d import *
import dungeon_1_mode as start_mode

open_canvas(1280, 720)
game_framework.run(start_mode)
close_canvas()