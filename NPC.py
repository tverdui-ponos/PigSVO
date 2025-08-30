import pygame as pg
import random as r
from pygame.locals import *
import math
import numpy as np

from ENGINE import play_sound

from OBJECT import Entity, Money

from PARTICLE import Particle, BloodParticle


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
	

	@property
	def hp(self):
		return self._hp
	
	@hp.setter
	def hp(self,hp):
		if self.hp > hp:
			BloodParticle(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))
		self._hp = hp



class Pig(NPC):
	def __init__(self,x,y,groups):
		super().__init__(x,y,hp=50, speed=4, damage=1, filename="materials/npc/pig/pig.png", width=100, height=100, groups=groups)
		self._visible_sprites = groups[0]
		self._obstacle_sprites = groups[2]
	def update(self):
		pass
	
	@property
	def hp(self):
		return self._hp
	
	@hp.setter
	def hp(self,hp):
		if self.hp > hp:
			BloodParticle(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))
			BloodParticle(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))
			BloodParticle(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))
			BloodParticle(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))
			play_sound(f'materials/effects/blood/bleeding.mp3')
		self._hp = hp
		if self._hp <= 0:
			play_sound('materials/npc/pig/sound/death.mp3')
			Money(self.rect.centerx, self.rect.centery, (self._visible_sprites,self._obstacle_sprites))
			self.kill()