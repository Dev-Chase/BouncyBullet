from src.settings import *
import arcade
from src.shield import Shield
from math import atan2, degrees, radians, sin, cos
from pyglet.math import Vec2
from pyglet.window import key


class Player(arcade.Sprite):
    def __init__(self, pos=Vec2(0, 0)):
        self.list = arcade.SpriteList(capacity=2)
        super().__init__("./assets/player.png", center_x=pos.x, center_y=pos.y)
        self.list.append(self)
        self.shield = Shield(Vec2(pos.x, pos.y+self.height//2+15))
        self.list.append(self.shield)
        self.distance_from_center = self.shield.center_y-self.center_y

    def update(self, keyboard, mouse_pos, window_size, walls, dt):
        self.change_x = ((keyboard[key.RIGHT] or keyboard[key.D])-(keyboard[key.LEFT] or keyboard[key.A]))*PLAYER_SPEED
        self.change_y = ((keyboard[key.UP] or keyboard[key.W])-(keyboard[key.DOWN] or keyboard[key.S]))*PLAYER_SPEED

        # Applying Vertical Movement
        self.move(0, self.change_y, dt)
        self.shield.move(0, self.change_y, dt)

        # Applying Vertical Collision
        for wall in arcade.check_for_collision_with_list(self, walls):
            if self.change_y < 0:
                moved = self.bottom-wall.top
                self.bottom = wall.top
            else:
                moved = self.top-wall.bottom
                self.top = wall.bottom
            self.change_y = 0
            self.shield.move(0, -moved, 1/FPS)

        # Applying Horizontal Movement
        self.move(self.change_x, 0, dt)
        self.shield.move(self.change_x, 0, dt)

        # Applying Horizontal Collision
        for wall in arcade.check_for_collision_with_list(self, walls):
            if self.change_x < 0:
                moved = self.left-wall.right
                self.left = wall.right
            else:
                moved = self.right-wall.left
                self.right = wall.left
            self.change_x = 0
            self.shield.move(-moved, 0, 1 / FPS)
            
        offs_y = ((self.center_y - (self.center_y-window_size.y//2)) - mouse_pos.y)
        offs_x = ((self.center_x - (self.center_x-window_size.x//2)) - mouse_pos.x)
        self.shield.angle = -1 * degrees(atan2(offs_x, offs_y))

        # Moving the Shield Center Along with the Rotation
        self.shield.center_y = (self.center_y + cos(radians(-1 * self.shield.angle)) * self.distance_from_center)
        self.shield.center_x = (self.center_x + sin(radians(-1 * self.shield.angle)) * self.distance_from_center)

        # Applying Shield Collision
        for wall in walls:
            if arcade.check_for_collision(wall, self.shield):
                # Creating the Vector of which the Player will move if there is a collision
                move_x = 0
                move_y = 0

                # TODO: do individual checks to see if the shield is on either side of player body
                # Changing the Direction the Player should Move to get away from the Wall
                if abs(self.shield.bottom - wall.top) < min(
                        [abs(self.shield.top - wall.bottom), abs(self.shield.right - wall.left),
                         abs(self.shield.left - wall.right)]):
                    move_y = .01
                elif abs(self.shield.top - wall.bottom) < min(
                        [abs(self.shield.bottom - wall.top), abs(self.shield.right - wall.left),
                         abs(self.shield.left - wall.right)]):
                    move_y = -.01
                elif abs(self.shield.right - wall.left) < min(
                        [abs(self.shield.bottom - wall.top), abs(self.shield.top - wall.bottom),
                         abs(self.shield.left - wall.right)]):
                    move_x = -.01
                else:
                    move_x = .01

                # Moving the Player until there is no Collision
                while arcade.check_for_collision(wall, self.shield):
                    self.move(move_x, move_y, dt)
                    self.shield.move(move_x, move_y, dt)
        # print(self.shield.get_adjusted_hit_box())

    def move(self, vel_x, vel_y, dt):
        self.center_x += vel_x*dt*FPS
        self.center_y += vel_y*dt*FPS
