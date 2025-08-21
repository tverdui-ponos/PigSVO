import pygame as pg
import numpy as np
import time as t

from ENGINE import EngineFunc


engine = EngineFunc()



class Animation(pg.sprite.Sprite):
	def __init__(self, animation_frames, pos, groups, duration=5):
		super().__init__(groups)
		self._animation_frames = sum([[x] * duration for x in animation_frames], [])
		self.image = self._animation_frames[0]
		self.rect = self.image.get_rect(center=pos)
	def update(self):
		if len(self._animation_frames) > 0:
			for i in self._animation_frames:
				self.image = i
				self.rect = self.image.get_rect(center=pos)
				self._animation_frames.remove(i)
				break
		else:
			self.kill()

class MeleeHit(Animation):
	def __init__(self, pos, groups, angle, player, npcs):
		super().__init__(animation_frames=[engine.get_image('materials/weapon/melee/hit_right.png', 100, 100)], pos=pos, groups=groups, duration=1)
		self._player = player

		for i, image in enumerate(self._animation_frames):

			rotated_img = pg.transform.rotate(image, angle)
			scaled_img = pg.transform.scale(rotated_img, (self._player.weapon.width * 2, self._player.weapon.height * 2))

			self._animation_frames[i] = scaled_img

		self.image = self._animation_frames[0]
		self.rect = self.image.get_rect(center=pos)	
		self._npcs = npcs
	
	def update(self):
		if len(self._animation_frames) > 0:
			for i in self._animation_frames:
				self.image = i
				self._animation_frames.remove(i)
				break
		else:
			self.kill()
				
		for npc in self._npcs:
			if self.rect.colliderect(npc.rect):
				if npc != self._player:
					npc.hp -= self._player.weapon.damage
					engine.play_sound('materials/weapon/melee/hands/sound/direct_hit.mp3')
					break
				



