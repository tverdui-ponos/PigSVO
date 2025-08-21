import pygame as pg
import numpy as np

from ENGINE import EngineFunc
from OBJECT import Object


pg.font.init()

engine = EngineFunc()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)



class Interface:
	def __init__(self,x,y,width,height):
		self._x = np.int16(x)
		self._y = np.int16(y)
		self._width = np.int16(width)
		self._height = np.int16(height)
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


class Hp_Bar(Object):
	def __init__(self, x, y, player, groups):
		super().__init__(x, y, "materials/gui/map/picture/hp_bar.png", 300, 100, groups)

		self.display_surface = pg.display.get_surface()
		self._player = player

	def update(self):
		self._hp = self._player.hp
		self.bar = pg.Rect(self.rect.x + 18, self.rect.y, self._hp *  2.8, (self.rect.bottom + self.rect.y)) #pg.Rect(self.rect.left, self.rect.topleft, self._hp, self.rect.bottom)
		pg.draw.rect(self.display_surface, GREEN, self.bar)



class Weapon_Label():
	pass



class Gui:
	def __init__(self, player):
		self.display_surface = pg.display.get_surface()
		self.visible_objects = pg.sprite.Group()
		self.obstacle_objects = pg.sprite.Group()
		self._player = player
		self.add_elements()

	def add_elements(self):
		return Hp_Bar(150, 50, self._player, (self.visible_objects, self.obstacle_objects))

	def run(self):
		self.obstacle_objects.update()
		self.visible_objects.draw(self.display_surface)



