import pygame as pg
import numpy as np

import math

image_libraly = {}
sound_library = {}
music_library = {}



class EngineFunc:

	def get_image(self,path, i_x, i_y):
		image = image_libraly.get(path)
		try:
			if image == None:
				image = pg.image.load(path)
				image = pg.transform.scale(image, (i_x, i_y))
				image_libraly[path] = image
			return image
		except Exception as ex:
			print(f'Error loading image {path}', ex)
			image = image_libraly.get('materials/effects/error.png')
			if image == None:
				image = pg.image.load('materials/effects/error.png')
				image = pg.transform.scale(image, (i_x, i_y))
				image_libraly[path] = image
				return image			

	
	def play_sound(self,path, volume=1.0):
		try:
			sound = sound_library.get(path)
			if sound is None:
				sound = pg.mixer.Sound(path)
				sound_library[path] = sound

			sound.set_volume(volume)
			sound.play()
		except Exception as e:
			print(f'Error loading sound {path}, {e}')
			


	
	def play_music(self,path,mode):
		music = music_library.get(path)
		music = pg.mixer.music.load(path)
		music_library[path] = music
		pg.mixer.music.play(mode)
		pg.mixer.music.set_volume(0.1)
	
	def length_of_vector(self,vector):
		#vector = np.array(vector)
		return np.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))


	def normalize_vector(self, vector):
		vector = np.array(vector)
		return vector / self.length_of_vector(vector)
	
	
	def angle_between_vectors(self,vector1,vector2):
		vector1 = np.array(vector1, dtype=float)
		vector2 = np.array(vector2, dtype=float)

		dx = vector2[0] - vector1[0]
		dy = vector1[1] - vector2[1]

		angle = np.arctan2(dy,dx)
		return np.degrees(angle) % 360
	

	def check_angle(self, vector1, vector2):
		angle = self.angle_between_vectors(vector1, vector2)
		if 0 < angle <= 45 or 338 < angle <= 360:
			return 'right'
		elif 245 < angle <= 337:
			return 'bottom'
		elif 155 < angle <= 244:
			return 'left'
		elif 46 < angle <= 155:
			return 'top'

	
	def get_mouse_pos(self, camera_group):
		
		mouse_pos = pg.mouse.get_pos()
		
		world_mouse_pos = np.array(mouse_pos) + camera_group.offset

		return world_mouse_pos

engine = EngineFunc()



class Collisions:
	def __init__(self, physical_sprites, static_spites, 
	npcs_sprites, friendly_npcs_sprites, enemy_npcs_sprites):

		self._physical_sprites = physical_sprites
		self._static_sprites = static_spites

		self._npcs_sprites = npcs_sprites
		self._friendly_npcs_sprites = friendly_npcs_sprites
		self._enemy_npcs_sprites = enemy_npcs_sprites




	def collision_between_physical_objects(self):
		collision = pg.sprite.groupcollide(self._physical_sprites, self._physical_sprites, False, False)
		for sprite1,sprite_list in collision.items():
			for sprite2 in sprite_list:
				if sprite1 != sprite2:
					direction = engine.check_angle(sprite1.rect, sprite2.rect)
					
					match direction:
						
						case "left":
							sprite1.rect.x += 1
						case "right":
							sprite1.rect.x -= 1
						case "top":
							sprite1.rect.y += 1
						case "bottom":
							sprite1.rect.y -= 1
	

	def collison_betweeen_npc_and_static_objects(self):
		collision = pg.sprite.groupcollide(self._npcs_sprites, self._static_sprites, False, False)
		for sprite1,sprite_list in collision.items():
			for sprite2 in sprite_list:
				direction = engine.check_angle(sprite1.rect, sprite2.rect)
				match direction:
					case "left":
						sprite1.rect.x += sprite1.speed
					case "right":
						sprite1.rect.x -= sprite1.speed
					case "top":
						sprite1.rect.y += sprite1.speed
					case "bottom":
						sprite1.rect.y -= sprite1.speed	
		

	def collusion_between_enemies(self):
		collision = pg.sprite.groupcollide(self._friendly_npcs_sprites, self._enemy_npcs_sprites, False, False)
		for sprite1,sprite_list in collision.items():
			for sprite2 in sprite_list:
				if sprite1 != sprite2:
					sprite1.hp -= sprite2.damage

	
	def collusion(self):
		self.collision_between_physical_objects()
		self.collison_betweeen_npc_and_static_objects()
		self.collusion_between_enemies()


class SortCameraGroup(pg.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pg.display.get_surface()
		self.size = np.array(self.display_surface.get_size()) // 2
		self.offset = pg.math.Vector2()
		
	def custom_draw(self, player, *screen):

		self.offset = player.rect.center - self.size

		camera_rect = pg.Rect(
			self.offset[0], 
			self.offset[1],
			self.display_surface.get_width(),
			self.display_surface.get_height()
		)

		for sprite in self.sprites():
			if sprite.rect.colliderect(camera_rect):
				offset_pos = sprite.rect.topleft - self.offset
				self.display_surface.blit(sprite.image, offset_pos)





class Inventory:
	def __init__(self,groups, weapon):
		self._inv = [[],[]]
		self._visible_sprites = groups[0]
		self._obstacle_sprites = groups[1]
		self.weapon = weapon


	def add_weapon(self,weapon,name):
		self._inv[0].append(weapon)
		self._inv[1].append(name)
	

	def get_name(self):
		if self.weapon:
			for i, weapon in enumerate(self._inv[0]):
				if self.weapon == weapon:
					return self._inv[1][i]

			return "Нету оружия"


	def choose_weapon(self,ind):
		if ind >= len(self._inv[0]):
			return None
		else:
			if self.weapon:
				self.weapon.kill()
			
			self.weapon = self._inv[0][ind]
			

			self._visible_sprites.add(self.weapon)
			self._obstacle_sprites.add(self.weapon)

			engine.play_sound('materials/effects/ammo_pickup.mp3')

			return self.weapon