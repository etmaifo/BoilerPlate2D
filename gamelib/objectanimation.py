import pygame

class SimpleAnimation(object):
    def __init__(self, image_list, speed):
        self.frames = image_list * speed
        self.frames.sort()
        self.frame_index = 0
        self.numberofframes = len(self.frames)

    def get_frame(self):
        return self.frames[self.frame_index]

    def update(self):
        self.frame_index += 1
        if self.frame_index >= self.numberofframes:
            self.frame_index = 0