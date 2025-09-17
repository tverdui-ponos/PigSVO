import pygame as pg
import numpy as np
import random as r

from ENGINE import get_image, play_sound

from PARTICLE import BloodParticle, SawdustParticle

#from WEAPON import *

class Object(pg.sprite.Sprite):
	def __init__(self,x,y,filename,width,height, *groups):
		if groups:
			super().__init__(groups)
		self._x = np.int32(x)
		self._y = np.int32(y)
		self._width = np.int32(width)
		self._height = np.int32(height)
		if filename != None:
			self.image = get_image(filename, self._width, self._height).convert_alpha()
			self.rect = self.image.get_rect(center=(self._x, self._y))
	@property
	def x(self):
		return self._x
	@property
	def y(self):
		return self._y
	@property
	def width(self):
		return self._width
	@width.setter
	def width(self, width):
		self._width = width
	@property
	def height(self):
		return self._height
	@height.setter
	def height(self, height):
		self._height = height

class Entity(Object):
	def __init__(self, x, y, filename, width,height,groups,hp):
		super().__init__(x,y,filename,width,height, groups)
		self._hp = np.int16(hp)
	@property
	def hp(self):
		return self._hp
	
	@hp.setter
	def hp(self,hp):
		self._hp = hp
		if self._hp <= 0:
			self.kill()
	@property
	def x(self):
		return self._x
	@x.setter
	def x(self, x):
		self._x = x
	@property
	def y(self):
		return self._y
	@y.setter
	def y(self, y):
		self._y = y


# Entity

class Crate(Entity):
	def __init__(self, x, y, groups):
		super().__init__(x, y, 'materials/map/object/crates/crate.png', 130, 130, groups, 80)
		self._visible_sprites = groups[0]
		self._physical_sprites = groups[1]
		self._obstacle_sprites = groups[2]
		

	def spawn_supplies(self):
		chance = bool(r.randint(0,1))
		if chance:
			Money(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))

	@property
	def hp(self):
		return self._hp
	
	@hp.setter
	def hp(self,hp):
		if self.hp > hp:
			SawdustParticle(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))
		self._hp = hp
		if self._hp <= 0:
			SawdustParticle(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))
			SawdustParticle(self.rect.x, self.rect.y, (self._visible_sprites, self._obstacle_sprites))
			self.spawn_supplies()
			self.kill()











# Pickaple

class Money(Object):
	def __init__(self, x, y, groups):
		super().__init__(x, y, 'materials/effects/money/bitcoin.png', 50, 50, groups)

		self._obstacle_sprites = groups[1]
		
	def update(self):
		collide = pg.sprite.spritecollide(self,self._obstacle_sprites,False)
		if collide:
			for sprite in collide:
				if hasattr(sprite, 'money'):
					sprite.money += 1
					play_sound('materials/effects/money/sound/pickup_money.mp3')
					self.kill()
					break


class WeaponObject(Object):
	def __init__(self, x, y, weapon, groups):
		super().__init__(x, y, weapon.filename, weapon.width, weapon.height, groups)
		self._weapon = weapon
		self._obstacle_sprites = groups[1]

	def update(self):
		collide = pg.sprite.spritecollide(self,self._obstacle_sprites,False)
		if collide:
			for sprite in collide:
				if hasattr(sprite, 'inventory'):
					sprite.inventory.add_weapon(self._weapon, (self._weapon.filename.split('/')[-1]).split('.')[0])
					self.kill()
					break
