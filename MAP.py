import pygame as pg
import json
import numpy as np
import random as r

from ENGINE import EngineFunc,Collisions,SortCameraGroup
from NPC import *
from PLAYER import *
from OBJECT import *

engine = EngineFunc()

TILE_SIZE = np.int16(128)



class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, groups,image):
        super().__init__(groups)
        self.image = engine.get_image(image, TILE_SIZE, TILE_SIZE).convert()
        self.rect = self.image.get_rect(topleft = (x,y))
        

class Map():
    def __init__(self,map_name):
        self.display_surface = pg.display.get_surface()

        self.obstacle_sprites = pg.sprite.Group()
        self.physical_sprites = pg.sprite.Group()
        self.visible_sprites = SortCameraGroup()
        self.npcs = pg.sprite.Group()

        self.create_map(map_name)
        self.collusion = Collisions()

        engine.play_music('materials/music/ambient1.mp3', -1)
    def create_map(self,name):
        with open(f'materials/map/list/{name}.json','r', encoding="utf-8") as filemap:
            map_dict = filemap.read()
            map_json = json.loads(map_dict)
            #print(map_json)
            WORLD_MAP = map_json['tilemap']
            OBJECT_MAP = map_json['objectmap']
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = np.int64(col_index) * TILE_SIZE
                y = np.int64(row_index) * TILE_SIZE

                self.spawn_tile(col,x,y)
        for row_index, row in enumerate(OBJECT_MAP):
            for col_index, col in enumerate(row):
                x = np.int64(col_index) * TILE_SIZE
                y = np.int64(row_index) * TILE_SIZE

                self.spawn_object(col,x,y)
    def spawn_tile(self,type,x,y):
        ''' # - Dirt
            G - Grass
        '''
        match type:
            case "#":
                return 0
            case "G":
                return Tile(x,y, [self.visible_sprites], (f"materials/map/tilemap/grass/grass{r.randint(1,5)}.png"))


    def spawn_object(self,type,x,y):
        ''' P - Player
            T - Tree
            p - Pig
        '''
        match type:
            case "P":
                self.player = Player(x,y, (self.visible_sprites, self.physical_sprites, self.obstacle_sprites, self.npcs))
            case "T":
                return Object(x,y,(f'materials/map/object/trees/tree{r.randint(1,6)}.png'), 200,300, (self.visible_sprites, self.physical_sprites))
            case "p":
                return Pig(x,y, (self.visible_sprites, self.physical_sprites, self.obstacle_sprites, self.npcs))
                

    def run(self):
        self.visible_sprites.custom_draw(self.player, self.display_surface)
        #self.collusion.collision_between_physical_object(self.physical_sprites,self.physical_sprites)
        self.collusion.collison_betweeen_npc_and_static_objects(self.npcs, self.physical_sprites)
        #self.visible_sprites.update()
        self.obstacle_sprites.update()
    def events(self, event):
        self.player.control(event)


