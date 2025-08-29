import numpy as np
import pygame as pg
import random as r
import numpy as np


from MAP import Map
from GUI import Gui




pg.init()
pg.display.set_caption('PigSVO')
#pygame.display.set_icon(pygame.image.load("app.bmp"))
pg.mouse.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)




class Game:
	def __init__(self):
		#Engine Init
		self.screen = pg.display.set_mode((1366,768))
		self.done = False
		
		self.map = Map('testmap')
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
			self.clock.tick(60)


if __name__ == "__main__":
	game = Game()
	game.run()
	pg.quit()
