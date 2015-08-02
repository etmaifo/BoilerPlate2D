import pygame
import sys, os


class Asset(object):
    def __init__(self, spritesheet, spritemap):
        self.spritesheet = pygame.image.load(spritesheet)
        self.textfile = spritemap
        self.sprites = []

    def load_sprites(self):
        info = open(self.textfile, 'r')
        lines = []
        for line in info:
            lines.append(line.split())
        for line in lines:
            sprite = self.get_image(int(line[2]), int(line[3]), int(line[4]), int(line[5])) # 0 0 0 0
            self.sprites.append([line[0], sprite])

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        return image



class PlayerAsset(Asset):
    def __init__(self, spritesheet, spritemap):
        Asset.__init__(self, spritesheet, spritemap)
        self.load_sprites()

    def get_walk_frames(self, color_code):
        walk_frames = [frame[1] for frame in self.sprites if color_code+"_walk" in frame[0]]

        return walk_frames

    def get_idle_frames(self, color_code):
        idle_frames = [frame[1] for frame in self.sprites if color_code+"_stand" in frame[0]]

        return idle_frames

    def get_jump_frames(self, color_code):
        jump_frames = [frame[1] for frame in self.sprites if color_code+"_jump" in frame[0]]

        return jump_frames

    def get_hurt_frames(self, color_code):
        hurt_frames = [frame[1] for frame in self.sprites if color_code+"_hurt" in frame[0]]

        return hurt_frames


class BlockAssets(Asset):
    def __init__(self, spritesheet, spritemap):
        Asset.__init__(self, spritesheet, spritemap)
        self.load_sprites()

    def get_frame(self):
        return self.sprites[0][1]


