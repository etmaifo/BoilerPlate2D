import pygame

class Camera(object):
    def __init__(self, camera_rect, width, height):
        self.camera_func = camera_rect
        self.rect = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):
        self.rect = self.camera_func(self.rect, target.rect)
