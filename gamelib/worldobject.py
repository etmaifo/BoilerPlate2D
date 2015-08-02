from constants import *


class WorldObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.width = width
        self.height = height

        self.vspeed = 0
        self.hspeed = 0

    def update(self):
        pass

    def handleEvents(self):
        pass

    def draw(self):
        pass


class BgObject(WorldObject):
    def __init__(self, x, y, width, height):
        WorldObject.__init__(self, x, y, width, height)

    def update(self):
        pass


class Movable(WorldObject):
    def __init__(self, x, y, color_code, width, height):
        WorldObject.__init__(self, x, y, width, height)

        self.color_code = color_code
        self.assets = ""
        self.scanned_frame = 0
        self.distance_moved = 0
        self.jumping = False
        self.direction = 'right'
        self.idle = True

        self.collision_group = pygame.sprite.Group()
        self.land_group = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()
        self.interaction_group = pygame.sprite.Group()
        self.moveable_group = pygame.sprite.Group()
        self.lock_group = pygame.sprite.Group()
        self.key_group = pygame.sprite.Group()

        self.idle_frames = ""
        self.jump_frames = ""
        self.frames = ""

    def update(self):
        pass

    def move(self, dx, dy):
        if dx != 0:
            self.detect_collision(dx, 0)
        if dy != 0:
            self.detect_collision(0, dy)

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

        for sprite in self.moveable_group:
            if tempRect.colliderect(sprite.rect):
                if dx > 0:
                    self.rect.right = sprite.rect.left
                    sprite.hspeed = self.hspeed
                elif dx < 0:
                    self.rect.left = sprite.rect.right
                    sprite.hspeed = self.hspeed

                if dy > 0:
                    self.rect.bottom = sprite.rect.top
                    self.vspeed = 0
                elif dy < 0:
                    self.rect.top = sprite.rect.bottom
                    self.vspeed = 0

                return

        self.rect = pygame.Rect(tempRect)

    def reset_rect(self):
        self.rect.width = self.image.get_rect()[2]
        self.rect.height = self.image.get_rect()[3]

    def get_distance(self, frames):
        pass

    def animate_movement(self, frames, direction):
        self.get_distance(frames)
        if self.jumping:
            self.image = self.frames[0]
            if direction == 'left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        else:
            if self.scanned_frame >= len(frames):
                self.scanned_frame = 0

            if direction == 'left':
                self.image = frames[self.scanned_frame]
                self.image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
            elif direction == 'right':
                self.image = frames[self.scanned_frame]
                self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

            self.scanned_frame += 1

    def animate_idle(self, direction):
        if self.scanned_frame >= len(self.idle_frames):
            self.scanned_frame = 0

        self.image = self.idle_frames[self.scanned_frame]
        self.scanned_frame += 1

        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.reset_rect()

    def animate_jump(self, direction):
        self.get_jump_image()
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

    def load_frames(self):
        self.frames = self.assets.get_walk_frames(self.color_code)

    def load_idle_frames(self):
        self.idle_frames = self.assets.get_idle_frames(self.color_code)

    def load_jump_image(self):
        self.jump_frames = self.assets.get_jump_frames(self.color_code)