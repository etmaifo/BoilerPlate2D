import os
import pygame
from levelparser import LevelCreator
from player import Player
from block import Block
from constants import BLOCK

class Level(object):
    def __init__(self):
        self.level_blocks = []
        self.solid_blocks = []

    def convertToSprite(self, x, y, grid_number):
        block = Block(x, y, BLOCK.width, BLOCK.height, grid_number)
        return block

    def parse_level(self):
        for blockTile in self.level_blocks:
            if blockTile[2] > 0:
                block = self.convertToSprite(blockTile[0] * 32, blockTile[1] * 32, blockTile[2])
                self.solid_blocks.append(block)

    def draw(self, surface):
        for block in self.solid_blocks:
            pygame.draw.rect(surface, (2, 19, 19), block.rect)

    def update(self):
        pass


######################################
#
# Extend level class
#
######################################


class StageLevel(Level):
    def __init__(self, filename):
        Level.__init__(self)
        self.assets = LevelCreator(filename)
        self.level_blocks = self.assets.blocks

        self.width = self.assets.width
        self.height = self.assets.height

        self.parse_level()
        self.projectiles = pygame.sprite.Group()
        self.entities = pygame.sprite.OrderedUpdates()
        self.particle_group = pygame.sprite.Group()

        self.player = None

        self.assemble()
        self.intro = True
        self.timer = 0
        self.elapsed = 0

    def assemble(self):
        pX = int(self.assets.players[0].x)
        pY = int(self.assets.players[0].y)
        self.player = Player(pX, pY, color_code="green")

        # Add blocks
        for block in self.solid_blocks:
            self.player.collision_group.add(block)
            self.entities.add(block)

        self.entities.add(self.player)

    def update(self):
        now = pygame.time.get_ticks()/1000.0
        self.elapsed =  now - self.timer

        if self.intro:
            if self.elapsed > 2:
                self.intro = False
        else:
            self.entities.update()

    def play_intro(self):
        pass


class Stage(object):
    def __init__(self):
        """ Stage class with levels """
        self.levels = []
        self.score = 0
        self.level_index = 0

        self.load_files()
        self.level = self.levels[0]

        self.playerDied = False

    def load_files(self):
        """ Loads level files """
        levels = os.listdir(os.path.join("data"))
        for level in levels:
            self.levels.append(StageLevel(os.path.join("data", level)))

    def load_file(self, filename):
        level = self.create_level(filename)
        self.levels.append(level)

    def create_level(self, filename):
        level = StageLevel(filename)
        return level

    def get_level(self, number):
        return self.levels[number-1]  # Number starts at 1

    def get_next(self):
        if self.level_index >= len(self.levels):
            self.level_index = 0

        i = self.level_index + 1
        self.level_index += 1
        return self.levels[i]

    def load_next(self):
        # Fix looping levels ASAP
        self.level_index += 1
        if self.level_index >= len(self.levels):
            self.level_index = 0

        i = self.level_index
        self.level = self.levels[i]

        self.level.timer = pygame.time.get_ticks()/1000.0

    def reload_level(self):
        """ Reloads the level """
        number = self.level_index
        if number < 10:
            number = "0"+str(self.level_index+1)
        number = str(number)

        self.level = self.levels[self.level_index-1]

    def update(self):
        self.playerDied = False
        if self.level.player.foundExit:
            self.load_next()
            self.level.player.foundExit = False

        # if the player falls below the floor they die
        if self.level.player.rect.y > self.level.height:
            self.level.player.alive = False

        if not self.level.player.alive:
            self.reload_level()
            self.playerDied = True
