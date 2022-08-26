import arcade
from src.settings import *
from pyglet.math import Vec2
import random


class MenuView(arcade.View):
    def __init__(self, window):
        super().__init__(window)

        # Creating the Attribute that Holds the text that will be displayed on the Menu
        self.text = "Press Space or Click to Start"

        # Creating Background and Foreground Cameras
        self.background_camera = arcade.Camera(window.width, window.height, window)
        self.foreground_camera = arcade.Camera(window.width, window.height, window)

        # Creating Attributes to Control the Position of the Background Camera
        self.background_animation_start_position = Vec2()
        self.background_animation_end_position = Vec2()
        self.background_animation_elapsed_time = 0
        self.background_animation_duration = 0
        self.background_animation_percentage_complete = 0
        self.background_animation_i = 0

        # Creating the List of points the Background Camera will Animate to
        self.background_animation_points = [
            # Bottom Left of World
            Vec2(-(WORLD_WIDTH//2), -(WORLD_HEIGHT//2)),
            # Top Left of World
            Vec2(-(WORLD_WIDTH//2), WORLD_HEIGHT//2-window.height),
            # Top Right of World
            Vec2(WORLD_WIDTH//2-window.width, WORLD_HEIGHT//2-window.height),
            # Bottom Right of World
            Vec2(WORLD_WIDTH//2-window.width, -(WORLD_HEIGHT//2)),
            # Center of World
            Vec2(0, 0)
        ]

    def setup(self, text, offs):
        # Resetting the Player Position
        self.text = text
        self.background_camera.move(Vec2(offs.x, offs.y))
        self.background_animation_i = random.randint(0, len(self.background_animation_points) - 1)
        self.set_target(self.background_camera.position,
                        self.background_animation_points[self.background_animation_i],
                        MENU_CAMERA_SPEED)

    def update_background(self, dt):
        # Clearing the Window
        self.clear()

        # Updating the Position Coordinates
        if self.background_animation_percentage_complete <= 1:
            self.background_animation_elapsed_time += dt
            self.background_animation_percentage_complete = (
                self.background_animation_elapsed_time / self.background_animation_duration)
            new_vec = arcade.lerp_vec(
                (self.background_animation_start_position.x, self.background_animation_start_position.y),
                (self.background_animation_end_position.x, self.background_animation_end_position.y),
                self.background_animation_percentage_complete)
            self.background_camera.move(Vec2(new_vec[0], new_vec[1]))
        else:
            self.background_animation_i = random.randint(0, len(self.background_animation_points) - 1)
            while self.background_animation_points[self.background_animation_i] == self.background_camera.position:
                self.background_animation_i = random.randint(0, len(self.background_animation_points)-1)
            self.set_target(self.background_camera.position,
                            self.background_animation_points[self.background_animation_i],
                            MENU_CAMERA_SPEED)

    def set_target(self, begin, dest, dur):
        self.background_animation_start_position = begin
        self.background_animation_end_position = dest
        self.background_animation_duration = dur
        self.background_animation_elapsed_time = 0
        self.background_animation_percentage_complete = 0

    def draw_background(self, window):
        # Drawing the Background on the Background Camera
        self.background_camera.use()
        arcade.draw_rectangle_filled(window.width//2, window.height//2, window.width, window.height, colours['lightblue'])

    def draw_foreground(self, window):
        self.foreground_camera.use()
        arcade.draw_text(self.text,
                         window.width // 2,
                         window.height // 2,
                         font_name="Arial",
                         font_size=18,
                         anchor_x="center", anchor_y="center")

    def on_resize(self, width, height):
        # Resizing the Cameras to Fit the Window
        self.background_camera.resize(width, height)
        self.foreground_camera.resize(width, height)

        # Updating the Cameras
        self.background_camera.update()
        self.foreground_camera.update()

        # Updating the Animation Points
        self.background_animation_points[1] = Vec2(-(WORLD_WIDTH // 2), WORLD_HEIGHT // 2 - height)
        self.background_animation_points[2] = Vec2(WORLD_WIDTH // 2 - width, WORLD_HEIGHT // 2 - height)
        self.background_animation_points[3] = Vec2(WORLD_WIDTH // 2 - width, -(WORLD_HEIGHT // 2))

        #  Updating the Background Animation
        self.set_target(self.background_camera.position, self.background_animation_points[self.background_animation_i],
                        MENU_CAMERA_SPEED-self.background_animation_elapsed_time)
