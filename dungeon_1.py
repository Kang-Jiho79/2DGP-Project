from pico2d import *
import time

class Dungeon1:
    def __init__(self):
        self.entry_image = load_image('resource/background/dungeon_1/Dungeon_1_entry.png')
        self.fighting_image = load_image('resource/background/dungeon_1/Dungeon_1_fighting.png')
        self.end_image = load_image('resource/background/dungeon_1/Dungeon_1_end.png')
        # 던전 상태 관리
        self.state = 'entry'
        self.entry_time = time.time()
        self.entry_duration = 3.0

        # 적 카운터
        self.total_enemies = 0
        self.alive_enemies = 0
    def draw(self):
        if self.state == 'entry':
            self.entry_image.clip_composite_draw(0, 0, 1248, 832, 0, '', 640, 360, 1280, 720)
        elif self.state == 'fighting':
            self.fighting_image.clip_composite_draw(0, 0, 1248, 832, 0, '', 640, 360, 1280, 720)
        elif self.state == 'end':
            self.end_image.clip_composite_draw(0, 0, 1248, 832, 0, '', 640, 360, 1280, 720)

    def update(self):
        current_time = time.time()

        # entry에서 fighting으로 자동 전환
        if self.state == 'entry':
            if current_time - self.entry_time >= self.entry_duration:
                self.state = 'fighting'
                print("전투 시작!")

        # fighting에서 end로 자동 전환 (모든 적 처치 시)
        elif self.state == 'fighting':
            if self.alive_enemies <= 0 and self.total_enemies > 0:
                self.state = 'end'
                print("던전 클리어!")

    def set_enemy_count(self, count):
        """던전 모드에서 적 수를 설정"""
        self.total_enemies = count
        self.alive_enemies = count

    def enemy_killed(self):
        """적이 죽었을 때 호출"""
        if self.alive_enemies > 0:
            self.alive_enemies -= 1
            print(f"적 처치! 남은 적: {self.alive_enemies}")

    def is_fighting_time(self):
        """전투 시간인지 확인 (적 소환 타이밍)"""
        return self.state == 'fighting'

    def is_cleared(self):
        """던전 클리어 여부"""
        return self.state == 'end'

    def get_state(self):
        """현재 상태 반환"""
        return self.state