from constants import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width=BLOCK.height, height=BLOCK.height, grid_number="5"):
        pygame.sprite.Sprite.__init__(self)
        self.assets = ASSETS.blocks
        self.image = self.assets.get_frame()
        self.image = pygame.transform.smoothscale(self.image, (BLOCK.width, BLOCK.height))
        # self.color = color

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.width = width
        self.height = height

        self.vspeed = 0
        self.hspeed = 0
        self.move_range = 20

    def update(self):
        self.rect.y += self.vspeed
        self.rect.x += self.hspeed

    def set_image(self, img, width=BLOCK.width, height=BLOCK.height):
        self.image = pygame.image.load(img)
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height

    def reset_image(self, width=BLOCK.width, height=BLOCK.height):
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height

