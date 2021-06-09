from utils import print_terminal

# Class representing a tile in the game
class Tile:
  def __init__(self, x, y, glyph, fg, s, i) -> None:
    self.x = x
    self.y = y
    self.glyph = glyph
    self.fg = fg
    self.solid = s
    self.interactable = i
    self.name = ''
    self.desc = ''
  
  def draw(self):
    print_terminal(self.x + 8, self.y + 8, self.glyph, self.fg)