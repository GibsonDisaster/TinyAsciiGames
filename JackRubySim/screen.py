from tile import Tile

# Class representing a single screen in the game
class Screen:
  tiles = {}

  def __init__(self, filepath):
    f = open(filepath, 'r').read()

    x = 0
    y = 0

    for line in f:
      for char in line:
        if char == '\n':
          x = 0
          y += 1
        else:
          if char == '#':
            self.tiles[(x, y)] = Tile(x, y, char, 'white', True, False)
          else:
            self.tiles[(x, y)] = Tile(x, y, char, 'white', False, False)

          x += 1

  def draw(self):
    for t in self.tiles.values():
      t.draw()