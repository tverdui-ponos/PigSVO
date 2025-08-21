import pygame as pg
from pygame.locals import *
import random as r
import numpy as np

from ENGINE import EngineFunc
from ANIMATION import MeleeHit
from OBJECT import Object

engine = EngineFunc()

class Weapon(Object):
	def __init__(self,x, y, damage, width, height, player, filename):
		super().__init__(x=player.x, y=player.y, filename=filename,
						 width=width, height=height)

		pg.sprite.Sprite.__init__(self)
		self._damage = np.int16(damage)
		self._player = player
	def update(self):
		try:
			self.rect.center = (self._player.rect.centerx, self._player.rect.centery)
		except AttributeError:
			pass
	@property
	def damage(self):
		return self._damage
	@damage.setter
	def damage(self, damage):
		self._damage = damage



		

class MeleeWeapon(Weapon):
	def __init__(self, damage, width, height, player, filename):
		super().__init__(x=player.x, y=player.y, damage=damage, 
						width=width,height=height, player=player, filename=filename )

	def spawn_hit(self, direction, groups, npcs):

		size = (self._width + self._height) * 1.2

		match direction:
			
			case 'left':
				return MeleeHit((self._player.rect.centerx - size, self._player.rect.centery), groups, -180, self._player, npcs)

			case 'right':
				return MeleeHit((self._player.rect.centerx + size, self._player.rect.centery), groups, 0, self._player, npcs)

			case 'top':
				return MeleeHit((self._player.rect.centerx, self._player.rect.centery - size), groups, 90, self._player, npcs)

			case 'bottom':
				return MeleeHit((self._player.rect.centerx, self._player.rect.centery + size ), groups, -90, self._player, npcs)



class FireArms(Weapon):
	def __init__(self, damage, width, height, player, filename, characteristic):
		super().__init__(x=player.x, y=player.y, damage=damage, 
						width=width,height=height, player=player, filename=filename,
						characteristic=characteristic)
						
	self._characteristic = characteristic
		




# Melee

class Fists(MeleeWeapon):
	def __init__(self, player):
		super().__init__(damage=5, width=40, height=30, player=player, filename='')

class Bat(MeleeWeapon):
	def __init__(self,player):
		super().__init__(damage=8, width=130, height=40, player=player, filename='materials/weapon/melee/bat/bat.png')


# Firearms


