import pygame as pg
from pygame.locals import *
import random as r
import numpy as np

from ENGINE import EngineFunc
from ANIMATION import MeleeHit
from PARTICLE import Bullet
from OBJECT import Object

engine = EngineFunc()

class Weapon(Object):
	def __init__(self,x, y, damage, width, height, player, filename, sounds):
		super().__init__(x=player.x, y=player.y, filename=filename,
						 width=width, height=height)

		pg.sprite.Sprite.__init__(self)
		self._damage = np.int16(damage)
		self._player = player

		self.sounds = sounds # 0 - shoot, 1 - hit (for melee), 2 - reload(for firearms)
		self.filename = filename


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
	def __init__(self, damage, width, height, player, filename, sounds):
		super().__init__(x=player.x, y=player.y, damage=damage, 
						width=width,height=height, player=player, filename=filename, sounds=sounds)

	def spawn_hit(self, direction, groups, npcs):

		engine.play_sound(self.sounds[0])

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
	def __init__(self, damage, width, height, player, filename, sounds,
	magazine_volume, delay_before_shoots, ammo_type):
		super().__init__(x=player.x, y=player.y, damage=damage, 
						width=width,height=height, player=player, filename=filename, sounds=sounds)

		# (magazine_volume, delay_before_shoots, ammo_type)

	def shoot(self, pos, groups):
		Bullet(self._player, pos, groups)
		engine.play_sound(self.sounds[0])


# Melee

class Fists(MeleeWeapon):
	def __init__(self, player):
		super().__init__(damage=5, width=40, height=30, player=player, filename='',
		sounds=('materials/weapon/melee/hit.mp3',
		'materials/weapon/melee/hands/sound/direct_hit.mp3'))

class Bat(MeleeWeapon):
	def __init__(self,player):
		super().__init__(damage=8, width=130, height=40, player=player, filename='materials/weapon/melee/bat/bat.png',
		sounds=('materials/weapon/melee/hit.mp3',
		'materials/weapon/melee/hands/sound/direct_hit.mp3'))


# Firearms


class Tokarev(FireArms):
	def __init__(self, player):
		super().__init__(damage = 3, 
						width = 70,height = 30, player = player,
						filename = 'materials/weapon/firearms/tokarev_pistol/tokarev.png',
						sounds=('materials/weapon/firearms/tokarev_pistol/sound/shoot.mp3',
						'', 'materials/weapon/firearms/tokarev_pistol/sound/reload.mp3'),
						magazine_volume = 8, 
						delay_before_shoots = 2, 
						ammo_type = 'pistol')
	
