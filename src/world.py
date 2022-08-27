from src.settings import *
import arcade
from pyglet.math import Vec2
from pyglet.window import key
from pyglet.window import mouse
from src.playview import PlayView
from src.menuview import MenuView


# TODO: Make overlapping pause screen
# TODO: Add Art for Player and Shield
# TODO: Add Art for Walls and Background
# TODO: Use Lerp to Move Menu Background around World Background
# TODO: Set fixed world size and borders
# TODO: Add procedural Generation Eventually
class World(arcade.Window):
    """ Our custom Window Class"""
    def __init__(self, *args, **kwargs):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(*args, **kwargs, enable_polling=True)

        # Setting a minimum size for the Window
        self.set_min_size(600, 400)

        # Initializing Core Attributes
        self.game_state = game_state_dict['menu']
        self.mouse_pos = Vec2()

        # Creating Play and Menu Views
        self.play_view = PlayView(self)
        self.menu_view = MenuView(self)

        # Setting up the Menu View
        self.menu_view.setup("Press Space or Click to Start", Vec2(0, 0))
        # self.play_view.setup(Vec2(self.width, self.height))

        # Showing the Menu View
        self.show_view(self.menu_view)
        # self.show_view(self.play_view)

        # Setting the Background Color and then Starting Rendering
        arcade.set_background_color(colours['black'])
        arcade.start_render()

    # Creating a function to run everytime the Game State is Menu
    def update_menu(self, dt):

        # Updating the Background of the Menu View
        self.menu_view.update_background(dt)

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
        if self.keyboard[key.F]:
            self.clear()
            self.menu_view.setup("Press Space or Click to Restart", Vec2(0, 0))
            self.show_view(self.menu_view)
            return 0

        self.play_view.update_play(self.keyboard, self.mouse_pos, self, dt)
        self.play_view.draw()

        return game_state_dict['play']

    # Creating a function to run every frame
    def on_update(self, dt):
        # Updating the Game State
        self.game_state = eval(
            f"self.update_{rev_game_state_dict[self.game_state][0]}({rev_game_state_dict[self.game_state][1]})")

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
