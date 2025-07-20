import pygame as pg
import random as r
from pygame.locals import *
from NPC import NPC
from INTERFACE import *
from WEAPON import Fists,Bat
import math
import numpy as np



class Player(NPC):
	def __init__(self,x,y):
		super().__init__(x,y,hp=100, speed=10, damage=100, filename="materials/player/serega.png", width=150, height=100, name='player')
		self.inventory = Inventory(10,100, 20, 20)
		self.weapon = None 
		self.inventory.add_weapon(Fists(self),'Руки')
		self.inventory.add_weapon(Bat(self),'Бита')
		self.attack_rect = None
	def update_weapon_position(self):
		if self.weapon and hasattr(self.weapon, 'update_position'):
			self.weapon.update_position()
	def spawn_model(self,screen):
		screen.blit(self.model, self.rect)
		if self.weapon and hasattr(self.weapon ,'model'):
			try:
				screen.blit(self.weapon.model, self.weapon.rect)
			except TypeError:
				pass
	def movement(self,button):
		if button[pg.K_w]:
			self.rect.y -= self.speed
		if button[pg.K_s]:
			self.rect.y += self.speed
		if button[pg.K_a]:
			self.rect.x -= self.speed
		if button[pg.K_d]:
			self.rect.x += self.speed
	def mouse_event(self,event,screen):
			try:
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 1:
						direction = engine.check_angle(self.rect.center, pg.mouse.get_pos())
						match direction:
							case 'left':
								self.weapon.spawn_hit(screen, direction)
							case 'right':
								self.weapon.spawn_hit(screen, direction)
							case 'top':
								self.weapon.spawn_hit(screen, direction)
							case 'bottom':
								self.weapon.spawn_hit(screen, direction)	
						engine.play_sound('materials/weapon/melee/hit.mp3')
							
			except Exception as e:
				print(e)
	def keyboard_event(self,event,screen):
		if event.type == pg.KEYDOWN:
			match event.key:
				case pg.K_0:
					self.weapon = self.inventory.choose_weapon(0, None)
					#self.particles.spawn(100, (100,500), 'blood', self.screen)
				case pg.K_1:
					self.weapon = self.inventory.choose_weapon(1, None)
				
	def keys(self,event,screen):
		self.keyboard_event(event, screen)
		self.mouse_event(event,screen)