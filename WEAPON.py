import pygame as pg
from pygame.locals import *
import random as r
import numpy as np
import time as t




from ENGINE import play_sound
from ANIMATION import MeleeHit
from PARTICLE import Bullet
from OBJECT import Object


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
	def __init__(self, damage, width, height, player, filename, delay_before_hits, sounds):
		super().__init__(x=player.x, y=player.y, damage=damage, 
						width=width,height=height, player=player, filename=filename,
						sounds=sounds)
		self._delay_before_hits = delay_before_hits
		self._delay = False

	
	def hit(self,direction, groups):
		if self._delay == False:
			self.start_time = t.time()
			
			self.spawn_hit(direction, groups)
			self._delay = True



	def spawn_hit(self, direction, groups):

		play_sound(self.sounds[0])

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
		


	def update(self):
		if self._delay == True:
			current_delay = t.time() - self.start_time
			if current_delay >= self._delay_before_hits:
				self._delay = False

		self.rect.center = (self._player.rect.centerx, self._player.rect.centery)
		



class FireArms(Weapon):
	def __init__(self, damage, width, height, player, filename, sounds,
	magazine_volume, delay_before_shoots, ammo_type):
		super().__init__(x=player.x, y=player.y, damage=damage, 
						width=width,height=height, player=player, filename=filename, sounds=sounds)

		# (magazine_volume, delay_before_shoots, ammo_type)

		self._delay = False

		self._delay_before_shoots = delay_before_shoots

		self._magazine_volume = magazine_volume

		self.magazine_ammo = self._magazine_volume

		self.full_ammo = 0

	def fire(self,direction,groups):
		Bullet(self._player, direction, groups)
		play_sound(self.sounds[0])


	def shoot(self, direction, groups):
		if self._delay == False and self.magazine_ammo > 0:
			self._delay = True 
			self.start_time = t.time()
			self.fire(direction,groups)
			self.magazine_ammo -= 1
		elif self.magazine_ammo <= 0:
			play_sound(EMPTY_SOUND)
	
	def reload(self):
		if self.magazine_ammo < self._magazine_volume and self.full_ammo > 0:
			play_sound(self.sounds[2])
			for i in range(self._magazine_volume):
				if self.full_ammo > 0 and self.magazine_ammo < self._magazine_volume:
					self.magazine_ammo += 1
					self.full_ammo -= 1

	


	
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
		delay_before_hits=0.3,
		sounds=('materials/weapon/melee/hit.mp3',
		'materials/weapon/melee/hands/sound/direct_hit.mp3'))

class Bat(MeleeWeapon):
	def __init__(self,player):
		super().__init__(damage=7, width=130, height=40, player=player, filename='materials/weapon/melee/bat/bat.png',
		delay_before_hits=0.5,
		sounds=('materials/weapon/melee/hit.mp3',
		'materials/weapon/melee/hands/sound/direct_hit.mp3'))


# Firearms


class Tokarev(FireArms):
	def __init__(self, player):
		super().__init__(damage = 8, 
						width = 70,height = 30, player = player,
						filename = 'materials/weapon/firearms/tokarev_pistol/tokarev.png',
						sounds=('materials/weapon/firearms/tokarev_pistol/sound/shoot.mp3',
						'', 'materials/weapon/firearms/tokarev_pistol/sound/reload.mp3'),
						magazine_volume = 8, 
						delay_before_shoots = 0.3, 
						ammo_type = 'pistol')




class Mosin(FireArms):
	def __init__(self, player):
		super().__init__(damage = 40, 
						width = 220,height = 70, player = player,
						filename = 'materials/weapon/firearms/mosin/mosin.png',
						sounds=('materials/weapon/firearms/mosin/sound/fire.mp3',
						'', 'materials/weapon/firearms/mosin/sound/reload.mp3'),
						magazine_volume = 6, 
						delay_before_shoots = 0.8, 
						ammo_type = 'pistol')



class Ak47(FireArms):
	def __init__(self, player):
		super().__init__(damage = 10, 
						width = 200,height = 40, player = player,
						filename = 'materials/weapon/firearms/ak47/ak47.png',
						sounds=('materials/weapon/firearms/ak47/sound/shoot.mp3',
						'', 'materials/weapon/firearms/ak47/sound/reload.mp3'),
						magazine_volume = 30, 
						delay_before_shoots = 0.05, 
						ammo_type = 'pistol')
