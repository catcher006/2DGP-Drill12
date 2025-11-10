import random
import math
import game_framework
import game_world

from pico2d import *

from arrow import Arrow

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = 1280 // 2, 1024 // 2
        self.load_images()
        self.frame = random.randint(0, 9)
        self.face_dir = random.choice([-1,1])

        self.arrow = Arrow()
        game_world.add_object(self.arrow, 2)

        # 여기를 채우시오.
        self.t = 0.0
        self.sx, self.sy = self.x, self.y
        self.distance = math.sqrt((self.arrow.x - self.x) ** 2 + (self.arrow.y - self.y) ** 2)

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        # 여기를 채우시오.
        if self.t < 1.0:
            self.t += game_framework.frame_time * RUN_SPEED_PPS / self.distance
            self.x = (1 - self.t) * self.sx + self.t * self.arrow.x
            self.y = (1 - self.t) * self.sy + self.t * self.arrow.y
        else:
            self.x, self.y = self.arrow.x, self.arrow.y # 도착점에 장확히 맞추기
            self.t = 0.0
            self.arrow.reset_position() # 새로운 목표 지점 설정
            self.sx, self.sy = self.x, self.y # 시작 지점 갱신
            self.distance = math.sqrt((self.arrow.x - self.x) ** 2 + (self.arrow.y - self.y) ** 2)



    def draw(self):
        if self.x > self.arrow.x:
            Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass


    def handle_collision(self, group, other):
        pass




