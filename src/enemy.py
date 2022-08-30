from src.settings import *
import arcade
from pyglet.math import Vec2
from pyglet.window import key

from src.bullet import Bullet


class Enemy(arcade.Sprite):
    def __init__(self, pos=Vec2()):
        super().__init__("./assets/enemy.png", center_x=pos.x, center_y=pos.y)

        # Creating a Sprite List to Hold all of the Bullets that the Bullet Fires
        self.bullet_list = arcade.SpriteList()

        # Creating Attributes to Slow down How fast Bullets Fire in Succession
        self.time_waited = 0
        self.slow_down = FPS//4

    # Creating a Function to Fire a Bullet to Create a new Bullet
    def fire(self, target):
        self.bullet_list.append(Bullet(self, self.position, BULLET_SPEED, target))

    # Creating a Function to Run Every Frame
    def update(self, window, window_rect, walls, player, player_cam, dt):
        # Setting a Timer to Make Sure the Bullets are Fired with a delay
        self.time_waited += 1

        # Firing a Bullet if the Delay is Over and the User Pressed Space
        if window.keyboard[key.SPACE] and self.time_waited > self.slow_down:
            self.time_waited = 0
            self.fire(player.position)

        # Updating all of the Bullets in self.bullet_list
        for bullet in self.bullet_list:
            bullet.update(window, window_rect, walls, player, self, player_cam, dt)
