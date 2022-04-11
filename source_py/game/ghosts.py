import pygame
import game.utils as utils


class Ghost(pygame.sprite.Sprite):
  def __init__(self, pos_x, pos_y, color, anim):
    super().__init__(anim.player_group, anim.all_sprites)
    self.frames = []
    image = utils.load_image('ghosts.png')
    utils.cut_image(self, image, 8, 4, color)
    self.color = color
    self.image = self.frames[0]
    self.img_right = self.frames[0]
    self.img_left = self.frames[2]
    self.img_up = self.frames[4]
    self.img_down = self.frames[6]
    self.rect = self.rect.move(anim.tile_width * pos_y + 5, anim.tile_height * pos_x + 4)
    self.pos = [pos_y, pos_x]
    self.prev_pos = [-1, -1]
    self.is_active = False
    self.d_pos = [0, 0]
    self.current_time = 0
    self.anim_time = 1

    if color % 4 == 0:
        self.select_point = self.point_to0
        self.run_up = [20, -1]
        self.is_active = True
    elif color % 4 == 1:
        self.select_point = self.point_to1
        self.run_up = [-1, -1]
        self.is_active = True
    elif color % 4 == 2:
        self.select_point = self.point_to2
        self.run_up = [20, 20]
    elif color % 4 == 3:
        self.select_point = self.point_to3
        self.run_up = [-1, 20]
    self.point_to = self.run_up

    colorkey = self.image.get_at((0, 0))
    self.image.set_colorkey(colorkey)

  def update(self, delta_time, anim):
    if not self.is_active:
      return

    self.current_time += delta_time
    if self.current_time >= self.anim_time:
      self.current_time = 0
      self.change_position_set_direction(anim)
      self.prev_pos[0] = self.pos[0]
      self.prev_pos[1] = self.pos[1]
      self.pos[0] += self.d_pos[0]
      self.pos[1] += self.d_pos[1]

      if anim.map_get_state(*self.pos) == '@': # or anim.map_get_state(*self.prev_pos) == '@':
        anim.game_state = utils.GAME_STATE.LOSE

      if self.d_pos[0] > 0:
        self.image = self.img_right
      elif self.d_pos[0] < 0:
        self.image = self.img_left
      elif self.d_pos[1] > 0:
        self.image = self.img_down
      elif self.d_pos[1] < 0:
        self.image = self.img_up

      dx, dy = 0, 0
      if self.pos[0] < 0:
        self.pos[0] = anim.level_x - 1
        dx = anim.level_x * anim.tile_width
      if self.pos[1] < 0:
        self.pos[1] = anim.level_y - 1
        dy = anim.level_y * anim.tile_height
      if self.pos[0] >= anim.level_x:
        self.pos[0] = 0
        dx = -anim.level_x * anim.tile_width
      if self.pos[1] >= anim.level_y:
        self.pos[1] = 0
        dy = anim.level_y * anim.tile_height
      self.rect.move_ip(self.d_pos[0] * anim.tile_width + dx, self.d_pos[1] * anim.tile_height + dy)
      self.d_pos = [0, 0]

  def change_position_set_direction(self, anim):
    if anim.map_get_state(*self.pos) in list('0123'):
        self.point_to = [7, 8]
    goes = [(self.pos[0] - 1, self.pos[1]), (self.pos[0] + 1, self.pos[1]), (self.pos[0], self.pos[1] - 1), (self.pos[0], self.pos[1] + 1)]
    invalid = set()
    invalid.add((self.prev_pos[0], self.prev_pos[1]))
    for i in goes:
        if not anim.map_validate_cell(*i):
            invalid.add(i)
    cc = list(set(goes) - invalid)
    cc_len = 10000
    pos_to = None
    for i in cc:
        k = (i[0] - self.point_to[0]) ** 2 + (i[1] - self.point_to[1]) ** 2
        if k < cc_len:
            cc_len = k
            pos_to = i
    if pos_to is not None:
        self.d_pos = [pos_to[j] - self.pos[j] for j in range(2)]

  def point_to0(self, player_pos, player_dir, red_ghost_pos):
      return player_pos

  def point_to1(self, player_pos, player_dir, red_ghost_pos):
      return [player_pos[i] + player_dir[i] * 4 for i in range(2)]

  def point_to2(self, player_pos, player_dir, red_ghost_pos):
      return [(red_ghost_pos[i] + player_pos[i] + player_dir[i] * 2) * 2 for i in range(2)]

  def point_to3(self, player_pos, player_dir, red_ghost_pos):
      if (self.pos[0] - player_pos[0]) ** 2 + (self.pos[1] - player_pos[1]) ** 2 < 64:
          return player_pos
      return self.run_up
