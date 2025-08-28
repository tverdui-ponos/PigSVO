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
	def __init__(self, pos, groups, angle, player):
		super().__init__(animation_frames=[engine.get_image('materials/weapon/melee/hit_right.png', 100, 100)], pos=pos, groups=groups, duration=1)
		self._player = player

		for i, image in enumerate(self._animation_frames):

			rotated_img = pg.transform.rotate(image, angle)
			scaled_img = pg.transform.scale(rotated_img, (self._player.weapon.width * 2, self._player.weapon.height * 2))

			self._animation_frames[i] = scaled_img

		self.image = self._animation_frames[0]
		self.rect = self.image.get_rect(center=pos)	
		self._obstacle_sprites = groups[1]
	
	def update(self):
		if len(self._animation_frames) > 0:
			for i in self._animation_frames:
				self.image = i
				self._animation_frames.remove(i)
				break
		else:
			self.kill()
				
		for sacrifice in self._obstacle_sprites:
			if self.rect.colliderect(sacrifice.rect):
				if hasattr(sacrifice, 'hp'):
					if sacrifice != self._player:
						sacrifice.hp -= self._player.weapon.damage

						direction = np.array(np.array(sacrifice.rect.center) - np.array(self._player.rect.center))
					
						if engine.length_of_vector(direction) >= 0:
							direction = engine.normalize_vector(direction)

						sacrifice.rect.x += direction[0] * self._player.weapon.damage
						sacrifice.rect.y += direction[1] * self._player.weapon.damage
					
						engine.play_sound(self._player.weapon.sounds[1])
				



