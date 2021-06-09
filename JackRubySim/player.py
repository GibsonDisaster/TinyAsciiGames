from utils import *

# Class representing the player
class Player:
  def __init__(self, x, y, g) -> None:
    self.x = x
    self.y = y
    self.glyph = g

  def draw(self):
    print_terminal(self.x + 8, self.y + 8, self.glyph, 'white')

  # Will definitely need to refactor in the future
  # Checks if player can move to tile in given direction
  #   Player Can -> return MoveResponse indicating so
  #   Player Can't -> Check if player can move to next screen
  #                   returning MoveResponse indicating so
  def can_move(self, dir, w, h, tiles):
    new_pos = (self.x, self.y)
    move_resp = MoveResponse.none

    if dir == Dir.up:
      new_pos = (self.x, self.y - 1)

      if new_pos[1] < 0:
        move_resp = MoveResponse.move_scr
      elif tiles[new_pos].solid:
        move_resp = MoveResponse.solid
      elif new_pos[1] >= 0:
        move_resp = MoveResponse.can_move

    if dir == Dir.down:
      new_pos = (self.x, self.y + 1)
      
      if new_pos[1] > h - 1:
        move_resp = MoveResponse.move_scr
      elif tiles[new_pos].solid:
        move_resp = MoveResponse.solid
      elif new_pos[1] < h:
        move_resp = MoveResponse.can_move

    if dir == Dir.left:
      new_pos = (self.x - 1, self.y)

      if new_pos[0] < 0:
        move_resp = MoveResponse.move_scr
      elif tiles[new_pos].solid:
        move_resp = MoveResponse.solid
      elif new_pos[0] >= 0:
        move_resp = MoveResponse.can_move

    if dir == Dir.right:
      new_pos = (self.x + 1, self.y)

      if new_pos[0] > w - 1:
        move_resp = MoveResponse.move_scr
      elif tiles[new_pos].solid:
        move_resp = MoveResponse.solid
      elif new_pos[0] < w:
        move_resp = MoveResponse.can_move
      else:
        move_resp = MoveResponse.move_scr

    return move_resp