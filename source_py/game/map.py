from game.utils.constants import MAP_CHARACTER
import game.utils.files as Files

from game.units.tile import Tile, TILE_TYPES
from game.units.player import Player
from game.units.ghosts import Ghost


class Map:
  start_delta = (4, 5)

  def __init__(self, map_name):
    self.game_map = Files.load_map(map_name + '.txt')  # y x
    self.map_grid = []
    self.width, self.height = 0, 0

  
  def load_map(self, anim):
    '''
    Create tiles for each objects in game: player, ghosts_instances, walls etc.
    '''
    player_instance, x, y = None, None, None
    ghosts_instances = []
    self.map_grid = []
    ghosts_by_index = dict()
    eat_cnt = 0
    for y in range(len(self.game_map)):
        new_row = []
        for x in range(len(self.game_map[y])):
            if self.game_map[x][y] in MAP_CHARACTER.DOT:
                new_row += [Tile(TILE_TYPES.DOT, (x, y), anim)]
                self.game_map[x][y] = '.'
                eat_cnt += 1
            elif self.game_map[x][y] in MAP_CHARACTER.WALL:
                new_row += [Tile(TILE_TYPES.WALL, (x, y), anim)]
            elif self.game_map[x][y] in MAP_CHARACTER.PLAYER:
                new_row += [Tile(TILE_TYPES.EMPTY, (x, y), anim)]
                player_instance = Player([x, y], self.start_delta, anim)
            elif self.game_map[x][y] in MAP_CHARACTER.GHOSTS:
                new_row += [Tile(TILE_TYPES.EMPTY, (x, y), anim)]
                ghost_type = int(self.game_map[x][y]) % 4
                ghosts_by_index[ghost_type] = len(ghosts_instances)
                ghosts_instances += [Ghost([x, y], self.start_delta, ghost_type, anim)]
        self.map_grid += [new_row]

    self.width = x + 1
    self.height = y + 1
    return player_instance, ghosts_instances, ghosts_by_index, eat_cnt
  
  def change_state(self, x, y, character):
    '''
    Change map state.
    '''
    self.game_map[y % self.height][x % self.width] = character

  def get_state(self, x, y):
    '''
    Get map state by position.
    '''
    return self.game_map[y % self.height][x % self.width]

  def validate_cell(self, x, y):
    '''
    Check if cel isn't wall.
    '''
    return self.game_map[y % self.height][x % self.width] != MAP_CHARACTER.WALL
