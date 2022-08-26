from src.settings import *
import arcade
from src.player import Player
from pyglet.math import Vec2


class PlayView(arcade.View):
    def __init__(self, window):
        super().__init__(window)

        # Initializing Sprites
        self.player = Player()
        self.test_rect = arcade.Sprite("./assets/wall.png", center_x=0, center_y=0)

        # Initializing Sprite Lists
        self.walls = arcade.SpriteList(use_spatial_hash=True)

        # Creating Cameras
        self.sprite_camera = arcade.Camera(window.width, window.height, window)
        self.hud_camera = arcade.Camera(window.width, window.height, window)

    def setup(self, window):
        # Changing the Size of the Cameras
        self.sprite_camera.resize(window.width, window.height)
        self.hud_camera.resize(window.width, window.height)

        # Resetting the Player Position
        self.player.set_position(window.width // 2, window.height // 2)

        # Clearing Wall list
        self.walls.clear()
        self.walls.append(self.test_rect)

    def update_play(self, keyboard, mouse_pos, window, dt):
        # Resizing the Cameras
        self.sprite_camera.resize(window.width, window.height)
        self.hud_camera.resize(window.width, window.height)

        # Updating the Cameras
        self.sprite_camera.update()
        self.hud_camera.update()

        # Clearing the View
        window.clear()

        # Uncomment the following line when you implement the HUD
        # self.hud_camera.use()
        # Drawing the HUD goes here

        # Using the Sprites Camera to Draw all the Sprites
        self.sprite_camera.use()

        # Calling the Player Update Function
        self.player.update(keyboard, mouse_pos, Vec2(window.width, window.height), self.walls, dt)

        # Updating the Sprite Camera to Center the Player
        self.sprite_camera.move_to(
            Vec2(self.player.center_x - window.width // 2, self.player.center_y - window.height // 2), CAMERA_SPEED)
        self.sprite_camera.update()
        self.sprite_camera.use()

    def draw(self):
        # Drawing the Sprites
        self.walls.draw()
        self.player.list.draw()
        # Drawing some Text to Visualise where the Player is
        arcade.draw_text('Testing testing testing',
                         W,
                         0,
                         font_name='Arial',
                         font_size=18,
                         anchor_x='right', anchor_y='bottom')