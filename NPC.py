import pygame as pg
import random as r
from pygame.locals import *
from ENGINE import EngineFunc, Object, Entity
import math
import numpy as np

engine = EngineFunc()

class NPC(Entity):
	def __init__(self, x,y,hp,speed,damage,filename,width,height,name, groups):
		super().__init__(x=x,y=y,filename=filename,width=width,height=height,hp=hp, groups=groups)
		self._speed = np.int32(speed)
		self._damage = np.int16(damage)
		
		self._width = np.int32(width)
		self._height = np.int32(height)
		
		self.model = engine.get_image(filename, self._width, self._height).convert_alpha()
		self.rect = self.model.get_rect(center=(self._x,self._y))
		self._name = name

	def spawn_model(self,screen):
		return screen.blit(self.model, self.rect)

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
	def hp(self):
		return self._hp

	@hp.setter
	def hp(self,hp):
		self._hp = hp
	@property
	def damage(self):
		return self._damage
	





class Pig(NPC):
	def __init__(self,x,y):
		super().__init__(x,y,hp=40, speed=4, damage=1, filename="materials/npc/pig/pig.png", width=100, height=100, name='pig')
	def move_idle(self):
		moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
		step = moves[r.randint(0, 3)]
		self.rect.x += step[0] * self._speed
		self.rect.y += step[1] * self._speed
	def __del__(self):
		engine.play_sound('materials/npc/pig/sound/death.mp3')