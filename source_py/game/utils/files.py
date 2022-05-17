def load_map(filename):
  '''
  Load map from source path: data/maps/.
  '''
  filename = "data/maps/" + filename
  with open(filename, 'r') as map_file:
    level_map = [line.strip() for line in map_file]
  max_width = max(map(len, level_map))
  return [list(i) for i in list(map(lambda x: x.ljust(max_width, '-'), level_map))]

def write_score(player_name, score):
  scores = dict()
  with open('data/score.txt', 'r') as score_file:
    for line in score_file.readlines():
      line = line.split()
      scores[line[0]] = int(line[1])
    scores[player_name] = max(scores.get(player_name, 0), score)
  with open('data/score.txt', 'w') as score_file:
    [score_file.write('{} {}\n'.format(key[0], key[1])) for key in sorted(scores.items(), key=lambda item: -item[1])]
