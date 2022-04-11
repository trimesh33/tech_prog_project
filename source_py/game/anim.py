import sys
import pygame

import game.utils as utils
from game.utils import GAME_STATE

from game.tile import Tile
from game.player import Player
from game.ghosts import Ghost


class Anim:
  def __init__(self, player_name, map_name):
    pygame.init() 
    self.size = self.WIDTH, self.HEIGHT = 475, 475
    self.screen = pygame.display.set_mode(self.size)
    self.screen.fill((0, 0, 0))
    # time
    self.FPS = 24
    self.time_start = 0
    self.clock = pygame.time.Clock()
    self.all_sprites = pygame.sprite.Group()
    self.tiles_group = pygame.sprite.Group()
    self.player_group = pygame.sprite.Group()
    self.tile_width = self.tile_height = 25
    # load maps
    self.eat_cnt = 0
    self.game_map = utils.load_map(map_name + '.txt')  # y x
    self.player, self.level_x, self.level_y, self.game_spr_map, self.ghosts, self.ghosts_ind = self.generate_level(self.game_map)
    # game
    self.eat_max = self.eat_cnt
    self.game_state = GAME_STATE.START
    self.running = True
    self.font_name = "data/monospace.ttf"
    #player
    self.player_name = player_name
    self.score_recorded = False

  def loop(self):
    '''
    Infinite loop for game processing.
    '''
    while True:
      delta_time = self.clock.tick(self.FPS) / 100
      if self.game_state == GAME_STATE.START:
        self.start_screen()
        self.time_start = pygame.time.get_ticks()
      elif self.game_state == GAME_STATE.RUN:
        self.game_step(delta_time)
        self.ghosts_control(delta_time)
      elif self.game_state == GAME_STATE.LOSE:
        if not self.score_recorded:
          self.write_score()
          self.score_recorded = True
        self.game_over_screen()
      elif self.game_state == GAME_STATE.SCORE:
        self.score_screen()
      elif self.game_state == GAME_STATE.EXIT:
        self.write_score()
        self.terminate()
      if self.eat_cnt == 0 or self.game_state == GAME_STATE.WIN:
        self.game_state = GAME_STATE.WIN
        self.eat_cnt -= 1
        self.game_win_screen()
      pygame.display.flip()
      self.clock.tick(self.FPS)

  def map_change_state(self, x, y, ch):
    '''
    Infinite loop for game processing.
    '''
    self.game_map[y % self.level_y][x % self.level_x] = ch

  def map_get_state(self, x, y):
    '''
    Infinite loop for game processing.
    '''
    return self.game_map[y % self.level_y][x % self.level_x]

  def map_validate_cell(self, x, y):
    '''
    Infinite loop for game processing.
    '''
    return self.game_map[y % self.level_y][x % self.level_x] != '#'

  def game_step(self, delta_time):
    '''
    Infinite loop for game processing.
    '''
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.game_state = GAME_STATE.SCORE
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game_state = GAME_STATE.SCORE
        else:
          self.player.go(event, self)

    self.player.update(delta_time, self)

    # Draw eat counter 
    self.screen.fill((0, 0, 0))
    self.tiles_group.draw(self.screen)
    self.player_group.draw(self.screen)
    line = "Your score {}. Points left: {}".format(self.eat_max - self.eat_cnt, self.eat_cnt)
    font = pygame.font.Font(self.font_name, 20)
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = self.HEIGHT - intro_rect.height
    intro_rect.x = 0
    self.screen.blit(string_rendered, intro_rect)

  def ghosts_control(self, delta_time):
    '''
    Ghosts processing.
    '''
    if self.eat_max - self.eat_cnt > 30 and not self.ghosts[self.ghosts_ind[2]].is_active:
        self.ghosts[self.ghosts_ind[2]].is_active = True
    if self.eat_cnt < self.eat_max * 2 / 3 and not self.ghosts[self.ghosts_ind[3]].is_active:
        self.ghosts[self.ghosts_ind[3]].is_active = True
        self.ghosts[self.ghosts_ind[3]].point_to = self.ghosts[self.ghosts_ind[3]].run_up
        self.ghosts[self.ghosts_ind[3]].update(delta_time, self)
    tt = pygame.time.get_ticks() - self.time_start
    if tt < 7000 or 27000 < tt < 34000 or 54000 < tt < 59000 or 79000 < tt < 83000:
        for sp in self.ghosts:
            sp.point_to = sp.run_up
            sp.update(delta_time, self)
    else:
        # 7000 < pygame.time.get_ticks() < 27000 or 34000 < pygame.time.get_ticks() < 54000 or \
        #   59000 < pygame.time.get_ticks() < 79000 or 83000 < pygame.time.get_ticks():
        for sp in self.ghosts:
            sp.point_to = sp.select_point(self.player.pos, self.player.dir, self.ghosts[self.ghosts_ind[0]].pos)
            sp.update(delta_time, self)

  def write_score(self):
    scores = dict()
    with open('data/score.txt', 'r') as score_file:
      for line in score_file.readlines():
        line = line.split()
        scores[line[0]] = int(line[1])
      scores[self.player_name] = self.eat_max - self.eat_cnt
    with open('data/score.txt', 'w') as score_file:
      [score_file.write('{} {}\n'.format(key[0], key[1])) for key in sorted(scores.items(), key=lambda item: -item[1])]

  def terminate(self):
    '''
    Quite the game.
    '''
    pygame.quit()
    sys.exit()

  def generate_level(self, level):
    '''
    Create tiles for each objects in game: player, ghosts, walls etc.
    '''
    self.all_sprites = pygame.sprite.Group()
    self.tiles_group = pygame.sprite.Group()
    self.player_group = pygame.sprite.Group()
    new_player, x, y = None, None, None
    mm = []
    ss = []
    ss1 = dict()
    for y in range(len(level)):
        mm1 = []
        for x in range(len(level[y])):
            if level[x][y] in '.+':
                mm1 += [Tile('dot', x, y, self)]
                level[x][y] = '.'
                self.eat_cnt += 1
            elif level[x][y] == '#':
                mm1 += [Tile('wall', x, y, self)]
            elif level[x][y] == '@':
                mm1 += [Tile('empty', x, y, self)]
                new_player = Player(x, y, self)
            elif level[x][y] in '0123':
                mm1 += [Tile('empty', x, y, self)]
                ss1[int(level[x][y]) % 4] = len(ss)
                ss += [Ghost(x, y, int(level[x][y]) % 4, self)]
        mm += [mm1]
    self.all_sprites.draw(self.screen)
    return new_player, x + 1, y + 1, mm, ss, ss1

  def start_screen(self):
    intro_text = ["PACMAN", "",
                  "Created by trimesh",
                  "GLHF"]
    background = pygame.transform.scale(utils.load_image('background.jpg'), (self.WIDTH, self.HEIGHT))
    self.screen.blit(background, (0, 0))
    font = pygame.font.Font(self.font_name, 20)
    text_coord = 50
    io = 'yellow'
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color(io))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        self.screen.blit(string_rendered, intro_rect)
        io = 'red'

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
  
  def score_screen(self):
    text = ["Scores:", "(\'esc\' for exit)", ""]
    with open("data/score.txt", 'r') as score_file:
      lines = score_file.readlines()
      for i in range(min(len(lines), 5)):
        name_score = lines[i].replace('\n', '').split()
        wd = 20 - len(name_score[0])
        text += ['{}. {}{:.>{wd}}'.format(i, *name_score, wd=wd)]
    # background = pygame.transform.scale(utils.load_image('background.jpg'), (self.WIDTH, self.HEIGHT))
    # self.screen.blit(background, (0, 0))
    self.screen.fill((0, 0, 0))
    font = pygame.font.Font(self.font_name, 20)
    text_coord = 50
    io = (50, 0, 240)
    color_cnt = 0
    for line in text:
      string_rendered = font.render(line, True, pygame.Color(io))
      intro_rect = string_rendered.get_rect()
      text_coord += 10
      intro_rect.top = text_coord
      intro_rect.x = 50
      text_coord += intro_rect.height
      if color_cnt > 1:
        io = 'red'
      color_cnt += 1
      self.screen.blit(string_rendered, intro_rect)
    line = "Your score {}. Points left: {}".format(self.eat_max - self.eat_cnt, self.eat_cnt)
    font = pygame.font.Font(self.font_name, 20)
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = self.HEIGHT - intro_rect.height
    intro_rect.x = 0
    self.screen.blit(string_rendered, intro_rect)


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

  def game_over_screen(self):
    background = pygame.transform.scale(utils.load_image('wasted.png'), (self.WIDTH, self.HEIGHT))
    self.screen.blit(background, (0, 0))
    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
        self.game_state = GAME_STATE.SCORE

  def game_over_screen1(self):
    line = "You lose!"
    font = pygame.font.Font(self.font_name, 100)
    self.screen.fill((0, 0, 0))
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = self.HEIGHT / 2 - intro_rect.height / 2
    intro_rect.x = self.WIDTH / 2 - intro_rect.width / 2
    self.screen.blit(string_rendered, intro_rect)

    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
        self.game_state == GAME_STATE.SCORE

  def game_win_screen(self):
    line = "You win!"
    font = pygame.font.Font(self.font_name, 50)
    self.screen.fill((0, 0, 0))
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = self.HEIGHT / 2 - intro_rect.height / 2
    intro_rect.x = self.WIDTH / 2 - intro_rect.width / 2
    self.screen.blit(string_rendered, intro_rect)

    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          self.game_state = GAME_STATE.SCORE