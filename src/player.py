from src.settings import *
import arcade
from pyglet.math import Vec2
from pyglet.window import key
from math import atan2, degrees, radians, sin, cos

from src.shield import Shield


class Player(arcade.Sprite):
    def __init__(self, pos=Vec2(0, 0)):
        super().__init__("./assets/player.png", center_x=pos.x, center_y=pos.y)

        # Initializing the Player Shield Sprite
        self.shield = Shield(Vec2(pos.x, pos.y+self.height//2+15))

        # Creating a Sprite List to Hold the Player and Shield Sprites
        self.list = arcade.SpriteList(capacity=2)

        # Adding the Player and Shield Sprites to the Sprite List
        self.list.append(self)
        self.list.append(self.shield)

        # Creating an Attribute to tell How Far the Shield Center is from the Body Center for Rotation
        self.distance_from_center = self.shield.center_y-self.center_y

    # Creating a Function to Run Every Frame
    def update(self, window, walls, dt):
        # Setting the Play Velocity Attributes
        self.change_x = ((window.keyboard[key.RIGHT] or window.keyboard[key.D]) - (
                    window.keyboard[key.LEFT] or window.keyboard[key.A])) * PLAYER_SPEED
        self.change_y = ((window.keyboard[key.UP] or window.keyboard[key.W]) - (
                    window.keyboard[key.DOWN] or window.keyboard[key.S])) * PLAYER_SPEED

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

        # Finding out How much the Shield should Rotate Based on the Mouse Position
        offs_y = ((self.center_y - (self.center_y-window.height//2)) - window.mouse_pos.y)
        offs_x = ((self.center_x - (self.center_x-window.width//2)) - window.mouse_pos.x)

        # Applying the Rotation
        self.shield.angle = -1 * degrees(atan2(offs_x, offs_y))

        # Moving the Shield Center Along with the Rotation so that the Shield Rotates around the Player
        self.shield.center_y = (self.center_y + cos(radians(-1 * self.shield.angle)) * self.distance_from_center)
        self.shield.center_x = (self.center_x + sin(radians(-1 * self.shield.angle)) * self.distance_from_center)

        # Applying Shield Collision
        for wall in walls:
            if arcade.check_for_collision(wall, self.shield):
                # Creating the Vector of which the Player will move if there is a collision
                move_x = 0
                move_y = 0

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

    # Creating a Utility Function to Move the Player Based on the Velocities Given
    def move(self, vel_x, vel_y, dt):
        self.center_x += vel_x*dt*FPS
        self.center_y += vel_y*dt*FPS
