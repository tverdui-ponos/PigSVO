import pygame as pg
import random as r
from pygame.locals import *
import math
import numpy as np

from ENGINE import EngineFunc

from OBJECT import Entity, Money


engine = EngineFunc()

class NPC(Entity):
	def __init__(self, x,y,hp,speed,damage,filename,width,height, groups):
		super().__init__(x=x,y=y,filename=filename,width=width,height=height,hp=hp, groups=groups)
		self._speed = np.int32(speed)
		self._damage = np.int16(damage)
	@property
	def x(self):
		return self._x

	@x.setter
	def x(self,x):
		self._x = x
	@property
	def y(self):
		return self._y
	@y.setter
	def y(self,y):
		self._y = y
	
	@property
	def speed(self):
		return self._speed

	@property
	def width(self):
		return self._width
	@property
	def height(self):
		return self._height
	@property
	def damage(self):
		return self._damage
	





class Pig(NPC):
	def __init__(self,x,y,groups):
		super().__init__(x,y,hp=40, speed=4, damage=1, filename="materials/npc/pig/pig.png", width=100, height=100, groups=groups)
		self._visible_sprites = groups[0]
		self._obstacle_sprites = groups[2]
	def move_idle(self):
		moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
		step = moves[r.randint(0, 3)]
		self.rect.x += step[0] * self._speed
		self.rect.y += step[1] * self._speed
	def update(self):
		if self._hp <= 0:
			engine.play_sound('materials/npc/pig/sound/death.mp3')
			Money(self._x, self._y, (self._visible_sprites,self._obstacle_sprites))
			self.kill()