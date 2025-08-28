import pygame as pg
import random as r
from pygame.locals import *
import math
import numpy as np

from NPC import NPC
from WEAPON import Fists,Bat, Tokarev
from ENGINE import Inventory,EngineFunc
from ANIMATION import *


engine = EngineFunc()

class Player(NPC):
	def __init__(self,x,y,groups):
		super().__init__(x,y,hp=100, speed=10, damage=0, filename="materials/player/serega.png", width=150, height=100,groups=groups)
		
		self._groups = groups

		self._visible_sprites = self._groups[0]
		self._obstacle_sprites = self._groups[2]

		self._weapon = None

		self.money = np.int32(0)

		self.inventory = Inventory((self._visible_sprites, self._obstacle_sprites), self._weapon)

		self.inventory.add_weapon(Fists(self),'Руки')
		#self.inventory.add_weapon(Bat(self),'Бита')
		#self.inventory.add_weapon(Tokarev(self), 'Пистолет Токарева')

	def movement(self):
		button = pg.key.get_pressed()
		if button[pg.K_w]:
			self.rect.y -= self.speed
		if button[pg.K_s]:
			self.rect.y += self.speed
		if button[pg.K_a]:
			self.rect.x -= self.speed
		if button[pg.K_d]:
			self.rect.x += self.speed
	def mouse_event(self,event):

		if self._weapon != None:
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:

					mouse_pos = engine.get_mouse_pos(self._visible_sprites)
					
					groups = (self._visible_sprites, self._obstacle_sprites)

					if hasattr(self._weapon, 'spawn_hit'):
						direction = engine.check_angle(self.rect, mouse_pos)
						npcs = self._groups[3]

						self._weapon.spawn_hit(direction, groups, npcs)	

					elif hasattr(self.weapon, 'shoot'):
						self._weapon.shoot(mouse_pos, groups)

							
	def keyboard_event(self,event):
		if event.type == pg.KEYDOWN:
			match event.key:
				case pg.K_0:
					self._weapon = self.inventory.choose_weapon(0)
				case pg.K_1:
					self._weapon = self.inventory.choose_weapon(1)
				case pg.K_2:
					self._weapon = self.inventory.choose_weapon(2)
				case pg.K_3:
					self._weapon = self.inventory.choose_weapon(3)
				case pg.K_4:
					self._weapon = self.inventory.choose_weapon(4)
				case pg.K_5:
					self._weapon = self.inventory.choose_weapon(5)
				
	def control(self,event):
		#self.movement()
		self.keyboard_event(event)
		self.mouse_event(event)
	def update(self):
		self.movement()
		if self._weapon and hasattr(self.weapon, 'update'):
			self._weapon.update()
	
	@property
	def weapon(self):
		return self._weapon
	@weapon.setter
	def weapon(self,weapon):
		self._weapon = weapon

	