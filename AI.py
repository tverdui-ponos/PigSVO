import pygame as pg
import random as r

import numpy as np

from MATHLIB import *



class Ai:
    def __init__(self, npc, groups): 
        self._groups = group
        self._tasks = []

    def add_task(self, npc, task='walk'):
        match task:
            case 'walk':
                self.walk()
    
    def goto(self, npc, direction):
        where = np.array(np.array(direction) - np.array(npc.rect.center))

        if length_of_vector(where) >= 0:
            where = normalize_vector(where)
        
        npc.rect += where * npc.rect.speed



    def walk(self, npc, max_distance=100):

        distance = np.array((r.randint(-max_distance, max_distance), r.randint(-max_distance, max_distance)))

        self._tasks.append(direction)
    

    def update(self):
        for npc, tasks in self._tasks:
            if tasks is None:
                self.add_task(npc)