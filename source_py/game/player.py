import pygame
import game.utils as utils
import game.tile as tile


class Player(pygame.sprite.Sprite):
  '''
  Player Pacman class.
  '''
  def __init__(self, pos_x, pos_y, anim):
    super().__init__(anim.player_group, anim.all_sprites)
    self.frames = []
    player_image = utils.load_image('pac.png')
    utils.cut_image(self, player_image, 3, 1)
    self.cur_frame = 0
    self.image = self.frames[self.cur_frame]
    self.img_right = self.frames
    self.img_left = [pygame.transform.flip(image, True, False) for image in self.img_right]
    self.img_up = [pygame.transform.rotate(image, 90) for image in self.img_right]
    self.img_down = [pygame.transform.flip(image, False, True) for image in self.img_up]
    self.rect = self.rect.move(anim.tile_width * pos_y + 5, anim.tile_height * pos_x + 4)
    self.pos = [pos_y, pos_x]
    self.d_pos = [0, 0]
    self.dir = [0, 0]
    self.current_time = 0
    self.anim_time = 1
    colorkey = self.image.get_at((0, 0))
    self.image.set_colorkey(colorkey)

  def go(self, event, anim):
    p_x, p_y = self.pos
    self.d_pos = [0, 0]
    ch = None
    if event.key == pygame.K_UP:  # up
        ch = anim.map_get_state(p_x, p_y - 1)
        if ch in '.-':
            self.d_pos[1] -= 1
    elif event.key == pygame.K_DOWN:  # down
        ch = anim.map_get_state(p_x, p_y + 1)
        if ch in '.-':
            self.d_pos[1] += 1
    elif event.key == pygame.K_RIGHT:  # right
        ch = anim.map_get_state(p_x + 1, p_y)
        if ch in '.-':
            self.d_pos[0] += 1
    elif event.key == pygame.K_LEFT:  # left
        ch = anim.map_get_state(p_x - 1, p_y)
        if ch in '.-':
            self.d_pos[0] -= 1
    elif event.key == pygame.K_1:
        anim.eat_cnt = 0
    if ch is not None and self.d_pos != [0, 0]:
        if ch == '.':
            anim.eat_cnt -= 1
            xx, yy = (p_x + self.d_pos[0]) % anim.level_x, (p_y + self.d_pos[1]) % anim.level_y
            anim.all_sprites.remove(anim.game_spr_map[xx][yy])
            anim.tiles_group.remove(anim.game_spr_map[xx][yy])
            anim.game_spr_map[xx][yy].kill()
            anim.game_spr_map[xx][yy] = tile.Tile('empty', yy, xx, anim)
        anim.map_change_state(p_x, p_y, '-')
        anim.map_change_state(p_x + self.d_pos[0], p_y + self.d_pos[1], '@')
    self.dir = self.d_pos

  def update(self, delta_time, anim):
    if self.d_pos[0] > 0:
        self.frames = self.img_right
    elif self.d_pos[0] < 0:
        self.frames = self.img_left
    elif self.d_pos[1] > 0:
        self.frames = self.img_down
    elif self.d_pos[1] < 0:
        self.frames = self.img_up

    dy, dx = 0, 0

    self.pos[0] += self.d_pos[0]
    self.pos[1] += self.d_pos[1]

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
    self.current_time += delta_time
    if self.current_time >= self.anim_time:
        self.current_time = 0
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)

    self.image = self.frames[self.cur_frame]
