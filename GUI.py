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




class MoneyBar(Object):
	def __init__(self, x, y, player, text, groups):
		super().__init__(x, y, "materials/effects/money/bitcoin.png", 50, 50, groups)
		self.text = text
		self._player = player



		self.amount_of_money = self.text.create_text(f'{self._player.money}', 'ArialBlack', 50, WHITE)
		self.amount_of_money_rect = self.amount_of_money.get_rect(center=(self.rect.x + 90, self.rect.y + 26))

	
	def update(self,display):
		self._money = self._player.money
		self.amount_of_money = self.text.create_text(f'{self._money}', 'ArialBlack', 50, WHITE)
		display.blit(self.amount_of_money, self.amount_of_money_rect)


class HpBar(Object):
	def __init__(self, x, y, player, groups):
		super().__init__(x, y, "materials/gui/map/picture/hp_bar.png", 300, 100, groups)

		self._player = player

	def update(self,display):
		self._hp = self._player.hp
		self.bar = pg.Rect(self.rect.x + 18, self.rect.y, self._hp *  2.8, (self.rect.bottom + self.rect.y)) #pg.Rect(self.rect.left, self.rect.topleft, self._hp, self.rect.bottom)
		pg.draw.rect(display, GREEN, self.bar)



class WeaponLabel(pg.sprite.Sprite):
	def __init__(self, x, y, player, text, groups):
		super().__init__(groups)
		self.text = text
		self._player = player
		self.image = self.text.create_text('Помргите', "Arial Black", 50, BLACK)
		self.rect = self.image.get_rect(center=(x,y))
	def update(self,display):
		weapon_text = self._player.inventory.get_name()
		if hasattr(self._player.weapon, 'ammo'):
			weapon_text += str(self._player.weapon.ammo)
		self.image = self.text.create_text(f'{weapon_text}', "Arial Black", 50, BLACK)


class FPS_label(pg.sprite.Sprite):
	def __init__(self, x, y, text, groups):
		super().__init__(groups)
		self.text = text
		self.image = self.text.create_text('Помргите', "Arial Black", 50, WHITE)
		self.rect = self.image.get_rect(center=(x,y))

		self.clock = pg.time.Clock()

	def update(self,display):
		self.fps = int(self.clock.get_fps())
		self.image = self.text.create_text(f'{self.fps}', "Arial Black", 30, WHITE)
		self.clock.tick()



class Gui:
	def __init__(self, player):
		self.display_surface = pg.display.get_surface()
		self.visible_objects = pg.sprite.Group()
		self.obstacle_objects = pg.sprite.Group()
		self._player = player
		self.text = Text()
		self.add_elements()

	def add_elements(self):
		display_size = self.display_surface.get_size()
		self.hp_bar = HpBar(150, 50, self._player, (self.visible_objects, self.obstacle_objects))
		self.weapon_label = WeaponLabel(100 , display_size[1] - 150 , self._player, self.text, (self.visible_objects, self.obstacle_objects))
		self.money_bar = MoneyBar(30,self.hp_bar.rect.y + 140,self._player, self.text, (self.visible_objects, self.obstacle_objects))
		FPS_label(display_size[0] - 30, 30,  self.text, (self.visible_objects, self.obstacle_objects))
	def run(self):
		self.obstacle_objects.update(self.display_surface)
		self.visible_objects.draw(self.display_surface)



