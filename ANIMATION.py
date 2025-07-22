import pygame as pg
import numpy as np
from ENGINE import Object
import time as t

class Animation:
	def __init__(self):
		'''super().__init__(filename=filename, width=width, height=height)
		self._x = x
		self._y = y
		self._width = width
		self._height = height
		 = []'''
		self.last_update = pg.time.get_ticks()
		self.frame_rate = 10
		self._pull_animation = [[], []]
	def add_animation(self,animation_frames,duration,position):
		frames = len(animation_frames)
		start_time = pg.time.get_ticks()
		animation = (animation_frames,frames,position)
		self._pull_animation.append(animation, duration)
		delta = clock.tick(60) / 1000.0
		current_time = pg.time.get_ticks() / 1000.0
	
	def update(self, screen):
		now = pg.time.get_ticks()
		difference = now - self.last_update
		if difference > self.frame_rate:
			self.last_update = now
			for i in self._pull_animation:
				pass

	def run_animation(self,animation_frames, duration, position, screen):
		# Init for work
		clock = pg.time.Clock()
		start_time = pg.time.get_ticks() / 1000.0  # в секундах
		running = True

		# Animation Loop
		while running:

			elapsed = current_time - start_time
			if elapsed >= duration:
				running = False
			frame_index = min(int((elapsed / duration) * len(animation_frames)), len(animation_frames) - 1)
			current_frame = animation_frames[frame_index]
			screen.blit(current_frame, position)




