from assets import *
from pygame import *


pygame.init()
"""
Global constants
"""

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class FilesPath(object):
    def __init__(self):
        self.path = ''

    def get_path(self, absolute_path, filename):
        return os.path.join(absolute_path, filename)

FILES = FilesPath()

# Screen dimensions
class SCREEN(object):
    width = 1024
    height = 576

# Camera
CAMERA_SLACK = 20

# Block
class BLOCK(object):
    width = 32
    height = 32

# Player
class PLAYER(object):
    width = 40
    height = 49
    speed = 8
    jump_speed = -15


# World
class WORLD(object):
    gravity = 1

class ASSETS(object):
    player = PlayerAsset(os.path.join("img", "player.png"), os.path.join("img", "player.txt"))
    blocks = BlockAssets(os.path.join("img", "blocks.png"), os.path.join("img", "blocks.txt"))
