import pygame as pg
import random as r

import numpy as np

from ENGINE import EngineFunc

import functools 

MAX_PARTICLES = 100


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

BLOOD_COLOR = ((255,0,0), (176,0,0), (255,36,0), (72,6,7), (150,0,24))
SAWDUST_COLOR = ((101, 67, 33), (80, 40, 50), (145, 129, 81))


RED = (255,0,0)

particles = []


engine = EngineFunc()

class Particle(pg.sprite.Sprite):
	def __init__(self, x, y, width, height, x_vel, y_vel, color, groups):

		super().__init__(groups)

		self.x = np.int32(x)
		self.y = np.int32(y)


		self.width = width
		self.height = height


		self.velocity = np.array((x_vel, y_vel), dtype=float)

		self.color = color


		self.image = pg.Surface((self.width, self.height))
		self.image.fill(self.color)

		self.rect = self.image.get_rect(center=(self.x, self.y))
	
	def update(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]

		self.width -= 0.1
		self.height -= 0.1

		self.image = pg.Surface((self.width, self.height))
		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.image.fill(self.color)

		if self.width and self.height <= 0:
			self.kill()




class BloodParticle(Particle):
	def __init__(self, x, y, groups):
		super().__init__(x,y, 10, 10, r.uniform(-10.0, 10.0), r.uniform(-10.0, 10.0), BLOOD_COLOR[r.randint(0,4)], groups)


class SawdustParticle(Particle):
	def __init__(self, x, y, groups):
		super().__init__(x,y, 15, 15, r.uniform(-10.0, 10.0), r.uniform(-10.0, 10.0), SAWDUST_COLOR[r.randint(0,2)], groups)





class Bullet(Particle):
	# Direction ONLY is Rect
	def __init__(self, sender, direction, groups):
		x = np.int32(sender.rect.centerx)
		y = np.int32(sender.rect.centery)

		speed = np.int16(30)

		distance = np.array(np.array(direction) - np.array(sender.rect.center))
		
		if engine.length_of_vector(distance) >= 0:

			velocity = engine.normalize_vector(distance)

		super().__init__(x, y, 10, 10, velocity[0] * speed, velocity[1] * speed, YELLOW, groups)

		self._groups = groups
		self._obstacle_sprites = self._groups[1]

		self._sender = sender

	def collision(self):
		for sacrifice in self._obstacle_sprites:
			if self.rect.colliderect(sacrifice.rect):
				if hasattr(sacrifice, 'hp'):
					if sacrifice != self._sender:
						sacrifice.hp -= self._sender.weapon.damage
						self.kill()


	def update(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]

		self.width -= 0.1
		self.height -= 0.1

		self.image = pg.Surface((self.width, self.height))
		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.image.fill(self.color)

		if self.width and self.height <= 0:
			self.kill()
		
		self.collision()



