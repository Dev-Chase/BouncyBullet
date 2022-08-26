from src.settings import *
import arcade
from pyglet.math import Vec2


class Shield(arcade.Sprite):
    def __init__(self, pos=Vec2(0, 0)):
        super().__init__("./assets/shield.png", center_x=pos.x, center_y=pos.y)
        # self.vertices =

    def move(self, vel_x, vel_y, dt):
        self.center_x += vel_x*dt*FPS
        self.center_y += vel_y*dt*FPS
