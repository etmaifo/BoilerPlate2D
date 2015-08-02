from constants import *
from random import *

class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, width=5, height=3, color=(242, 126, 48)):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((width, height))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.life = 10 + randrange(0, 5)

		self.rect.x = x
		self.rect.y = y

		self.hspeed = choice([-3, 3])
		self.vspeed = randrange(-15, 0)

	def update(self):
		if self.vspeed < 16:
			self.vspeed += GRAVITY

		self.rect.x += self.hspeed
		self.rect.y += self.vspeed

		self.life -= 1

		if self.life <= 0:
			self.kill()
