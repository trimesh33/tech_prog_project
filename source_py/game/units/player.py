import pygame

import game.utils.image as Image
from game.units.tile import Tile, TILE_TYPES
from game.utils.constants import MAP_CHARACTER

class Player(pygame.sprite.Sprite):
  '''
  Player Pacman class.
  '''
  image_name = 'pac.png'
  image_grid = (3, 1)

  def __init__(self, position, start_delta, anim):
    super().__init__(anim.player_group, anim.all_sprites)
    self.rect, self.frames = Image.cut_image(Image.load_image(self.image_name),
                                             *self.image_grid)
    self.cur_frame = 0
    self.image = self.frames[self.cur_frame]
    self.img_right = self.frames
    self.img_left = [pygame.transform.flip(image, True, False) for image in self.img_right]
    self.img_up = [pygame.transform.rotate(image, 90) for image in self.img_right]
    self.img_down = [pygame.transform.flip(image, False, True) for image in self.img_up]
    self.rect = self.rect.move(anim.screens.tile_width  * position[1] + start_delta[1],
                               anim.screens.tile_height * position[0] + start_delta[0])
    self.pos = position[::-1]
    self.d_pos = [0, 0]
    self.dir = [0, 0]
    self.current_time = 0
    self.animation_delta = 1

  def change_position_set_direction(self, event, anim):
    self.d_pos = [0, 0]
    p_x, p_y, ch = self.get_next_cell(event, anim)
    if ch is not None and self.d_pos != [0, 0]:
        if ch in MAP_CHARACTER.DOT:
            anim.eat_cnt -= 1
            xx, yy = (p_x + self.d_pos[0]) % anim.map.width, (p_y + self.d_pos[1]) % anim.map.height
            anim.all_sprites.remove(anim.map.map_grid[xx][yy])
            anim.tiles_group.remove(anim.map.map_grid[xx][yy])
            anim.map.map_grid[xx][yy].kill()
            anim.map.map_grid[xx][yy] = Tile(TILE_TYPES.EMPTY, (yy, xx), anim)
        anim.map.change_state(p_x, p_y, '-')
        anim.map.change_state(p_x + self.d_pos[0], p_y + self.d_pos[1], '@')
    self.dir = self.d_pos

  def get_next_cell(self, event, anim):
    p_x, p_y = self.pos
    ch = None
    if event.key == pygame.K_UP:  # up
        ch = anim.map.get_state(p_x, p_y - 1)
        if ch in MAP_CHARACTER.DOT + MAP_CHARACTER.EMPTY:
            self.d_pos[1] -= 1
    elif event.key == pygame.K_DOWN:  # down
        ch = anim.map.get_state(p_x, p_y + 1)
        if ch in MAP_CHARACTER.DOT + MAP_CHARACTER.EMPTY:
            self.d_pos[1] += 1
    elif event.key == pygame.K_RIGHT:  # right
        ch = anim.map.get_state(p_x + 1, p_y)
        if ch in MAP_CHARACTER.DOT + MAP_CHARACTER.EMPTY:
            self.d_pos[0] += 1
    elif event.key == pygame.K_LEFT:  # left
        ch = anim.map.get_state(p_x - 1, p_y)
        if ch in MAP_CHARACTER.DOT + MAP_CHARACTER.EMPTY:
            self.d_pos[0] -= 1
    elif event.key == pygame.K_1:
        anim.eat_cnt = 0
    return p_x, p_y, ch
    
  def update(self, delta_time, anim):
    self.choose_image_by_direction()
    dy, dx = 0, 0

    self.pos[0] += self.d_pos[0]
    self.pos[1] += self.d_pos[1]

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
    self.current_time += delta_time
    if self.current_time >= self.animation_delta:
        self.current_time = 0
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)

    self.image = self.frames[self.cur_frame]

  def choose_image_by_direction(self):
    if self.d_pos[0] > 0:
        self.frames = self.img_right
    elif self.d_pos[0] < 0:
        self.frames = self.img_left
    elif self.d_pos[1] > 0:
        self.frames = self.img_down
    elif self.d_pos[1] < 0:
        self.frames = self.img_up
