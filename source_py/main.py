import sys
from game.anim import Anim

def main():
  args = sys.argv[1:]
  player_name = ''
  maps_name = ['classic', 'edited']
  map_name = maps_name[0]
  try:
    player_name = args[0]
  except IndexError:
    print("Insert your nickname: ")
    player_name = input()
  if len(args) > 1:
    if args[1] in maps_name:
      map_name = args[1]    
  print("Hi {},\nyou chosen {} map.".format(player_name, map_name))

  anim = Anim(player_name, map_name)
  anim.loop()

if __name__ == "__main__":
  main()
