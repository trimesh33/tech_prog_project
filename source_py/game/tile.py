import pygame
import game.utils as utils


class Tile(pygame.sprite.Sprite):
  '''
  Class for tiles.
  '''
  def __init__(self, tile_type, pos_x, pos_y, anim):
    super().__init__(anim.tiles_group, anim.all_sprites)
    tile_images = {'wall': utils.load_image('box.png'), 'empty': utils.load_image('grass.png'), 'dot': utils.load_image('dot.png')}
    self.image = tile_images[tile_type]
    self.rect = self.image.get_rect().move(anim.tile_width * pos_y, anim.tile_height * pos_x)
