import pygame
import os

def constant(function):
  def set(self, value):
      pass
  def get(self):
      return function()
  return property(get, get)

class GameStates(object):
    @constant
    def START():
        return 1
    @constant
    def RUN():
        return 2
    @constant
    def LOSE():
        return 3
    @constant
    def WIN():
        return 4
    @constant
    def SCORE():
        return 5
    @constant
    def EXIT():
      return 6

GAME_STATE = GameStates()

def load_image(name, color_key=None):
  '''
  Load pictures from source path: data/pics/.
  '''
  fullname = os.path.join('data/pics/', name)
  if color_key is not None:
    image = pygame.image.load(fullname).convert()
    if color_key == -1:
      color_key = image.get_at((0, 0))
    image.set_colorkey(color_key)
  else:
    image = pygame.image.load(fullname).convert_alpha()
  return image


def cut_image(self, image, columns, rows, color=0):
  '''
  Cuting image into equals part by number of columns and rows.
  '''
  self.rect = pygame.Rect(0, 0, image.get_width() // columns,
                          image.get_height() // rows)
  for i in range(columns):
    frame_location = (self.rect.w * i, self.rect.h * color)
    self.frames.append(image.subsurface(pygame.Rect(
      frame_location, self.rect.size)))


def load_map(filename):
  '''
  Load map from source path: data/maps/.
  '''
  filename = "data/maps/" + filename
  with open(filename, 'r') as mapFile:
    level_map = [line.strip() for line in mapFile]
  max_width = max(map(len, level_map))
  return [list(i) for i in list(map(lambda x: x.ljust(max_width, '-'), level_map))]
