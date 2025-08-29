import pygame as pg
import random as r

class Particle(pg.Rect):
	def __init__(self, location):
		self.width = 4
		self.height = 4
		self.center = location
	def update(self):
		self.centery -= 3
		self.centerx += r.randint(-2,2)

class SpawnParticle(Particle):
	def __init__(self):
		self.particles = []
	def spawn(self,amount, location,type,screen):
		if type == "blood":
			self.color = [(247,8,17),(247,24,8),(247,8,17), (164,12,18), (135,9,10)]
		for i in range(amount):
			self.particles.append(Particle(location))
	def update(self,screen):
		for x in self.particles:
			x.update()
			if x.centery<0:
				self.particles.remove(x)
			else:
				pg.draw.rect(screen, self.color[r.randint(0,4)], x)
