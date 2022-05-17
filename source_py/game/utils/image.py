import pygame
import os


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


# def cut_image(self, image, columns, rows, color=0):
#   '''
#   Cuting image into equals part by number of columns and rows.
#   '''
#   self.rect = pygame.Rect(0, 0, image.get_width() // columns,
#                           image.get_height() // rows)
#   for i in range(columns):
#     frame_location = (self.rect.w * i, self.rect.h * color)
#     self.frames.append(image.subsurface(pygame.Rect(
#       frame_location, self.rect.size)))


def cut_image(image, columns, rows, color=0):
  '''
  Cuting image into equals part by number of columns and rows.
  '''
  rect = pygame.Rect(0, 0, image.get_width() // columns,
                          image.get_height() // rows)
  frames = []
  for i in range(columns):
    frame_location = (rect.w * i, rect.h * color)
    frames.append(image.subsurface(pygame.Rect(frame_location, rect.size)))
  return rect, frames
