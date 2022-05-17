import pygame

from game.utils.constants import constant
import game.utils.image as Image


class TileTypes(object):
  @constant
  def EMPTY():
    return 0

  @constant
  def DOT():
    return 1
  
  @constant
  def WALL():
    return 2


TILE_TYPES = TileTypes()


class Tile(pygame.sprite.Sprite):
  '''
  Class for tiles.
  '''
  images_names = {TILE_TYPES.WALL: 'box.png',
                  TILE_TYPES.EMPTY: 'grass.png',
                  TILE_TYPES.DOT: 'dot.png'}


  def __init__(self, tile_type, position, anim):
    super().__init__(anim.tiles_group, anim.all_sprites)
    self.image = Image.load_image(self.images_names[tile_type])
    self.rect = self.image.get_rect().move(anim.screens.tile_width * position[1], anim.screens.tile_height * position[0])
