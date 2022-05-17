def constant(function):
  def set(self, value):
      pass
  def get(self):
      return function()
  return property(get, get)

class GameStates(object):
    @constant
    def START():
        return 1
    @constant
    def RUN():
        return 2
    @constant
    def LOSE():
        return 3
    @constant
    def WIN():
        return 4
    @constant
    def SCORE():
        return 5
    @constant
    def EXIT():
      return 6

class Directions(object):
    @constant
    def RIGHT():
        return 0
    @constant
    def LEFT():
        return 1
    @constant
    def UP():
        return 2
    @constant
    def DOWN():
        return 3

class Ghosts(object):
    @constant
    def BLINKY():
        return 0
    @constant
    def PINKY():
        return 1
    @constant
    def INKY():
        return 2
    @constant
    def CLYDE():
        return 3

class Limits(object):
    @constant
    def WAY_LENGTH():
        return 100000

    @constant
    def MIN_CLYDE_DISTANCE():
        return 64

    @constant
    def MAX_EAT():
        return 100000


class MapCharacter(object):
  @constant
  def WALL():
    return '#'

  @constant
  def GHOSTS():
    return '0123'
  
  @constant
  def PLAYER():
    return '@'

  @constant
  def DOT():
    return '+.'

  @constant
  def EMPTY():
    return '-'


MAP_CHARACTER = MapCharacter()
GAME_STATE = GameStates()
DIRECTION = Directions()
GHOSTS = Ghosts()
LIMITS = Limits()
