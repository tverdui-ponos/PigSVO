import pygame as pg
import math
import numpy as np



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
		except Exception as e:
			print(f'Error loading sound {path}, {e}')


	
	def play_music(self,path,mode):
		music = self._music_library.get(path)
		music = pg.mixer.music.load(path)
		self._music_library[path] = music
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

class Object(pg.sprite.Sprite):
	def __init__(self,x,y,filename,width,height):
		pg.sprite.Sprite.__init__(self)

		self._x = np.int32(x)
		self._y = np.int32(y)
		self._width = np.int32(width)
		self._height = np.int32(height)
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
