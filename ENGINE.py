import pygame as pg
import numpy as np


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

	
	def play_sound(self,path):
		sound = sound_library.get(path)
		try:
			if sound == None:
				sound = pg.mixer.Sound(path)
				sound_library[path] = sound
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
		return math.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))


	def normalize_vector(self, vector):
		vector = np.array(vector)
		return vector / self.length_of_vector(vector)
	
	
	def angle_between_vectors(self,vector1,vector2):
		vector1 = np.array(vector1, dtype=float)
		vector2 = np.array(vector2, dtype=float)

		dx = vector2[0] - vector1[0]
		# Features of pygame (OY)
		dy = vector1[1] - vector2[1]

		angle = np.arctan2(dy,dx)

		'''normal1 = np.linalg.norm(vector1)
		normal2 = np.linalg.norm(vector2)

		cos_theta = np.dot(vector1, vector2) / (normal1 * normal2)
		cos_theta = np.clip(cos_theta, -1.0, 1.0)

		theta_rad = np.arccos(cos_theta)

		return theta_rad'''
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

engine = EngineFunc()

class Collisions:
	def collision_between_physical_objects(self, objects1, objects2):
		collision = pg.sprite.groupcollide(objects1, objects2, False, False)
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
	

	def collison_betweeen_npc_and_static_objects(self, npcs, objects):
		collision = pg.sprite.groupcollide(npcs, objects, False, False)
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
		

	def collusion_between_enemies(self, enemy, sacrifice):
		for _enemy,_sacrifice in zip(enemy,sacrifice):
			if _enemy.rect.colliderect(_sacrifice.rect):
				_sacrifice.hp -= _enemy.damage


class SortCameraGroup(pg.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pg.display.get_surface()
		self.size = np.array(self.display_surface.get_size()) // 2 
		self.offset = pg.math.Vector2
	def custom_draw(self, player, *screen):
		self.offset = player.rect.center - self.size
		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)




class Inventory:
	def __init__(self,groups):
		self._inv = [[],[]]
		self._visible_sprites = groups[0]
		self._obstacle_sprites = groups[1]
	def add_weapon(self,weapon,name):
		self._inv[0].append(weapon)
		self._inv[1].append(name)
	def choose_weapon(self,ind,weapon):
		if weapon:
			weapon.kill()
		engine.play_sound('materials/effects/ammo_pickup.mp3')
		current_weapon = self._inv[0][ind]
		if ind < len(self._inv[0]):
			self._visible_sprites.add(current_weapon)
			self._obstacle_sprites.add(current_weapon)
			return current_weapon
		return None