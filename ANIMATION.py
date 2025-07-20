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
		self._pull_animation = []'''
	def add_animation(self,animation):
		self._pull_animation.append(animation)
	def run_animation(self,animation_frames, duration, position, screen):
		# Init for work

		start_time = np.float32(t.time())
		frame_count = np.int8(len(animation_frames))
		frame_duration = np.int16(duration / frame_count)
		current_time = np.float32(t.time())
		elapsed = current_time - start_time
		# Animation Loop
		while elapsed >= duration:
			current_time = np.float32(t.time())
			elapsed = current_time - start_time
			frame_index = np.int16(min(int(elapsed / frame_duration), frame_count - 1))
			current_frame = animation_frames[frame_index]
			screen.blit(current_frame, position)




