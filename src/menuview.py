import arcade
from src.settings import *
from pyglet.math import Vec2

BG_IMAGE = arcade.load_texture("./assets/grass-background.jpg")
MENU_WIDTH = BG_IMAGE.width*2
MENU_HEIGHT = BG_IMAGE.height*3
BG_IMAGE_W = BG_IMAGE.width
BG_IMAGE_H = BG_IMAGE.height


class MenuView(arcade.View):
    def __init__(self, window):
        super().__init__(window)

        # Creating the Attribute that Holds the text that will be displayed on the Menu
        self.text = "Press Space or Click to Start"

        # Creating Background and Foreground Cameras
        self.bg_camera = arcade.Camera(window.width, window.height, window)
        self.fg_camera = arcade.Camera(window.width, window.height, window)

        # Creating Attributes to Control the Position of the Background Camera
        self.bg_animation_start_position = Vec2()
        self.bg_animation_end_position = Vec2()
        self.bg_animation_elapsed_time = 0
        self.bg_animation_duration = 0
        self.bg_animation_percentage_complete = 0
        self.bg_animation_i = 0

        # Creating the List of points the Background Camera will Animate to
        self.bg_animation_points = [
            # Top Left of World
            Vec2(0-(MENU_WIDTH//2), MENU_HEIGHT//2-window.height),
            # Top Right of World
            Vec2(MENU_WIDTH//2-window.width, MENU_HEIGHT//2-window.height),
            # Center of World
            # Vec2(0, 0),
            # Bottom Left of World
            Vec2(0-(MENU_WIDTH//2), 0-(MENU_HEIGHT//2)),
            # Bottom Right of World
            Vec2(MENU_WIDTH//2-window.width, 0-(MENU_HEIGHT//2))
        ]

    def setup(self, text, offs):
        # Resetting the Player Position
        self.text = text
        self.bg_camera.move(Vec2(offs.x, offs.y))
        self.bg_animation_i = 0
        self.set_target(self.bg_camera.position,
                        self.bg_animation_points[self.bg_animation_i],
                        MENU_CAMERA_SPEED-self.bg_animation_elapsed_time)

    def update_background(self, window, dt):
        # Resizing the Cameras to Fit the Window
        self.bg_camera.resize(window.width, window.height)
        self.fg_camera.resize(window.width, window.height)

        # Updating the Cameras
        self.bg_camera.update()
        self.fg_camera.update()

        # Updating the Animation Points
        self.bg_animation_points[0] = Vec2(-(MENU_WIDTH // 2), MENU_HEIGHT // 2 - window.height)
        self.bg_animation_points[1] = Vec2(MENU_WIDTH // 2 - window.width, MENU_HEIGHT // 2 - window.height)
        self.bg_animation_points[3] = Vec2(MENU_WIDTH // 2 - window.width, -(MENU_HEIGHT // 2))

        # Clearing the Window
        self.clear()

        # Updating the Position Coordinates
        if self.bg_animation_percentage_complete <= 1:
            self.bg_animation_elapsed_time += dt
            self.bg_animation_percentage_complete = (
                    self.bg_animation_elapsed_time / self.bg_animation_duration)
            new_vec = arcade.lerp_vec(
                (self.bg_animation_start_position.x, self.bg_animation_start_position.y),
                (self.bg_animation_end_position.x, self.bg_animation_end_position.y),
                self.bg_animation_percentage_complete)
            self.bg_camera.move(Vec2(new_vec[0], new_vec[1]))
        else:
            if self.bg_animation_i < len(self.bg_animation_points)-1:
                self.bg_animation_i += 1
            else:
                self.bg_animation_i = 0
            self.set_target(self.bg_camera.position,
                            self.bg_animation_points[self.bg_animation_i],
                            MENU_CAMERA_SPEED)

    def set_target(self, begin, dest, dur):
        self.bg_animation_start_position = begin
        self.bg_animation_end_position = dest
        self.bg_animation_duration = dur
        self.bg_animation_elapsed_time = 0
        self.bg_animation_percentage_complete = 0

    def draw_background(self, window):
        # Drawing the Background on the Background Camera
        self.bg_camera.use()
        for i in range(0-((MENU_WIDTH//BG_IMAGE_W)//2)-1, (MENU_WIDTH//BG_IMAGE_W)//2+1):
            for x in range(0 - ((MENU_HEIGHT // BG_IMAGE_H) // 2)-1, (MENU_HEIGHT // BG_IMAGE_H)//2+1):
                arcade.draw_scaled_texture_rectangle(window.width // 2 + (i * BG_IMAGE_W),
                                                     window.height // 2 + (x * BG_IMAGE_H), BG_IMAGE)

    def draw_foreground(self, window):
        self.fg_camera.use()
        arcade.draw_rectangle_filled(window.width // 2, window.height // 2, window.width // 7 * 4,
                                     window.height // 7 * 3, colours['lightblue'])
        arcade.draw_text(self.text,
                         window.width // 2,
                         window.height // 2,
                         font_name="Arial",
                         font_size=18,
                         anchor_x="center", anchor_y="center")

    def on_resize(self, width, height):
        #  Updating the Background Animation
        self.set_target(self.bg_animation_start_position, self.bg_animation_points[self.bg_animation_i],
                        MENU_CAMERA_SPEED - self.bg_animation_elapsed_time)
