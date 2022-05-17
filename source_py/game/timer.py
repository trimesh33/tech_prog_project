import pygame


class Timer:
  FPS = 24
  time_start = 0

  def __init__(self):
    self.clock = pygame.time.Clock()

  def set_time_start(self):
    self.time_start = pygame.time.get_ticks()

  def get_game_time(self):
    return pygame.time.get_ticks() - self.time_start

  def update(self):
    self.clock.tick(self.FPS)

  def get_delta_time(self):
    return self.clock.tick(self.FPS) / 100