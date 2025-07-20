import pygame as pg
from ENGINE import *
from pygame.locals import *
import random as r

engine = EngineFunc()

class Weapon(Object):
	def __init__(self,damage,width,height,player,filename,x,y):
		super().__init__(filename=filename, width=width, height=height, x=player.x, y=player.y)
		self._damage = np.int16(damage)
		self._player = player
		self._x = self._player.x
		self._y = self._player.y
		self._width = np.int16(width)
		self._height = np.int16(height)

	def update_position(self):
		try:
			self.rect.center = (self._player.rect.centerx,self._player.rect.centery)
		except AttributeError:
			pass

		

class MeleeWeapon(Weapon):
	def __init__(self,player,width,height,damage,filename):
		super().__init__(player=player,width=width,height=height,damage=damage,filename=filename,x=player.x,y=player.y)
		self._player = player
		self.hit_right = engine.get_image('materials/weapon/melee/hit_right.png', self._width , self._height).convert_alpha()
		self.hit_right = pg.transform.scale(self.hit_right, (int(self._width * 1.2),int(self._height * 2.5)))
		self.hit_right_rect = self.hit_right.get_rect()
		self.hit_left = pg.transform.rotate(self.hit_right, 180)
		self.hit_left = pg.transform.scale(self.hit_left, (int(self._width * 1.2),int(self._height * 2.5)))
		self.hit_left_rect = self.hit_left.get_rect()
		self.hit_bottom = pg.transform.rotate(self.hit_right,-90)
		self.hit_bottom = pg.transform.scale(self.hit_bottom, (int(self._width * 1.2),int(self._height * 2.5)))
		self.hit_bottom_rect = self.hit_bottom.get_rect()
		self.hit_top = pg.transform.rotate(self.hit_right, 90)
		self.hit_top = pg.transform.scale(self.hit_top, (int(self._width * 1.2),int(self._height * 2.5)))
		self.hit_top_rect = self.hit_top.get_rect()
		self.is_attacking = False
		self.attack_frame = 0
		self.attack_animation = None
	def spawn_hit(self, screen, direction):
		match direction:
			case 'left':
				self.hit_left_rect.topleft = (self._player.rect.x - (self._width * 1.4), self._player.rect.y - (self._height * 2.5) / 10)
				self._player.attack_rect = self.hit_left_rect
				self.is_attacking = True
				self.attack_animation = 'left'
				return screen.blit(self.hit_left,  self.hit_left_rect)
			case 'right':
				self.hit_right_rect.topleft = (self._player.rect.x + (self._width * 1.4), self._player.rect.y + (self._height * 2.5) / 10)
				self._player.attack_rect = self.hit_right_rect
				self.is_attacking = True
				self.attack_animation = 'right'
				return screen.blit(self.hit_right, self.hit_right_rect)
			case 'top':
				self.hit_top_rect.topleft = (self._player.rect.x + (self._height * 2.5) / 10 , self._player.rect.y - (self._width * 1.1))
				self._player.attack_rect = self.hit_top_rect
				self.is_attacking = True
				self.attack_animation = 'top'
				return screen.blit(self.hit_top,self.hit_top_rect)
			case 'bottom':
				self.hit_bottom_rect.topleft = (self._player.rect.x - (self._height * 2.7) / 10 , self._player.rect.y + (self._width * 1.1))
				self._player.attack_rect = self.hit_bottom_rect
				self.is_attacking = True
				self.attack_animation = 'bottom'
				return screen.blit(self.hit_bottom, self.hit_bottom_rect)


class Fists(MeleeWeapon):
	def __init__(self,player):
		super().__init__(player,width=95,height=30,damage=10, filename=None)

class Bat(MeleeWeapon):
	def __init__(self,player):
		super().__init__(player, filename='materials/weapon/melee/bat/bat.png', width=130,height=40,damage=30)