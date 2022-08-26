import arcade
from src.settings import *
from pyglet.math import Vec2


class MenuView(arcade.View):
    def __init__(self, window):
        super().__init__(window)

        self.text = "Press Space or Click to Start"

        self.background_camera = arcade.Camera(window.width, window.height, window)
        self.foreground_camera = arcade.Camera(window.width, window.height, window)

    def setup(self, text):
        # Resetting the Player Position
        self.text = text

    def update_background(self, window):
        # Clearing the View
        window.clear()

    def draw_background(self, window):
        # Drawing the Background on the Background Camera
        self.background_camera.use()
        arcade.draw_rectangle_filled(window.width//2, window.height//2, window.width, window.height, colours['lightblue'])

    def draw_foreground(self, window):
        arcade.draw_text(self.text,
                         window.width // 2,
                         window.height // 2,
                         font_name="Arial",
                         font_size=18,
                         anchor_x="center", anchor_y="center")
