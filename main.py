import arcade
from src.settings import *
from src.world import World


def main():
    World(W, H, "Bouncy Bullet", vsync=True, resizable=True, fullscreen=False)
    arcade.run()


if __name__ == "__main__":
    main()
