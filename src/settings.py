W = 1000
H = 800
FPS = 60
PLAYER_SPEED = 4
BULLET_SPEED = 14
PLAYER_CAMERA_SPEED = .05
MENU_CAMERA_SPEED = 10
WORLD_WIDTH = 6000
WORLD_HEIGHT = 4000


def avg(a, b):
    return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2


game_state_dict = {
    "menu": 0,
    "setup": 1,
    "play": 2
}

rev_game_state_dict = {
    0: ["menu", "dt"],
    1: ["setup", ""],
    2: ["play", "dt"]
}

# Creating Color Variables
colours = {
    "white": (255, 255, 255),
    "green": (0, 255, 0),
    "blue": (0, 0, 128),
    "red": (255, 0, 0),
    "yellow": (242, 255, 0),
    "black": (0, 0, 0),
    "grey": (117, 117, 116),
    "aqua": (0, 255, 255),
    "lightpink": (255, 182, 193),
    "orange": (255, 153, 0),
    "lightblue": (70, 136, 242),
    "lightgreen": (33, 166, 38),
    "purple": (130, 56, 209)
}
