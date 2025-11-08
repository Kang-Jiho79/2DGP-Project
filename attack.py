from pico2d import *
import game_world
import game_framework

class Attack:
    image = None

    def __init__(self, x=400, y=300, face_dir=1):
        if Attack.image == None:
            Attack.image = load_image('resource/player/player_attack.png')
        self.x, self.y = x, y
        self.face_dir = face_dir
        self.frame = 0