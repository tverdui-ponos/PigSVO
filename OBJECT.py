import pygame as pg
import numpy as np
from ENGINE import EngineFunc

engine = EngineFunc()


class Object(pg.sprite.Sprite):
	def __init__(self,x,y,filename,width,height, *groups):
		if groups:
			super().__init__(groups)
		self._x = np.int32(x)
		self._y = np.int32(y)
		self._width = np.int32(width)
		self._height = np.int32(height)
		if filename != None:
			self.image = engine.get_image(filename, self._width, self._height).convert_alpha()
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
	def hp(self, hp):
		self._hp = hp
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


class Money(Object):
	def __init__(self, x,y, groups):
		super().__init__(x, y, 'materials/effects/money/bitcoin.png', 50, 50, groups)

		self._obstacle_sprites = groups[1]
		
	def update(self):
		collide = pg.sprite.spritecollide(self,self._obstacle_sprites,False)
		if collide:
			for sprite in collide:
				if hasattr(sprite, 'money'):
					sprite.money += 1
					engine.play_sound('materials/effects/money/sound/pickup_money.mp3')
					self.kill()