import pygame
import game.utils.image as Image
from game.utils.constants import GAME_STATE


class Screens:
  screen_size = screen_width, screen_height = 475, 475
  tile_size = tile_width = tile_height = 25
  screen_color = (0, 0, 0)
  screen_start = (0, 0)
  font_name = "data/monospace.ttf"


  def __init__(self):
    self.screen = pygame.display.set_mode(self.screen_size)
    self.screen.fill(self.screen_color)

  def start_screen(self):
    intro_text = ["PACMAN",
                  "",
                  "Created by trimesh",
                  "GLHF"]
    background = pygame.transform.scale(Image.load_image('background.jpg'), self.screen_size)
    self.screen.blit(background, self.screen_start)
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

  def game_screen(self, tiles_group, player_group):
    self.screen.fill(self.screen_color)
    tiles_group.draw(self.screen)
    player_group.draw(self.screen)


  def score_screen(self):
    text = ["Scores:", "(\'esc\' for exit)", ""]
    with open("data/score.txt", 'r') as score_file:
      lines = score_file.readlines()
      for i in range(min(len(lines), 5)):
        name_score = lines[i].replace('\n', '').split()
        wd = 20 - len(name_score[0])
        text += ['{}. {}{:.>{wd}}'.format(i, *name_score, wd=wd)]
    # background = pygame.transform.scale(utils.load_image('background.jpg'), (self.screen_width, self.screen_height))
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

  def game_over_screen(self):
    background = pygame.transform.scale(Image.load_image('wasted.png'), (self.screen_width, self.screen_height))
    self.screen.blit(background, (0, 0))

  def game_over_screen1(self):
    line = "You lose!"
    font = pygame.font.Font(self.font_name, 100)
    self.screen.fill((0, 0, 0))
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = self.screen_height / 2 - intro_rect.height / 2
    intro_rect.x = self.screen_width / 2 - intro_rect.width / 2
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
    intro_rect.top = self.screen_height / 2 - intro_rect.height / 2
    intro_rect.x = self.screen_width / 2 - intro_rect.width / 2
    self.screen.blit(string_rendered, intro_rect)

  def draw_eat_counter(self, eat_collected, eat_cnt):
    line = "Your score {}. Points left: {}".format(eat_collected, eat_cnt)
    font = pygame.font.Font(self.font_name, 20)
    io = 'white'
    string_rendered = font.render(line, True, pygame.Color(io))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = self.screen_height - intro_rect.height
    intro_rect.x = 0
    self.screen.blit(string_rendered, intro_rect)
