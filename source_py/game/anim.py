import sys
import pygame

import game.utils.files as Files
from game.utils.constants import GAME_STATE, LIMITS

from game.timer import Timer
from game.map import Map
from game.screens import Screens

class Anim:
  def __init__(self, player_name, map_name):
    pygame.init()
    self.screens = Screens()
    self.timer = Timer()
    self.map = Map(map_name)

    # Sprites group
    self.all_sprites = pygame.sprite.Group()
    self.tiles_group = pygame.sprite.Group()
    self.player_group = pygame.sprite.Group()
    
    # Load maps
    self.player, self.ghosts, self.ghosts_ind, self.eat_cnt = self.map.load_map(self)

    # game
    self.eat_max = self.eat_cnt
    self.game_state = GAME_STATE.START
    # player
    self.player_name = player_name
    self.score_recorded = False

  def loop(self):
    '''
    Infinite loop for game processing.
    '''
    while True:
      delta_time = self.timer.get_delta_time()
      if self.game_state == GAME_STATE.START:
        self.start_events_processing()
        self.screens.start_screen()
        self.timer.set_time_start()
      elif self.game_state == GAME_STATE.RUN:
        self.game_loop_events_processing(delta_time)
        self.ghosts_control(delta_time)
        self.screens.game_screen(self.tiles_group, self.player_group)
        self.screens.draw_eat_counter(self.eat_max - self.eat_cnt, self.eat_cnt)
      elif self.game_state == GAME_STATE.LOSE:
        self.write_score()
        self.screens.game_over_screen()
        self.game_over_events_processing()
      elif self.game_state == GAME_STATE.SCORE:
        self.write_score()
        self.screens.score_screen()
        self.screens.draw_eat_counter(self.eat_max - self.eat_cnt, self.eat_cnt)
        self.score_events_processing()
      elif self.game_state == GAME_STATE.EXIT:
        self.write_score()
        self.terminate()
      if self.eat_cnt == 0 or self.game_state == GAME_STATE.WIN:
        self.game_state = GAME_STATE.WIN
        self.write_score()
        self.eat_cnt = LIMITS.MAX_EAT
        self.screens.game_win_screen()
        self.win_events_processing()
      pygame.display.flip()
      self.timer.update()

  def start_events_processing(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.game_state = GAME_STATE.EXIT
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game_state = GAME_STATE.EXIT
        else:
          self.game_state = GAME_STATE.RUN
      elif event.type == pygame.MOUSEBUTTONDOWN:
        self.game_state = GAME_STATE.RUN

  def game_loop_events_processing(self, delta_time):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.game_state = GAME_STATE.SCORE
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game_state = GAME_STATE.SCORE
        else:
          self.player.change_position_set_direction(event, self)

    self.player.update(delta_time, self)

  def score_events_processing(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.game_state = GAME_STATE.EXIT
      elif event.type == pygame.KEYDOWN:
        if not event.key == pygame.K_ESCAPE:
          self.game_state = GAME_STATE.RUN
        else:
          self.game_state = GAME_STATE.EXIT
      elif event.type == pygame.MOUSEBUTTONDOWN:
        self.game_state = GAME_STATE.RUN

  def game_over_events_processing(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
        self.game_state = GAME_STATE.SCORE

  def win_events_processing(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.game_state = GAME_STATE.EXIT
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game_state = GAME_STATE.EXIT

  def ghosts_control(self, delta_time):
    '''
    Ghosts processing.
    '''
    if self.eat_max - self.eat_cnt > 30 and not self.ghosts[self.ghosts_ind[2]].is_active:
        self.ghosts[self.ghosts_ind[2]].is_active = True
    if self.eat_cnt < self.eat_max * 2 / 3 and not self.ghosts[self.ghosts_ind[3]].is_active:
        self.ghosts[self.ghosts_ind[3]].is_active = True
        self.ghosts[self.ghosts_ind[3]].point_to = self.ghosts[self.ghosts_ind[3]].run_up_target_cell
        self.ghosts[self.ghosts_ind[3]].update(delta_time, self)
    time = self.timer.get_game_time()
    # Run up periods
    if time < 7000 or 27000 < time < 34000 or 54000 < time < 59000 or 79000 < time < 83000:
        for sp in self.ghosts:
            sp.point_to = sp.run_up_target_cell
            sp.update(delta_time, self)
    # Chasing period
    else:
        # 7000 < pygame.time.get_ticks() < 27000 or 34000 < pygame.time.get_ticks() < 54000 or \
        #   59000 < pygame.time.get_ticks() < 79000 or 83000 < pygame.time.get_ticks():
        for sp in self.ghosts:
            sp.point_to = sp.select_point(self.player.pos, self.player.dir, self.ghosts[self.ghosts_ind[0]].pos)
            sp.update(delta_time, self)

  def write_score(self):
    if not self.score_recorded:
      self.score_recorded = True
      Files.write_score(self.player_name, self.eat_max - self.eat_cnt)

  def terminate(self):
    '''
    Quite the game.
    '''
    pygame.quit()
    sys.exit()