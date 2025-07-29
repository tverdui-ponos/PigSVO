import numpy as np
import pygame as pg
#import pygame_gui as pgg
from pygame.locals import *
import os
import random as r
import time as t
from WEAPON import *
from PLAYER import *
from NPC import *
from ENGINE import *
from PARTICLE import *
from ANIMATION import *
from MAP import Map
import numpy as np

pg.init()
pg.font.init()
pg.display.set_caption('слышишь выскачем')
#pygame.display.set_icon(pygame.image.load("app.bmp"))


timing = t.time()

FLAG = False

def timer(seconds, flag):
	global timing
	while t.time() - timing > seconds:
		timing = t.time()
		print(f'{seconds} sec')
		return 0





engine = EngineFunc()


class Game:
	def __init__(self):
	
		#Engine Init
		self.screen = pg.display.set_mode((1024,768))
		self.interface = Interface(0,0,0,0)
		self.clock = pg.time.Clock()
		self.timer = 0
		#self.camera = Camera(200,400)
		pg.time.set_timer(pg.USEREVENT, 100, False)
		self.start_ticks=pg.time.get_ticks()
		self.done = False
		pg.mouse.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)
		self.time_delta = self.clock.tick(60)/1000.0
		self.particles = SpawnerParticle()
		self.system_of_collusions = Collisions()
		self.animations = Animation()
		# Object
		self.objects = []
		self.player = Player(100,100)
		
		
		self.phisical_objects = []
		self.collide_objects = []
		self.pigs = []
		self.bat = Bat(self.player)
		self.background = engine.get_image('materials/map/grass.png', 1024,640)
		self.hp_text = self.interface.create_text(f'HP:{self.player.hp}','arial',60,(0,0,0))
		engine.play_music('materials/music/ambient1.mp3', -1)

		self.objects.append(self.player)
		self.map = Map('testmap')
		#self.objects.append(self.background)

	def handle_events(self):

		for event in pg.event.get():
			###

			if event.type == pg.QUIT:					

				self.done = True
			# Keys
			self.player.keys(event,self.screen)

			#Other keys
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_x:
					pig = Pig(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
					self.pigs.append(pig)
					self.objects.append(pig)
				if event.key == pg.K_f:
					#self.collide_objects.append(Object(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1],(f'materials/map/object/trees/tree{r.randint(1,6)}.png'), 200,300))
					self.animations.run_animation([engine.get_image('materials/player/serega.png', 100,100)], 3000, (200,200), self.screen)


			#Ai pig
			for _pig in self.pigs:
				if event.type == pg.USEREVENT:
					self.timer += 1
					if self.timer > 10:
						_pig.move_idle()
					if self.timer > 40:
						engine.play_sound(f'materials/npc/pig/sound/pig_idle{r.randint(1,3)}.ogg')
						self.timer = 0
	def update(self):
		#self.player.update_weapon_position()
		# Sprite melee attack
		try:	
			if self.player.weapon.is_attacking == True:
				self.player.weapon.attack_frame += 1
				if self.player.weapon.attack_frame >= 1:
					self.player.attack_rect = None
				if self.player.weapon.attack_frame >= 5:
					self.player.weapon.is_attacking = False
					self.player.weapon.attack_animation = None
					self.player.weapon.attack_frame = 0
		except AttributeError:
			pass
		# Input
		pressed = pg.key.get_pressed()
		self.player.movement(pressed)

		# Death Logic
		for _pig in self.pigs:
			if _pig.hp <= 0:
				engine.play_sound('materials/npc/pig/sound/death.mp3')
				self.pigs.remove(_pig)
				del _pig
		
		self.camera.update(self.player)
		print(self.camera.camera.topleft)
					
	def collusion(self):
			# Pig and Player
			self.system_of_collusions.collusion_between_enemies(self.pigs, [self.player])
			# Object collide
			self.system_of_collusions.collision_between_physical_object([self.player], self.collide_objects)
			# Melee attack and pig
			try:
				for _pig in self.pigs:
					if self.player.attack_rect.colliderect(_pig.rect) and self.player.weapon.is_attacking == True:
						_pig.hp -= self.player.weapon._damage
						engine.play_sound('materials/weapon/melee/hands/sound/direct_hit.mp3')
						engine.play_sound(f'materials/npc/pig/sound/pig_idle{r.randint(1,3)}.ogg')
			except:
				pass
	def render(self):
		# Background
		#self.screen.blit(self.background, (0,0))
		
		#self.screen.fill((10,20,30))
		
		self.map.run()
		
		# Object
		if self.collide_objects:
			for _obj in self.collide_objects:
				_obj.spawn_model(self.screen)

		# Character
		for _pig in self.pigs:
			_pig.spawn_model(self.screen)
		

		self.player.spawn_model(self.screen)
		
		#for i in self.objects:
			#self.camera.apply(i)
		
		self.particles.update(self.screen)
		# Render attack animation
		try:
			if self.player.weapon.is_attacking == True:

				if self.player.weapon.attack_animation == "right":
					self.player.weapon.spawn_hit(self.screen, 'right')
					self.player.attack_rect = None
				elif self.player.weapon.attack_animation == "left":
					self.player.weapon.spawn_hit(self.screen, 'left')
					self.player.attack_rect = None
				elif self.player.weapon.attack_animation == "top":
					self.player.weapon.spawn_hit(self.screen, 'top')
					self.player.attack_rect = None
				elif self.player.weapon.attack_animation == "bottom":
					self.player.weapon.spawn_hit(self.screen, 'bottom')
					self.player.attack_rect = None
		except AttributeError:
			pass
		# HUD
		self.hp_text = self.interface.create_text(f'HP:{self.player.hp}','arial',60,(0,0,0))
		self.screen.blit(self.hp_text, (10,10))
		pg.draw.line(self.screen, (0,0,0), self.player.rect.center, pg.mouse.get_pos())
		
		
		# Update Display
		pg.display.flip()

	def run(self):
		while not self.done:
			self.handle_events()
			self.collusion()			
			self.update()
			self.render()
			self.clock.tick(60)
			#mouse_pos = pg.mouse.get_pos()

if __name__ == "__main__":
	game = Game()
	game.run()
	pg.quit()
