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


cached_text = {}
cached_fonts = {}


class Text:
	def make_font(self,fonts, size):
		available = pg.font.get_fonts()
		choices = map(lambda x:x.lower().replace(' ', ''), fonts)
		for choice in choices:
			if choice in available:
				return pg.font.SysFont(choice, size)
		return pg.font.Font(None, size)

	def get_font(self,font_preferences, size):
		key = str(font_preferences) + '|' + str(size)
		font = cached_fonts.get(key, None)
		if font == None:
			font = self.make_font(font_preferences, size)
			cached_fonts[key] = font
		return font

	def create_text(self,text, fonts, size, color):
		key = '|'.join(map(str, (fonts, size, color, text)))
		image = cached_text.get(key, None)
		if image == None:
			font = self.get_font(fonts, size)
			image = font.render(text, True, color)
			cached_text[key] = image
		return image


class HpBar(Object):
	def __init__(self, x, y, player, groups):
		super().__init__(x, y, "materials/gui/map/picture/hp_bar.png", 300, 100, groups)

		self.display_surface = pg.display.get_surface()
		self._player = player

	def update(self):
		self._hp = self._player.hp
		self.bar = pg.Rect(self.rect.x + 18, self.rect.y, self._hp *  2.8, (self.rect.bottom + self.rect.y)) #pg.Rect(self.rect.left, self.rect.topleft, self._hp, self.rect.bottom)
		pg.draw.rect(self.display_surface, GREEN, self.bar)



class WeaponLabel(pg.sprite.Sprite):
	def __init__(self, x, y, player, groups):
		super().__init__(groups)
		self.text = Text()
		self._player = player
		self.image = self.text.create_text('Помргите', "Arial Black", 50, BLACK)
		self.rect = self.image.get_rect(center=(x,y))
	def update(self):
		weapon_text = self._player.inventory.get_name()
		self.image = self.text.create_text(f'{weapon_text}', "Arial Black", 50, BLACK)
		



class Gui:
	def __init__(self, player):
		self.display_surface = pg.display.get_surface()
		self.visible_objects = pg.sprite.Group()
		self.obstacle_objects = pg.sprite.Group()
		self._player = player
		self.add_elements()

	def add_elements(self):
		HpBar(150, 50, self._player, (self.visible_objects, self.obstacle_objects))
		WeaponLabel(100 , self.display_surface.get_size()[1] - 150 , self._player, (self.visible_objects, self.obstacle_objects))

	def run(self):
		self.obstacle_objects.update()
		self.visible_objects.draw(self.display_surface)



