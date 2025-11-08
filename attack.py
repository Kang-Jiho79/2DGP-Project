from pico2d import *
import game_world
import game_framework

player_attack_animation = (
    (0,0,42,33), (42,0,40,33), (82,0,40,33), (122,0,40,33)
)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Attack:
    image = None

    def __init__(self, x=400, y=300, face_dir=1, player = None):
        if Attack.image == None:
            Attack.image = load_image('resource/player/player_attack.png')
        self.x, self.y = x, y
        self.face_dir = face_dir
        self.frame = 0
        self.player = player

    def update(self):
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        if self.frame >= len(player_attack_animation):
            game_world.remove_object(self)
            self.player.end_attack()

    def draw(self):
        frame_data = player_attack_animation[int(self.frame)]

        # 방향에 따른 오프셋과 회전 각도 설정
        offset_distance = 30  # 플레이어로부터 떨어뜨릴 거리

        if self.face_dir == 0:  # down
            effect_x = self.x
            effect_y = self.y - offset_distance
            angle = -90
        elif self.face_dir == 1:  # right
            effect_x = self.x + offset_distance
            effect_y = self.y
            angle = 0
        elif self.face_dir == 2:  # up
            effect_x = self.x
            effect_y = self.y + offset_distance
            angle = 90
        elif self.face_dir == 3:  # left
            effect_x = self.x - offset_distance
            effect_y = self.y
            angle = 0

        # 플레이어 캐릭터 그리기
        if self.face_dir == 3:  # left
            self.image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                                         angle, 'h',
                                                         effect_x, effect_y, 25,
                                                         50)
        else:
            self.image.clip_composite_draw(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                                                         angle, '',
                                                         effect_x, effect_y, 25,
                                                         50)
