from src.settings import *
import arcade

from pyglet.math import Vec2
from pyglet.window import key
from pyglet.window import mouse

from src.playview import PlayView
from src.menuview import MenuView


# TODO: Add Enemy Spawning and sort of A.I.
# TODO: Add Art for Player and Shield
# TODO: Add Art for Walls and Background
# TODO: Set fixed world size and borders
# TODO: Add procedural Generation Eventually
class World(arcade.Window):
    def __init__(self, *args, **kwargs):
        # Call the parent class initializer
        super().__init__(*args, **kwargs, enable_polling=True)

        # Setting a minimum size for the Window
        self.set_min_size(600, 400)

        # Initializing Core Attributes
        self.game_state = game_state_dict['menu']
        self.mouse_pos = Vec2()
        self.just_pressed = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "space": False
        }
        self.just_clicked = {
            "left": False,
            "right": False
        }

        # Creating Play and Menu Views
        self.play_view = PlayView(self)
        self.menu_view = MenuView(self)

        # Setting up the Menu View
        self.menu_view.setup("Press Space or Click to Start", Vec2(0, 0))

        # Showing the Menu View
        self.show_view(self.menu_view)

        # Setting the Background Color and then Starting Rendering
        arcade.set_background_color(colours['black'])
        arcade.start_render()

    # Creating a function to run everytime the Game State is Menu
    def update_menu(self, dt):

        # Updating the Background of the Menu View
        self.menu_view.update_background(self, dt)

        # Drawing the Menu View
        self.menu_view.draw_background(self)
        self.menu_view.draw_foreground(self)

        # Checking to See if the User pressed Space or Clicked
        if self.keyboard[key.SPACE] or self.mouse[mouse.LEFT]:
            # Setting up the core Variables with default values
            return game_state_dict['setup']

        return game_state_dict['menu']

    # Creating a function to run when the Game State is Setup
    def update_setup(self):

        # Setting up and Showing the Play View
        self.play_view.setup(self)
        self.show_view(self.play_view)

        # Setting Game State to Play
        return game_state_dict['play']

    # Creating a function to run when the Game State is Play
    def update_play(self, dt):
        # Setting the Game State to End the Game when the F Key is Pressed
        if self.keyboard[key.F]:
            self.clear()
            self.menu_view.setup("Press Space or Click to Restart", Vec2(0, 0))
            self.show_view(self.menu_view)
            return 0

        # Updating/Moving the Sprites when the Game is not Paused
        if not self.play_view.is_paused:
            # Updating and Drawing the Play View when the Game is not Paused
            self.play_view.update_play(self, dt)
            self.play_view.draw(self)
        else:
            # Still Drawing the Play View when the Game is Paused as a Background
            self.play_view.draw(self)

            # Drawing the Pause Menu Overtop of the Play View
            self.play_view.update_pause_menu(self)

        return game_state_dict['play']

    # Creating a function to run every frame
    def on_update(self, dt):
        # Updating the Game State
        self.game_state = eval(
            f"self.update_{rev_game_state_dict[self.game_state][0]}({rev_game_state_dict[self.game_state][1]})")
        for i, key_pressed in self.just_pressed.items():
            if key_pressed:
                self.just_pressed[i] = False

        for i, btn_pressed in self.just_clicked.items():
            if btn_pressed:
                self.just_clicked[i] = False

    # Changing the Coordinates of the Mouse Position every time the Cursor Moves
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pos = Vec2(x, y)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self.mouse_pos = Vec2(x, y)
        
    # Changing the Coordinates of the Mouse Position every time the Mouse leaves the Window and Returns
    def on_mouse_leave(self, x: int, y: int):
        self.mouse_pos = Vec2(x, y)
        
    def on_mouse_enter(self, x: int, y: int):
        self.mouse_pos = Vec2(x, y)

    # Reacting to Mouse Press
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == mouse.LEFT and not self.just_clicked['left']:
            self.just_clicked['left'] = True
        elif button == mouse.RIGHT and not self.just_clicked['right']:
            self.just_clicked['right'] = True

    # Reacting to Keyboard Input
    def on_key_press(self, symbol: int, modifiers: int):
        if (symbol == key.RIGHT or symbol == key.D) and not self.just_pressed['right']:
            self.just_pressed['right'] = True
        elif (symbol == key.LEFT or symbol == key.A) and not self.just_pressed['left']:
            self.just_pressed['left'] = True
        elif (symbol == key.UP or symbol == key.W) and not self.just_pressed['up']:
            self.just_pressed['up'] = True
        elif (symbol == key.DOWN or symbol == key.S) and not self.just_pressed['down']:
            self.just_pressed['down'] = True
        elif symbol == key.SPACE and not self.just_pressed['space']:
            self.just_pressed['space'] = True
