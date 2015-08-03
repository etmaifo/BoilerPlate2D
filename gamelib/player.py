import pygame
from pygame import *
from constants import PLAYER, ASSETS, WORLD
from worldobject import Movable
try:
    import pygame.mixer as mixer
except:
    import android.mixer as mixer


class Player(Movable):
    def __init__(self, x, y, color_code, width = PLAYER.width, height = PLAYER.height):

        Movable.__init__(self, x, y, color_code, width, height)
        mixer.init()

        self.assets = ASSETS.player
        self.color_code = color_code
        self.image = self.assets.get_idle_frames(color_code)[0]
        self.image = pygame.transform.smoothscale(self.image, (PLAYER.width, PLAYER.height))

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

        self.carrying_weapon = False
        self.foundExit = False
        self.alive = True

        self.collision_group = pygame.sprite.Group()

        self.cool_down = 30

        self.idle_frames = self.assets.get_idle_frames(self.color_code)
        self.frames = self.assets.get_walk_frames(self.color_code)

        # Sounds
        #self.footstep = mixer.Sound("sounds/step_1.ogg")
        #self.footstep.set_volume(0.1)

    def get_distance(self, frames):
        self.distance_moved += PLAYER.speed
        if self.distance_moved > len(frames) * PLAYER.speed:
            self.distance_moved = 0

    def handleEvents(self, event):
        self.load_frames()
        self.load_idle_frames()

        if event.type == KEYDOWN:
            if event.key == K_i and not self.jumping: # FIX DOUBLE JUMP ASAP
                self.vspeed = PLAYER.jump_speed

        if event.type == KEYUP:
            if event.key == K_a:
                self.hspeed = 0
            elif event.key == K_d:
                self.hspeed = 0

        if event.type == MOUSEBUTTONUP:
            self.hspeed = 0

    def update(self):
        self.load_frames()
        self.load_idle_frames()
        self.cool_down -= 1

        if self.jumping:
            pass

        key = pygame.key.get_pressed()

        if key[K_s]:
            self.hspeed = 0

        elif key[K_a]:
            if self.rect.x <= 0:
                self.hspeed = 0
            else:
                self.hspeed = -PLAYER.speed
                self.direction = 'left'
                if not self.jumping:
                    self.animate_movement(self.frames, self.direction)

        elif key[K_d]:
            self.hspeed = PLAYER.speed
            self.direction = 'right'
            if not self.jumping:
                self.animate_movement(self.frames, self.direction)
                # self.footstep.play()

        if self.vspeed < 16:
            # apply gravity
            self.vspeed += WORLD.gravity

        self.move(self.hspeed, self.vspeed)

        if self.vspeed == 0:
            self.jumping = False
        else:
            self.jumping = True

        if self.hspeed == 0 and not self.jumping:
            self.animate_idle(self.direction)

    def detect_collision(self, dx, dy):
        tempRect = pygame.Rect(self.rect)
        tempRect.x += dx
        tempRect.y += dy

        for sprite in self.collision_group:
            if tempRect.colliderect(sprite.rect):
                # Check x-axis
                self.rect.x += sprite.hspeed
                if dx > 0 and sprite.vspeed == 0:
                    self.rect.right = sprite.rect.left
                elif dx < 0 and sprite.vspeed == 0:
                    self.rect.left = sprite.rect.right

                # Check y-axis
                if dy > 0:
                    self.rect.bottom = sprite.rect.top
                    self.rect.y += sprite.vspeed

                    # Land on something
                    self.vspeed = 0

                elif dy < 0:
                    self.rect.top = sprite.rect.bottom
                    self.vspeed = 0

                return

        self.rect = pygame.Rect(tempRect)