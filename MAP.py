import pygame as pg
import json
import numpy as np
import random as r
import time as t


from ENGINE import Collisions,SortCameraGroup, play_music, play_sound, get_image
from NPC import *
from PLAYER import *
from OBJECT import *
from WEAPON import *



TILE_SIZE = np.int16(128)

START_TIME = t.time()

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, groups,image):
        super().__init__(groups)
        self.image = get_image(image, TILE_SIZE, TILE_SIZE).convert()
        self.rect = self.image.get_rect(topleft = (x,y))
        

class Map():
    def __init__(self,map_name):
        self.display_surface = pg.display.get_surface()

        self.current_time = 0
        self.delay_before_action = 3


        #
        self.obstacle_sprites = pg.sprite.Group()
        self.visible_sprites = SortCameraGroup()
        #

        #
        self.physical_sprites = pg.sprite.Group()
        self.static_spites = pg.sprite.Group()
        #


        #
        self.npcs_sprites = pg.sprite.Group()
        self.friendly_npcs_sprites = pg.sprite.Group()
        self.enemy_npcs_sprites = pg.sprite.Group()
        #



        self.create_map(map_name)

        self.collusion = Collisions(            
            physical_sprites=self.physical_sprites,
            static_spites=self.static_spites,

            npcs_sprites=self.npcs_sprites,
            friendly_npcs_sprites=self.friendly_npcs_sprites,
            enemy_npcs_sprites=self.enemy_npcs_sprites
        )

        play_music('materials/music/ambient1.mp3', -1)
    def create_map(self,name):
        with open(f'materials/map/list/{name}.json','r', encoding="utf-8") as filemap:
            map_dict = filemap.read()
            map_json = json.loads(map_dict)
            #print(map_json)
            WORLD_MAP = map_json['tilemap']
            OBJECT_MAP = map_json['objectmap']
            self.MAP_SIZE = ((len(WORLD_MAP[0]) - 2) * TILE_SIZE, (len(WORLD_MAP) - 2) * TILE_SIZE)
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
                return Tile(x, y, (self.visible_sprites), (f"materials/map/tilemap/dirt/dirt.png"))

            case "G":
                return Tile(x, y, (self.visible_sprites), (f"materials/map/tilemap/grass/newgrass.png"))


    def spawn_object(self,type,x,y):
        ''' P - Player
            T - Tree
            S - Stone
            p - Pig
            W_...(name_weapon) - WeaponObject
        '''
        match type:
            case "P":
                self.player = Player(x, y, (self.visible_sprites, self.physical_sprites, self.obstacle_sprites, self.npcs_sprites, self.friendly_npcs_sprites))

                self.weapon_list = {"W_Bat": Bat(self.player), 
                "W_Tokarev": Tokarev(self.player),
                "W_Ak47": Ak47(self.player),
                "W_Mosin": Mosin(self.player),
                'W_Eagle': Eagle(self.player),
                'W_Shotgun': Shotgun(self.player)}

            case "T":
                return Object(x, y,(f'materials/map/object/trees/tree{r.randint(1,6)}.png'), 200,300, (self.visible_sprites, self.static_spites))
            
            case "S":
                return Stone(x, y, (self.visible_sprites, self.static_spites))

            case "p":
                return Pig(x, y, (self.visible_sprites, self.physical_sprites, self.obstacle_sprites, self.npcs_sprites, self.enemy_npcs_sprites), self.player)
            case "c":
                return Crate(x, y, (self.visible_sprites, self.physical_sprites, self.obstacle_sprites))
            case 't':
                return Entity(x, y, 'materials/map/object/target.png', 100, 130, (self.visible_sprites, self.obstacle_sprites), 500)

            case 'W_Mosin':
                return WeaponObject(x, y, Mosin(self.player), (self.visible_sprites, self.obstacle_sprites))
            
            case 'W_Ak47':
                return WeaponObject(x, y, Ak47(self.player), (self.visible_sprites, self.obstacle_sprites))
            
            case 'W_Tokarev':
                return WeaponObject(x, y, Tokarev(self.player), (self.visible_sprites, self.obstacle_sprites))

            case 'W_Bat':
                return WeaponObject(x, y, Bat(self.player), (self.visible_sprites, self.obstacle_sprites))

            case 'W_Eagle':
                return WeaponObject(x, y, Eagle(self.player), (self.visible_sprites, self.obstacle_sprites))

            case 'W_Shotgun':
                return WeaponObject(x, y, Shotgun(self.player), (self.visible_sprites, self.obstacle_sprites))


    

    def run(self):
        self.visible_sprites.custom_draw(self.player, self.display_surface)
        self.collusion.collusion()
        self.obstacle_sprites.update()
        self.spawner()
    def events(self, event):
        self.player.control(event)
        if event.type == pg.MOUSEWHEEL:
            zoom_amount = event.y * 0.2
            self.visible_sprites.zoom(zoom_amount)
				



    def spawner(self):
        self.current_time = round(t.time() - START_TIME, 2)
        if self.current_time % self.delay_before_action == 0:
            '''if self.delay_before_action > 0.3:
                self.delay_before_action -= 0.1'''
            supplies = r.randint(0,100)
            pos = (r.randint(0, self.MAP_SIZE[0]), r.randint(100, self.MAP_SIZE[1]))
            if supplies < 5:
                Crate(pos[0], pos[1], (self.visible_sprites, self.physical_sprites, self.obstacle_sprites) )
            elif supplies < 30:
                WeaponObject(pos[0], pos[1], r.choice(list(self.weapon_list.values())), (self.visible_sprites, self.obstacle_sprites))
            else:
                Pig(pos[0], pos[1], (self.visible_sprites, self.physical_sprites, self.obstacle_sprites, self.npcs_sprites, self.enemy_npcs_sprites), self.player)
        

