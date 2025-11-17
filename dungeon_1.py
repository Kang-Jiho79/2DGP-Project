from pico2d import *

class Dungeon1:
    def __init__(self):
        self.entry_image = load_image('resource/background/dungeon_1/Dungeon_1_entry.png')
        self.fighting_image = load_image('resource/background/dungeon_1/Dungeon_1_fighting.png')
        self.end_image = load_image('resource/background/dungeon_1/Dungeon_1_end.png')
    def draw(self):
        self.image.clip_composite_draw(0, 0, 1248, 832, 0, '', 640, 360, 1280, 720)

    def update(self):
        pass