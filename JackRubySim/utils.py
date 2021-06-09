from posixpath import split
from bearlibterminal import terminal
from enum import Enum

class Dir(Enum):
  up = 0
  down = 1
  left = 2
  right = 3
  none = 4

class MoveResponse(Enum):
  none = 0
  can_move = 1
  move_scr = 2
  solid = 3

class Mode(Enum):
  start_menu = 0
  playing = 1
  correcting = 2
  win = 3
  lose = 4
  hiscores = 5

def print_terminal(x, y, g, c, bg='black'):
  old_color = terminal.TK_COLOR
  terminal.color(c)
  terminal.bkcolor(bg)
  terminal.printf(x, y, g)
  terminal.color(old_color)

def center_text(width, s):
  return int((width - len(s)) / 2)

def read_and_sort_hiscores(filename):
  f = open(filename, 'r').read().splitlines()

  result = []

  for line in f:
    splitted = line.split(' ')
    name = splitted[0]
    score = splitted[1]
    result.append((name, int(score)))

  result.sort(key = lambda x: x[1], reverse=True)

  return result


# Look at neighbors of pt in cardinal directions
# Depending on neighbors, return a layout
def get_room_layout(pts, pt):
  (x, y) = pt
  result = ''

  up = (x, y - 1) in pts
  down = (x, y + 1) in pts
  left = (x - 1, y) in pts
  right = (x + 1, y) in pts

  # Quads
  if up and down and left and right:
    result = 'LRDU'

  # Tris
  elif up and down and left and not right:
    result = 'LDU'
  elif up and down and right and not left:
    result = 'RDU'
  elif up and right and left and not down:
    result = 'LRU'
  elif down and right and left and not up:
    result = 'LRD'
  
  # Bis
  elif left and up and not right and not down:
    result = 'LU'
  elif right and up and not left and not down:
    result = 'RU'
  elif left and down and not right and not up:
    result = 'LD'
  elif right and down and not left and not up:
    result = 'RD'
  elif right and left and not up and not down:
    result = 'LR'
  elif up and down and not left and not right:
    result = 'DU'

  # Singles
  elif up and not down and not left and not right:
    result = 'U'
  elif down and not up and not left and not right:
    result = 'D'
  elif left and not right and not up and not down:
    result = 'L'
  elif right and not left and not up and not down:
    result = 'R'

  if result == '':
    print("%s %s %s %s" % (up, down, left, right))
  return result