from pico2d import *


class Wall:
    def __init__(self, left, top, right, bottom):
        # 좌상단, 우하단 좌표를 중심점과 크기로 변환
        self.x = (left + right) // 2
        self.y = (top + bottom) // 2
        self.width = right - left
        self.height = top - bottom

        # 원본 좌표도 저장 (필요시)
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def draw(self):
        pass

    def update(self):
        pass

    def get_bb(self):
        return (self.left, self.bottom, self.right, self.top)

    def handle_collision(self, group, other):
        pass