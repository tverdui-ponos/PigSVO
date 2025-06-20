import pygame as pg
import pygame_gui as pgg
from pygame.locals import *
import os
import random as r
import time as t



pg.init()
pg.font.init()
pg.display.set_caption('слышишь выскачем')


timing = t.time()

FLAG = False

def timer(seconds, flag):
	global timing
	while t.time() - timing > seconds:
		timing = t.time()
		print(f'{seconds} sec')
		return 0


class EngineFunc:
	def __init__(self):


		self._image_libraly = {}
		self._sound_library = {}
		self._music_library = {}


	
	def get_image(self,path, i_x, i_y):
		image = self._image_libraly.get(path)
		try:
			if image == None:
				image = pg.image.load(path)
				image = pg.transform.scale(image, (i_x, i_y))
				self._image_libraly[path] = image
			return image
		except:
			print(f'Error loading image {path}')

	
	def play_sound(self,path):
		sound = self._sound_library.get(path)
		try:
			if sound == None:
				sound = pg.mixer.Sound(path)
				self._sound_library[path] = sound
			sound.play()
		except:
			print(f'Error loading sound {path}')


	
	def play_music(self,path,mode):
		music = self._music_library.get(path)
		music = pg.mixer.music.load(path)
		self._music_library[path] = music
		pg.mixer.music.play(mode)
		pg.mixer.music.set_volume(0.1)


engine = EngineFunc()

class Object(pg.sprite.Sprite):
	def __init__(self,x,y,filename,width,height):
		pg.sprite.Sprite.__init__(self)

		self._x = x
		self._y = y
		self._width = width
		self._height = height
		if filename != None:
			self.model = engine.get_image(filename, self._width, self._height).convert_alpha()
			self.rect = self.model.get_rect(center=(self._x, self._y))
	def spawn_model(self,screen):
		return screen.blit(self.model, self.rect)
	def __getattr__(self, atr):
		return atr
	@property
	def width(self):
		return self._width
	@property
	def height(self):
		return self._height
	@width.setter
	def width(self, width):
		self._width = width
	@height.setter
	def width(self, height):
		self._height = height



class Interface:
	def __init__(self,x,y,width,height):
		#self.Font = self.get_font('arial',50)
		self._x = x
		self._y = y
		self._width = width
		self._height = height
		self._cached_text = {}
		self._cached_fonts = {}

	def make_font(self,fonts, size):
		available = pg.font.get_fonts()
		choices = map(lambda x:x.lower().replace(' ', ''), fonts)
		for choice in choices:
			if choice in available:
				return pg.font.SysFont(choice, size)
		return pg.font.Font(None, size)

	def get_font(self,font_preferences, size):
		key = str(font_preferences) + '|' + str(size)
		font = self._cached_fonts.get(key, None)
		if font == None:
			font = self.make_font(font_preferences, size)
			self._cached_fonts[key] = font
		return font

	def create_text(self,text, fonts, size, color):
		key = '|'.join(map(str, (fonts, size, color, text)))
		image = self._cached_text.get(key, None)
		if image == None:
			font = self.get_font(fonts, size)
			image = font.render(text, True, color)
			self._cached_text[key] = image
		return image

	def __getattr__(self, atr):
		return atr


class Inventory(Interface):
	def __init__(self,x,y,width,height):
		super().__init__(x,y,width,height)
		self.inv = [[],[]]
	def add_weapon(self,weapon,name):
		self.inv[0].append(weapon)
		self.inv[1].append(name)
	def choose_weapon(self,ind,weapon):
		del weapon
		engine.play_sound('effects/ammo_pickup.mp3')
		if ind < len(self.inv[0]):
			return self.inv[0][ind]  
		return None


class NPC(pg.sprite.Sprite):
	def __init__(self, x,y,hp,speed,damage,filename,width,height,name):
		pg.sprite.Sprite.__init__(self)
		self._x = x
		self._y = y
		self._hp = hp
		self._speed = speed
		self._damage = damage
		
		self._width = width
		self._height = height
		
		self.model = engine.get_image(filename, self._width, self._height).convert_alpha()
		self.rect = self.model.get_rect(center=(self._x,self._y))
		self._name = name

	def spawn_model(self,screen):
		return screen.blit(self.model, self.rect)

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self,x):
		self._x = x
	@property
	def y(self):
		return self._y
	@y.setter
	def y(self,y):
		self._y = y
	
	@property
	def speed(self):
		return self._speed

	@property
	def width(self):
		return self._width
	@property
	def height(self):
		return self._height

	@property
	def hp(self):
		return self._hp

	@hp.setter
	def hp(self,hp):
		self._hp = hp
	

class Player(NPC):
	def __init__(self,x,y):
		super().__init__(x,y,hp=100, speed=10, damage=100, filename="player/serega.png", width=150, height=100, name='player')
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



class Pig(NPC):
	def __init__(self,x,y):
		super().__init__(x,y,hp=40, speed=4, damage=10, filename="pig/pig.png", width=100, height=100, name='pig')
	def move_idle(self):
		moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
		step = moves[r.randint(0, 3)]
		self.rect.x += step[0] * self._speed
		self.rect.y += step[1] * self._speed
	def __del__(self):
		print('dead')
		engine.play_sound('pig/death.mp3')

class Weapon(Object):
	def __init__(self,damage,width,height,player,filename,x,y):
		super().__init__(filename=filename, width=width, height=height, x=player.x, y=player.y)
		self._damage = damage
		self._player = player
		self._x = self._player.x
		self._y = self._player.y
		self._width = width
		self._height = height

	def update_position(self):
		try:
			self.rect.center = (self._player.rect.centerx,self._player.rect.centery)
		except AttributeError:
			pass

		

class MeleeWeapon(Weapon):
	def __init__(self,player,width,height,damage,filename):
		super().__init__(player=player,width=width,height=height,damage=damage,filename=filename,x=player.x,y=player.y)
		self._player = player
		self.hit_right = engine.get_image('weapon/hit_right.png', self._width , self._height).convert_alpha()
		self.hit_right_rect = self.hit_right.get_rect()
		self.hit_left = engine.get_image('weapon/hit_left.png', self._width , self._height).convert_alpha()
		self.hit_left_rect = self.hit_left.get_rect()
		self.hit_bottom = engine.get_image('weapon/hit_bottom.png', self._width , self._height).convert_alpha()
		self.hit_bottom_rect = self.hit_bottom.get_rect()
		self.hit_top = engine.get_image('weapon/hit_top.png', self._width , self._height).convert_alpha()
		self.hit_top_rect = self.hit_top.get_rect()
		self.is_attacking = False
		self.attack_frame = 0
		self.attack_animation = None
	def spawn_hit_right(self,screen):
		self.hit_right = pg.transform.scale(self.hit_right, (int(self._width * 1.2),int(self._height * 2.5)))
		self.hit_right_rect.topleft = (self._player.rect.x + (self._width * 1.4), self._player.rect.y + (self._height * 2.5) / 10)
		self._player.attack_rect = self.hit_right_rect
		self.is_attacking = True
		self.attack_animation = 'right'
		return screen.blit(self.hit_right, self.hit_right_rect)
	def spawn_hit_left(self,screen):
		self.hit_left = pg.transform.scale(self.hit_left, (int(self._width * 1.2),int(self._height * 2.5)))
		self.hit_left_rect.topleft = (self._player.rect.x - (self._width * 1.4), self._player.rect.y - (self._height * 2.5) / 10)
		self._player.attack_rect = self.hit_left_rect
		self.is_attacking = True
		self.attack_animation = 'left'
		return screen.blit(self.hit_left,  self.hit_left_rect)
	def spawn_hit_top(self,screen):
		self.hit_top = pg.transform.scale(self.hit_top, (int(self._width * 1.2),int(self._height * 2.5)))
		self.hit_top_rect.topleft = (self._player.rect.x + (self._height * 2.5) / 10 , self._player.rect.y - (self._width * 1.1))
		self._player.attack_rect = self.hit_top_rect
		self.is_attacking = True
		self.attack_animation = 'top'
		return screen.blit(self.hit_top,self.hit_top_rect)
	def spawn_hit_bottom(self,screen):
		self.hit_bottom = pg.transform.scale(self.hit_bottom, (int(self._width * 1.2),int(self._height * 2.5)))
		self.hit_bottom_rect.topleft = (self._player.rect.x - (self._height * 2.7) / 10 , self._player.rect.y + (self._width * 1.1))
		self._player.attack_rect = self.hit_bottom_rect
		self.is_attacking = True
		self.attack_animation = 'bottom'
		return screen.blit(self.hit_bottom, self.hit_bottom_rect)

class Fists(MeleeWeapon):
	def __init__(self,player):
		super().__init__(player,width=95,height=30,damage=10, filename=None)
		#self.model = pg.Surface((40, 40), pg.SRCALPHA)
		#self.rect = self.model.get_rect(center=(player.x, player.y))

class Bat(MeleeWeapon):
	def __init__(self,player):
		super().__init__(player, filename='weapon/bat/bat.png', width=130,height=40,damage=30)


class Particle(pg.Rect):
	def __init__(self, location):
		self.width = 4
		self.height = 4
		self.center = location
	def update(self):
		self.centery -= 3
		self.centerx += r.randint(-2,2)

class SpawnerParticle(Particle):
	def __init__(self):
		self.particles = []
	def spawn(self,amount, location,type,screen):
		if type == "blood":
			self.color = [(247,8,17),(247,24,8),(247,8,17), (164,12,18), (135,9,10)]
		for i in range(amount):
			self.particles.append(Particle(location))
	def update(self,screen):
		for x in self.particles:
			x.update()
			if x.centery<0:
				self.particles.remove(x)
			else:
				pg.draw.rect(screen, self.color[r.randint(0,4)], x)


class Game:
	def __init__(self):
	
		#Engine Init
		self.screen = pg.display.set_mode((1020,640))
		self.interface = Interface(0,0,0,0)
		self.clock = pg.time.Clock()
		self.timer = 0
		pg.time.set_timer(pg.USEREVENT, 100, False)
		self.start_ticks=pg.time.get_ticks()
		self.done = False
		pg.mouse.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)
		self.time_delta = self.clock.tick(60)/1000.0
		self.particles = SpawnerParticle()
		# Object
		self.player = Player(100,100)

		self.objects = []
		self.collide_objects = []
		self.pigs = []
		self.bat = Bat(self.player)
		self.background = engine.get_image('grass.png', 1024,640)
		self.hp_text = self.interface.create_text(f'HP:{self.player.hp}','arial',60,(0,0,0))
		engine.play_music('music/ambient1.mp3', -1)
	def handle_events(self):

		for event in pg.event.get():
			###

			if event.type == pg.QUIT:
				self.done = True
			# Attack Animation
			try:
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 1:
						if pg.mouse.get_pos()[0] < self.player.rect.x and pg.mouse.get_pos()[1]> self.player.rect.y:
							self.player.weapon.spawn_hit_left(self.screen)
							engine.play_sound('weapon/hit.mp3')
						elif pg.mouse.get_pos()[0] > self.player.rect.x and pg.mouse.get_pos()[1]> self.player.rect.y and pg.mouse.get_pos()[0]>pg.mouse.get_pos()[1]:
							self.player.weapon.spawn_hit_right(self.screen)
							engine.play_sound('weapon/hit.mp3')
						elif pg.mouse.get_pos()[1] < self.player.rect.y and pg.mouse.get_pos()[0] > self.player.rect.x:
							self.player.weapon.spawn_hit_top(self.screen)
							engine.play_sound('weapon/hit.mp3')
						elif pg.mouse.get_pos()[1] > self.player.rect.y and pg.mouse.get_pos()[0] > self.player.rect.x:
							self.player.weapon.spawn_hit_bottom(self.screen)
							engine.play_sound('weapon/hit.mp3')
			except AttributeError:
				pass
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_x:
					self.pigs.append(Pig(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]))
					print('x')
				if event.key == pg.K_f:
					self.collide_objects.append(Object(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1],(f'object/trees/tree{r.randint(1,6)}.png'), 200,300))

				if event.key == pg.K_0:
					self.player.weapon = self.player.inventory.choose_weapon(0, None)
					self.particles.spawn(100, (100,500), 'blood', self.screen)
					
				if event.key == pg.K_1:
					self.player.weapon = self.player.inventory.choose_weapon(1, None)



			#Ai pig
			for _pig in self.pigs:
				if event.type == pg.USEREVENT:
					self.timer += 1
					if self.timer > 10:
						_pig.move_idle()
					if self.timer > 40:
						engine.play_sound(f'pig/pig_idle{r.randint(1,3)}.ogg')
						self.timer = 0
	def update(self):
		self.player.update_weapon_position()
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
		if pressed[pg.K_w]:
			self.player.rect.y -= self.player.speed
		if pressed[pg.K_s]:
			self.player.rect.y += self.player.speed
		if pressed[pg.K_a]:
			self.player.rect.x -= self.player.speed
		if pressed[pg.K_d]:
			self.player.rect.x += self.player.speed

		# Death Logic
		for _pig in self.pigs:
			if _pig.hp <= 0:
				engine.play_sound('pig/death.mp3')
				self.pigs.remove(_pig)
				del _pig
					
	def collusion(self):
			# Pig and Player
			try:
				for _pig in self.pigs:
					if self.player.rect.colliderect(_pig.rect):
						self.player.hp -= 1
			except:
				pass
			# Object collide
			for _obj in self.collide_objects:
				if self.player.rect.colliderect(_obj.rect):
					if _obj.rect.x >= self.player.rect.x:
						self.player.rect.x -= self.player.speed
					elif _obj.rect.y <= self.player.rect.y:
						self.player.rect.y += self.player.speed
					elif _obj.rect.y >= self.player.rect.y:
						self.player.rect.y -= self.player.speed
					elif _obj.rect.x >= self.player.rect.x:
						self.player.rect.x += self.player.speed
			# Melee attack and pig
			try:
				for _pig in self.pigs:
					if self.player.attack_rect.colliderect(_pig.rect) and self.player.weapon.is_attacking == True:
						_pig.hp -= self.player.weapon._damage
						engine.play_sound('weapon/hands/sound/direct_hit.mp3')
						engine.play_sound(f'pig/pig_idle{r.randint(1,3)}.ogg')
			except:
				pass
	def render(self):
		# Background
		self.screen.blit(self.background, (0,0))
		
		# Object
		if self.collide_objects:
			for _obj in self.collide_objects:
				_obj.spawn_model(self.screen)
		# Character
		for _pig in self.pigs:
			_pig.spawn_model(self.screen)
		self.player.spawn_model(self.screen)
		
		self.particles.update(self.screen)
		# Render attack animation
		try:
			if self.player.weapon.is_attacking == True:

				if self.player.weapon.attack_animation == "right":
					self.player.weapon.spawn_hit_right(self.screen)
					self.player.attack_rect = None
				elif self.player.weapon.attack_animation == "left":
					self.player.weapon.spawn_hit_left(self.screen)
					self.player.attack_rect = None
				elif self.player.weapon.attack_animation == "top":
					self.player.weapon.spawn_hit_top(self.screen)
					self.player.attack_rect = None
				elif self.player.weapon.attack_animation == "bottom":
					self.player.weapon.spawn_hit_bottom(self.screen)
					self.player.attack_rect = None
		except AttributeError:
			pass
		# HUD
		self.hp_text = self.interface.create_text(f'HP:{self.player.hp}','arial',60,(0,0,0))
		self.screen.blit(self.hp_text, (10,10))
		# Update Display
		pg.display.flip()

	def run(self):
		while not self.done:
			self.handle_events()
			self.collusion()			
			self.update()
			self.render()
			self.clock.tick(60)
			print( self.pigs,self.collide_objects, self.player.inventory.inv, self.player.weapon)

if __name__ == "__main__":
	game = Game()
	game.run()
	pg.quit()
