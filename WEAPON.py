import pygame as pg
from pygame.locals import *
import random as r
import numpy as np

from ENGINE import EngineFunc
from ANIMATION import MeleeHit
from OBJECT import Object

engine = EngineFunc()

class Weapon(Object):
	def __init__(self,x,y,damage,width,height,player,filename):
		super().__init__(x=player.x, y=player.y,filename=filename, width=width, height=height)
		pg.sprite.Sprite.__init__(self)
		self._damage = np.int16(damage)
		self.player = player
	def update(self):
		try:
			self.rect.center = (self.player.rect.centerx,self.player.rect.centery)
		except AttributeError:
			pass
	@property
	def damage(self):
		return self._damage
	@damage.setter
	def damage(self, damage):
		self._damage = damage


		

class MeleeWeapon(Weapon):
	def __init__(self,player,width,height,damage,filename):
		super().__init__(player=player,width=width,height=height,damage=damage,filename=filename,x=player.x,y=player.y)
	def spawn_hit(self, direction, groups, npcs):
		match direction:
			case 'left':
				return MeleeHit((self.player.rect.centerx - 120, self.player.rect.centery - 10), groups, -180, self.player, npcs)
			case 'right':
				return MeleeHit((self.player.rect.centerx + 120, self.player.rect.centery), groups, 0, self.player, npcs)
			case 'top':
				return MeleeHit((self.player.rect.centerx, self.player.rect.centery - 120), groups, 90, self.player, npcs)
			case 'bottom':
				return MeleeHit((self.player.rect.centerx, self.player.rect.centery + 120), groups, -90, self.player, npcs)


class Fists(MeleeWeapon):
	def __init__(self,player):
		super().__init__(player,width=95,height=30,damage=10, filename='')

class Bat(MeleeWeapon):
	def __init__(self,player):
		super().__init__(player, filename='materials/weapon/melee/bat/bat.png', width=130,height=40,damage=30)