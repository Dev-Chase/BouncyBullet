from src.settings import *
import arcade
from pyglet.math import Vec2
from pyglet.window import key

from src.player import Player
from src.enemy import Enemy
# from src.bullet import avg, vec2_from


class PlayView(arcade.View):
    def __init__(self, window):
        super().__init__(window)

        # Creating a Collision Box the Size of the Window for Checks
        self.window_rect = {
            "left": (Vec2(0, window.height), Vec2()),
            "right": (Vec2(window.width, window.height), Vec2(window.width, 0)),
            "down": (Vec2(0, 0), Vec2(window.width, 0)),
            "up": (Vec2(0, window.height), Vec2(window.width, window.height))
        }

        # Initializing Sprites
        self.player = Player()
        self.enemy = Enemy()
        self.bullet = None
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

        # Resetting the Window Rect
        self.window_rect["left"] = (Vec2(0, window.height), Vec2())
        self.window_rect["right"] = (Vec2(window.width, window.height), Vec2(window.width, 0))
        self.window_rect["down"] = (Vec2(0, 0), Vec2(window.width, 0))
        self.window_rect["up"] = (Vec2(0, window.height), Vec2(window.width, window.height))

        # TEMP
        # Resetting Temporary Enemy
        self.enemy.set_position(50, window.height-90)
        self.enemy.bullet_list.clear()

        # Clearing Wall list
        self.walls.clear()
        self.walls.append(self.test_rect)

        # Making sure the Game Doesn't Start off as Paused
        self.is_paused = False

    # Creating a Function to Run Every Frame when the Game isn't Paused
    def update_play(self, window, dt: float):
        # Resizing the Cameras
        self.sprite_camera.resize(window.width, window.height)
        self.hud_camera.resize(window.width, window.height)

        # Updating the Cameras with the New Sizes
        self.sprite_camera.update()
        self.hud_camera.update()

        # Resetting the Window Rect
        self.window_rect["left"] = (
            Vec2(self.sprite_camera.position.x, self.sprite_camera.position.y + window.height),
            Vec2(self.sprite_camera.position.x, self.sprite_camera.position.y)
        )
        self.window_rect["right"] = (
            Vec2(self.sprite_camera.position.x + window.width, self.sprite_camera.position.y + window.height),
            Vec2(self.sprite_camera.position.x + window.width, self.sprite_camera.position.y))
        self.window_rect["down"] = (Vec2(self.sprite_camera.position.x, self.sprite_camera.position.y),
                                    Vec2(self.sprite_camera.position.x + window.width, self.sprite_camera.position.y))
        self.window_rect["up"] = (Vec2(self.sprite_camera.position.x, self.sprite_camera.position.y + window.height),
                                  Vec2(self.sprite_camera.position.x + window.width,
                                       self.sprite_camera.position.y + window.height))

        # Calling the Player Update Function
        self.player.update(window, self.walls, dt)
        self.enemy.update(window, self.window_rect, self.walls, self.player, self.sprite_camera, dt)

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
        self.enemy.bullet_list.draw()
        self.walls.draw()
        self.enemy.draw()
        self.player.list.draw()

        # TEMP
        # Drawing some Text to Visualise where the Player is
        arcade.draw_text('Testing testing testing',
                         W,
                         0,
                         font_name='Arial',
                         font_size=18,
                         anchor_x='right', anchor_y='bottom')

    # Updating and Drawing the Pause Menu every Frame when the Game is Paused
    def update_pause_menu(self, window):
        # Resizing the Cameras
        self.sprite_camera.resize(window.width, window.height)
        self.hud_camera.resize(window.width, window.height)

        # Updating the Cameras with the New Sizes
        self.sprite_camera.update()
        self.hud_camera.update()

        # Using the HUD Camera to Draw the Pause Menu
        self.hud_camera.use()

        # Drawing the Pause Menu
        arcade.draw_rectangle_filled(window.width // 2, window.height // 2, window.width // 7 * 4,
                                     window.height // 7 * 3, colours['lightblue'])
        self.pause_btn.draw()

        # Un Pausing if the Space Key was Pressed
        if window.keyboard[key.SPACE]:
            self.update_pause_img(Vec2(self.pause_btn.width // 2, window.height - self.pause_btn.height // 2),
                                  "./assets/pause_button.png")
            self.is_paused = False

    # Creating a Function to Update the Pause Button with a New Image
    def update_pause_img(self, pos: Vec2, file_path: str):
        self.pause_btn.texture = arcade.load_texture(file_path)
        self.pause_btn.position = pos

    # Creating a Function to Run when a Mouse Button is Clicked
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.pause_btn.collides_with_point((x, y)):
            if self.is_paused:
                self.update_pause_img(Vec2(self.pause_btn.width // 2, self.window.height - self.pause_btn.height // 2),
                                      "./assets/pause_button.png")
            else:
                self.update_pause_img(Vec2(self.window.width // 2, self.window.height // 2),
                                      "./assets/pause_button.png")
            self.is_paused = not self.is_paused
