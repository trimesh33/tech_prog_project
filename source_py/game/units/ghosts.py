import pygame

import game.utils.image as Image
from game.utils.constants import GAME_STATE, DIRECTION, GHOSTS, LIMITS


class Ghost(pygame.sprite.Sprite):
  '''
  Ghosts class.
  '''
  image_name = 'ghosts.png'
  image_grid = (4, 4)

  def __init__(self, position, start_delta, ghost_type, anim):
    super().__init__(anim.player_group, anim.all_sprites)
    self.rect, self.frames = Image.cut_image(Image.load_image(self.image_name),
                                             *self.image_grid, ghost_type)
    self.image = self.frames[0]
    self.rect = self.rect.move(anim.screens.tile_width  * position[1] + start_delta[1],
                               anim.screens.tile_height * position[0] + start_delta[0])
    self.pos = position[::-1]
    
    self.prev_pos = [-1, -1]
    self.is_active = False
    self.d_pos = [0, 0]
    self.current_time = 0
    self.anim_time = 1
    self.define_target_cell(ghost_type)

  def update(self, delta_time, anim):
    if not self.is_active:
      return

    self.current_time += delta_time
    if self.current_time >= self.anim_time:
      self.current_time = 0
      self.change_position_set_direction(anim)
      self.prev_pos = self.pos
      self.pos = [self.pos[i] + self.d_pos[i] for i in range(2)]

      if anim.map.get_state(*self.pos) == '@': # or anim.map.get_state(*self.prev_pos) == '@':
        anim.game_state = GAME_STATE.LOSE

      self.choose_image_by_direction()

      dx, dy = 0, 0
      if self.pos[0] < 0:
        self.pos[0] = anim.map.width - 1
        dx = anim.map.width * anim.screens.tile_width
      if self.pos[1] < 0:
        self.pos[1] = anim.map.height - 1
        dy = anim.map.height * anim.screens.tile_height
      if self.pos[0] >= anim.map.width:
        self.pos[0] = 0
        dx = -anim.map.width * anim.screens.tile_width
      if self.pos[1] >= anim.map.height:
        self.pos[1] = 0
        dy = anim.map.height * anim.screens.tile_height
      self.rect.move_ip(self.d_pos[0] * anim.screens.tile_width + dx, self.d_pos[1] * anim.screens.tile_height + dy)
      self.d_pos = [0, 0]

  def change_position_set_direction(self, anim):
    if anim.map.get_state(*self.pos) in list('0123'):
        self.point_to = [7, 8]
    possible_steps = [(self.pos[0] - 1, self.pos[1]),
                      (self.pos[0] + 1, self.pos[1]),
                      (self.pos[0], self.pos[1] - 1),
                      (self.pos[0], self.pos[1] + 1)]
    invalid_steps = set()
    invalid_steps.add((self.prev_pos[0], self.prev_pos[1]))
    for step in possible_steps:
        if not anim.map.validate_cell(*step):
            invalid_steps.add(step)
    possible_steps = list(set(possible_steps) - invalid_steps)
    minimum_way_length = LIMITS.WAY_LENGTH
    new_step = None
    for step in possible_steps:
        k = (step[0] - self.point_to[0]) ** 2 + (step[1] - self.point_to[1]) ** 2
        if k < minimum_way_length:
            minimum_way_length = k
            new_step = step
    if new_step is not None:
        self.d_pos = [new_step[j] - self.pos[j] for j in range(2)]

  def point_to_blinky(self, player_pos, player_dir, red_ghost_pos):
      return player_pos

  def point_to_pinky(self, player_pos, player_dir, red_ghost_pos):
      return [player_pos[i] + player_dir[i] * 4 for i in range(2)]

  def point_to_inky(self, player_pos, player_dir, red_ghost_pos):
      return [(red_ghost_pos[i] + player_pos[i] + player_dir[i] * 2) * 2 for i in range(2)]

  def point_to_clyde(self, player_pos, player_dir, red_ghost_pos):
      if (self.pos[0] - player_pos[0]) ** 2 + (self.pos[1] - player_pos[1]) ** 2 < LIMITS.MIN_CLYDE_DISTANCE:
          return player_pos
      return self.run_up_target_cell

  def define_target_cell(self, ghost_type):
    if ghost_type == GHOSTS.BLINKY:
      self.select_point = self.point_to_blinky
      self.run_up_target_cell = [20, -1]
      self.is_active = True
    elif ghost_type == GHOSTS.PINKY:
      self.select_point = self.point_to_pinky
      self.run_up_target_cell = [-1, -1]
      self.is_active = True
    elif ghost_type == GHOSTS.INKY:
      self.select_point = self.point_to_inky
      self.run_up_target_cell = [20, 20]
    elif ghost_type == GHOSTS.CLYDE:
      self.select_point = self.point_to_clyde
      self.run_up_target_cell = [-1, 20]
    self.point_to = self.run_up_target_cell

  def choose_image_by_direction(self):
    if self.d_pos[0] > 0:
      self.image = self.frames[DIRECTION.RIGHT]
    elif self.d_pos[0] < 0:
      self.image = self.frames[DIRECTION.LEFT]
    elif self.d_pos[1] > 0:
      self.image = self.frames[DIRECTION.DOWN]
    elif self.d_pos[1] < 0:
      self.image = self.frames[DIRECTION.UP]
