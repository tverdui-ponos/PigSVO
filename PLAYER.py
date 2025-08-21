import pygame as pg
import random as r
from pygame.locals import *
import math
import numpy as np

from NPC import NPC
from WEAPON import Fists,Bat
from ENGINE import Inventory,EngineFunc
from ANIMATION import *


engine = EngineFunc()

class Player(NPC):
	def __init__(self,x,y,groups):
		super().__init__(x,y,hp=100, speed=10, damage=100, filename="materials/player/serega.png", width=150, height=100,groups=groups)
		self._groups = groups
		self._weapon = None 
		self.inventory = Inventory((self._groups[0], self._groups[2]), self._weapon)
		self.inventory.add_weapon(Fists(self),'Руки')
		self.inventory.add_weapon(Bat(self),'Бита')
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
					direction = engine.check_angle(self.rect, engine.get_mouse_pos(self._groups[0]))
					groups = [self._groups[0],self._groups[2]]
					npcs = self._groups[3]
					match direction:
						case 'left':
							self._weapon.spawn_hit(direction, groups, npcs)
						case 'right':
							self._weapon.spawn_hit(direction, groups, npcs)
						case 'top':
							self._weapon.spawn_hit(direction, groups, npcs)
						case 'bottom':
							self._weapon.spawn_hit(direction, groups, npcs)	
					engine.play_sound('materials/weapon/melee/hit.mp3')
							
	def keyboard_event(self,event):
		if event.type == pg.KEYDOWN:
			match event.key:
				case pg.K_0:
					self._weapon = self.inventory.choose_weapon(0)
				case pg.K_1:
					self._weapon = self.inventory.choose_weapon(1)
				
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

	