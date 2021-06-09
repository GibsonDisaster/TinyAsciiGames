from random import randint
from utils import get_room_layout
from tile import Tile

# Room Layout is made from a random walk algorithm
# That list of points is then fed through a function
# That matches the point to a room layout depening on its neighbors
class MapGen:
  def __init__(self):
    # Random walked map for game
    self.map = {}

    # (Map Coord) -> Room Layout dictionary
    self.layout_map = {}

    self.reporter_spots = []

    counter = 0

    start_found = False

    self.start_pos = (0, 0)

    pts = []

    walker_x = 8
    walker_y = 8

    while len(pts) < 12:
      dir = randint(0, 1)
      v = randint(-1, 1)

      if dir == 0: # HORIZONTAL
        if walker_x > 0 and walker_x < 15:
          walker_x += v

          if not (walker_x, walker_y) in pts:
            if not start_found:
              self.start_pos = (walker_x, walker_y)
              start_found = True

            pts.append((walker_x, walker_y))
      else: # VERTICAL
        if walker_y > 0 and walker_y < 15:
          walker_y += v

          if not (walker_x, walker_y) in pts:
            if not start_found:
              self.start_pos = (walker_x, walker_y)
              start_found = True

            pts.append((walker_x, walker_y))

    for (px, py) in pts:
      self.map[(px, py)] = Tile(px, py, '.', 'white', False, False)

      if counter > 1 and counter < 8:
        self.reporter_spots.append((px, py))
        counter += 1

      self.layout_map[(px, py)] = get_room_layout(pts, (px, py))