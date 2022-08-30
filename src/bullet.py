from src.settings import *
import arcade
from pyglet.math import Vec2
from math import cos, sin


# Creating a Utility Function to Convert a Union into a Vector2
def vec2_from(union) -> Vec2:
    return Vec2(union[0], union[1])


# Creating a function to get a List of the Lines from a Sprites Hit Box
# Order= Bottom, Right, Top, Left
def gen_sprite_lines(sprite):
    list_arr = []
    hit_box = sprite.get_adjusted_hit_box()

    for i in range(len(hit_box)):
        if not i+1 == len(hit_box):
            next_i = i+1
        else:
            next_i = 0

        list_arr.append([
            vec2_from(hit_box[i]),
            vec2_from(hit_box[next_i])
        ])

    return list_arr


# Creating a function to Check for Line Collisions
def line_to_line(line_1, line_2) -> bool:
    ua_1 = ((line_2[1].x - line_2[0].x) * (line_1[0].y - line_2[0].y) - (line_2[1].y - line_2[0].y) * (
                line_1[0].x - line_2[0].x))
    ua_2 = ((line_2[1].y - line_2[0].y) * (line_1[1].x - line_1[0].x) - (line_2[1].x - line_2[0].x) * (
                         line_1[1].y - line_1[0].y))
    if ua_1 and ua_2:
        u1 = ua_1/ua_2
    else:
        u1 = 0
    ub_1 = ((line_1[1].x - line_1[0].x) * (line_1[0].y - line_2[0].y) - (line_1[1].y - line_1[0].y) * (
                line_1[0].x - line_2[0].x))
    ub_2 = ((line_2[1].y - line_2[0].y) * (line_1[1].x - line_1[0].x) - (line_2[1].x - line_2[0].x) * (
                line_1[1].y - line_1[0].y))
    if ub_1 and ub_2:
        u2 = ub_1/ub_2
    else:
        u2 = 0

    # if uA and uB are between 0-1, lines are colliding
    if 0 <= u1 <= 1 and 0 <= u2 <= 1:
        return True

    return False


# Creating a Function to Check for Collision against a Polygon
def line_to_poly(line, poly_lines):
    for poly_line in poly_lines:
        if line_to_line(line, poly_line):
            return True

    return False


class Bullet(arcade.Sprite):
    def __init__(self, og_sprite, start: tuple = (0, 0), speed: int = 0, target: tuple = (0, 0)):
        super().__init__("./assets/bullet.png", center_x=start[0], center_y=start[1])
        # Setting the Speed
        self.speed = speed
        self.test = 0

        # Making the Bullet aim towards the Target
        self.face_point(arcade.rotate_point(target[0], target[1], start[0], start[1], 90))

        # Moving the Bullet forward Until it's not hitting its Original Sprite
        while arcade.check_for_collision(self, og_sprite):
            self.center_x += cos(self.radians) * 1
            self.center_y += sin(self.radians) * 1

        # Moving the Sprite at the Assigned Speed in the Designated Direction
        self.forward(speed)

    # Creating a function to Tell if the Bullet is Dead(will never be on screen again)
    def is_dead(self, window_rect):
        # Getting the Projection Line of the Bullet
        proj_line = (vec2_from(self.position), Vec2(self.center_x + cos(self.radians) * WORLD_WIDTH,
                                                    self.center_y + sin(self.radians) * WORLD_HEIGHT))

        # If there is no Collision with the Window Rect then return True
        return not line_to_poly(proj_line, window_rect.values())

    # Creating a function to Run Every Frame
    def update(self, window, window_rect, walls, player, enemy, camera, dt: float):
        # Moving the Bullet
        self.center_x += self.change_x * dt * FPS
        self.center_y += self.change_y * dt * FPS

        # Bouncing the Bullet when it Collides with the Shield
        if arcade.check_for_collision(self, player.shield):
            self.bounce(player.shield)

        # Bouncing the Bullet when it collides with a in the Next Frame
        for wall in arcade.check_for_collision_with_list(self, walls):
            self.bounce(wall)
            break

        # Killing off the Memory the Bullet takes when it is considered "dead"
        if arcade.check_for_collision(self, player) or arcade.check_for_collision(self, enemy) or self.is_dead(
                window_rect):
            self.kill()
            del self

    # Creating a function to Bounce the Current Bullet off of a given Sprite on a Collision
    def bounce(self, sprite, order=(1, 3, 2, 0)):
        # Getting the Bullets Hit Box and the line along its projection axis
        hit_box = self.get_adjusted_hit_box()
        collision_line = [vec2_from(avg(hit_box[3], hit_box[0])), vec2_from(avg(hit_box[1], hit_box[2]))]

        # Getting the Hit Box lines of the Sprite that the Bullet Collided with
        sprite_collision_lines = gen_sprite_lines(sprite)

        # Creating Variables that will help keep the Code more DRY
        extra_angle = 0
        do = True

        # Looping through the Indexes in the Order Specified in the Function Call.
        # Doing it this way Prioritizes the Sides which the Caller wants.
        for i in order:
            if line_to_line([vec2_from(tup) for tup in sprite_collision_lines[i]], collision_line):
                extra_angle = (i-1)*90
                break
        # Else Runs if the Loop finishes without Breaking
        else:
            do = False

        # Bouncing the Bullet in the Right direction if Necessary
        if do:
            # Bouncing Bullet
            self.angle = sprite.angle + extra_angle
            self.change_x = 0
            self.change_y = 0
            self.forward(self.speed)
