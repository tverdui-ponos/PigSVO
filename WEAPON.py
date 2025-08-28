import pygame as pg
from pygame.locals import *
import random as r
import numpy as np
import time as t




from ENGINE import EngineFunc, start_time
from ANIMATION import MeleeHit
from PARTICLE import Bullet
from OBJECT import Object

engine = EngineFunc()



EMPTY_SOUND = 'materials/weapon/firearms/empty.mp3'



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

		self.rect.center = (self._player.rect.centerx, self._player.rect.centery)

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

	def spawn_hit(self, direction, groups):

		engine.play_sound(self.sounds[0])

		size = (self._width + self._height) * 1.2

		match direction:
			
			case 'left':
				return MeleeHit((self._player.rect.centerx - size, self._player.rect.centery), groups, -180, self._player)

			case 'right':
				return MeleeHit((self._player.rect.centerx + size, self._player.rect.centery), groups, 0, self._player)

			case 'top':
				return MeleeHit((self._player.rect.centerx, self._player.rect.centery - size), groups, 90, self._player)

			case 'bottom':
				return MeleeHit((self._player.rect.centerx, self._player.rect.centery + size ), groups, -90, self._player)
		
		



class FireArms(Weapon):
	def __init__(self, damage, width, height, player, filename, sounds,
	magazine_volume, delay_before_shoots, ammo_type):
		super().__init__(x=player.x, y=player.y, damage=damage, 
						width=width,height=height, player=player, filename=filename, sounds=sounds)

		# (magazine_volume, delay_before_shoots, ammo_type)

		self._delay = False

		self._delay_before_shoots = delay_before_shoots

		self._magazine_volume = magazine_volume

		self.ammo = magazine_volume

	def shoot(self, pos, groups):
		if self._delay == False and self.ammo > 0:
			self._delay = True 
			self.start_time = t.time()
			Bullet(self._player, pos, groups)
			engine.play_sound(self.sounds[0])
			self.ammo -= 1
		elif self.ammo <= 0:
			engine.play_sound(EMPTY_SOUND)
	
	def update(self):
		if self._delay == True:
			current_delay = t.time() - self.start_time
			if current_delay >= self._delay_before_shoots:
				self._delay = False

		self.rect.center = (self._player.rect.centerx, self._player.rect.centery)

# Melee

class Fists(MeleeWeapon):
	def __init__(self, player):
		super().__init__(damage=5, width=40, height=30, player=player, filename='',
		sounds=('materials/weapon/melee/hit.mp3',
		'materials/weapon/melee/hands/sound/direct_hit.mp3'))

class Bat(MeleeWeapon):
	def __init__(self,player):
		super().__init__(damage=7, width=130, height=40, player=player, filename='materials/weapon/melee/bat/bat.png',
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
						delay_before_shoots = 0.3, 
						ammo_type = 'pistol')
	
