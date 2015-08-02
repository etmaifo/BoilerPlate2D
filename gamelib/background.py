from constants import *

class Bg(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bg_image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(bg_image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def move(self, target):
        return self.rect.move(target.rect.x - 2, self.rect.y)