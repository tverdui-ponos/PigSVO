import pygame as pg
import numpy as np

from ENGINE import EngineFunc

pg.font.init()

engine = EngineFunc()

class Interface:
	def __init__(self,x,y,width,height):
		#self.Font = self.get_font('arial',50)
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



