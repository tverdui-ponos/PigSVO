import pygame as pg
import numpy as np
from ENGINE import Object

class Animation(Object):
	def __init__(self,width,height,filename,x,y):
		super().__init__(filename=filename, width=width, height=height)
		self._x = x
		self._y = y
		self._width = width
		self._height = height
        self._pull_animation = []
