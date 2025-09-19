import numpy as np
import pygame as pg
import random as r
import numpy as np


from PLAYER import *
from ANIMATION import *
from MAP import Map
from GUI import Gui

from SETTING import *


pg.init()
pg.display.set_caption('PigSVO')
#pygame.display.set_icon(pygame.image.load("app.bmp"))
pg.mouse.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)

SCREEN_WIDTH = display.get_desktop_sizes()[0]



class Game:
	def __init__(self):
		#Engine Init
		self.screen = pg.display.set_mode((SCREEN_WIDTH[0], SCREEN_WIDTH[1]))
		self.done = False
		
		self.map = Map('map1')
		self.gui = Gui(self.map.player)
		
		self.clock = pg.time.Clock()

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:					
				self.done = True

			self.map.events(event)

	def render(self):
		self.screen.fill((0,0,0))
		self.map.run()
		self.gui.run()
		pg.display.flip()


		
	def run(self):
		while not self.done:
			self.handle_events()
			self.render()
			self.clock.tick(FPS)
			pg.display.set_caption(f'PigSVO({int(self.map.current_time)})')

if __name__ == "__main__":
	game = Game()
	game.run()
	pg.quit()