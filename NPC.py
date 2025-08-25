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
	def speed(self):
		return self._speed

	@property
	def damage(self):
		return self._damage
	





class Pig(NPC):
	def __init__(self,x,y,groups):
		super().__init__(x,y,hp=40, speed=4, damage=1, filename="materials/npc/pig/pig.png", width=100, height=100, groups=groups)
		self._visible_sprites = groups[0]
		self._obstacle_sprites = groups[2]
	def update(self):
		self.x + 1
		if self._hp <= 0:
			engine.play_sound('materials/npc/pig/sound/death.mp3')
			Money(self.rect.centerx, self.rect.centery, (self._visible_sprites,self._obstacle_sprites))
			self.kill()