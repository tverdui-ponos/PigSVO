import pygame as pg
import random as r

import numpy as np

from MATHLIB import *

from ENGINE import play_sound



class Ai:
    def __init__(self, npc, player): 
        self._player = player
        self.npc = npc

        self._direction = ()

    def goto(self, direction):
        where = np.array(np.array(direction) - np.array(self.npc.rect.center))

        if length_of_vector(where) >= 0:
            where = normalize_vector(where)
        
        if where.all() != 0:
            self.npc.rect.x += where[0] * self.npc.speed
            self.npc.rect.y += where[1] * self.npc.speed
    
    def run(self):
        self.goto(self._player.rect.center)