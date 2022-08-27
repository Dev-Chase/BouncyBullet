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

        # Creating Pause State Attributes
        self.pause_btn = arcade.Sprite("./assets/pause_button.png", center_x=0, center_y=0)
        self.pause_btn.center_x = self.pause_btn.width // 2
        self.pause_btn.center_y = window.height - self.pause_btn.height // 2
        self.is_paused = False

    def setup(self, window):
        # Changing the Size of the Cameras
        self.sprite_camera.resize(window.width, window.height)
        self.hud_camera.resize(window.width, window.height)

        # Resetting the Player Position
        self.player.set_position(window.width // 2, window.height // 2)

        # Clearing Wall list
        self.walls.clear()
        self.walls.append(self.test_rect)

        # Making sure the Game Doesn't Start off as Pausedd
        self.is_paused = False

    def update_play(self, window, dt: float):
        # Resizing the Cameras
        self.sprite_camera.resize(window.width, window.height)
        self.hud_camera.resize(window.width, window.height)

        # Updating the Cameras
        self.sprite_camera.update()
        self.hud_camera.update()

        # Calling the Player Update Function
        self.player.update(window.keyboard, window.mouse_pos, Vec2(window.width, window.height), self.walls, dt)

    def draw(self, window):
        # Clearing the View
        self.clear()

        # Using the HUD Camera to Draw the Stationary Sprites while not Paused
        if not self.is_paused:
            self.hud_camera.use()

            # Drawing the HUD goes here
            self.pause_btn.draw()

        # Using the Sprites Camera to Draw all the Sprites
        self.sprite_camera.use()

        # Updating the Sprite Camera to Center the Player
        self.sprite_camera.move_to(
            Vec2(self.player.center_x - window.width // 2, self.player.center_y - window.height // 2),
            PLAYER_CAMERA_SPEED)
        self.sprite_camera.update()
        self.sprite_camera.use()

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

    # Updating and Drawing the Pause Menu
    def update_pause_menu(self, window):
        self.hud_camera.use()
        arcade.draw_rectangle_filled(window.width // 2, window.height // 2, window.width // 7 * 4,
                                     window.height // 7 * 3, colours['lightblue'])
        self.pause_btn.draw()
        pass

    def update_pause_img(self, pos: Vec2, file_path: str):
        self.pause_btn.texture = arcade.load_texture(file_path)
        self.pause_btn.position = pos

    def on_left_mouse_press(self, x: int, y: int, window):
        if self.pause_btn.collides_with_point((x, y)):
            if self.is_paused:
                self.update_pause_img(Vec2(self.pause_btn.width // 2, window.height - self.pause_btn.height // 2),
                                      "./assets/pause_button.png")
            else:
                self.update_pause_img(Vec2(window.width//2, window.height//2),
                                      "./assets/pause_button.png")
            self.is_paused = not self.is_paused
