import pygame as pg
from GUI import Text


class Button:
    def __init__(self, x, y, width, height, color, hovered_color, text, action=None):
        self._x = x
        self._y = y
        self._color = color
        self._text = text
