from reporter import Reporter
from map_gen import MapGen
from screen import Screen
from player import Player
from utils import *
from bearlibterminal import terminal
from datetime import datetime
from textwrap import wrap
from random import randint, shuffle

class Game:
  def __init__(self, w, h):
    self.width = w
    self.height = h
    self.map = {}
    self.player = Player(int(w / 2), int(h / 2), '@')
    self.score = 100000
    self.start_time = datetime.now().time()
    self.curr_time = datetime.now().time()
    self.counting = True # If the timer is on

    self.corrected_reporters = 0
    self.oswald = True

    # Map Loc -> [Reporter]
    self.reporters_map = {}

    self.answers = open('answers.txt', 'r').read().split('\n')
    self.correct = self.answers[0]
    self.cursor_pos = 0

    # Keeps track of what rooms the player has been to
    self.discovered = []

    self.mode = Mode.start_menu

    self.title_screen = open('title_screen.txt', 'r').read()

    # Load the tiles of the screen the player starts on
    self.map_gen = MapGen()
    
    self.map_pos = self.map_gen.start_pos

    curr_layout = self.map_gen.layout_map[self.map_pos]

    self.scr = Screen('rooms/%s.txt' % curr_layout)

    self.basement_loc = list(self.map_gen.map)[-1]

    self.basement_x = randint(5, 14)
    self.basement_y = randint(5, 14)

    # Place reporters until there are ten across the map
    e = 0
    for (pos, _) in self.map_gen.map.items():
      if e == 0:
        self.reporters_map[pos] = [Reporter(10, 10), Reporter(2, 10)] #1
      elif e == 1:
        self.reporters_map[pos] = [Reporter(randint(1, 14), randint(1, 14))] #3
      elif e == 2:
        self.reporters_map[pos] = [Reporter(7, 12), Reporter(14, 11), Reporter(2, 3)] #6
      elif e == 5:
        self.reporters_map[pos] = [Reporter(1, 3), Reporter(10, 10)] # 8
      elif e == 6:
        self.reporters_map[pos] = [Reporter(randint(1, 14), randint(1, 14))] # 9
      elif e == 7:
        self.reporters_map[pos] = [Reporter(randint(1, 14), randint(1, 14))] # 10

      e += 1

  def current_time(self):
    return datetime.now().time()

  def update(self):
    running = True

    if self.mode == Mode.start_menu:
      running = self.start_menu_update()
    elif self.mode == Mode.playing:
      running = self.playing_update()
    elif self.mode == Mode.correcting:
      running = self.correcting_update()
    elif self.mode == Mode.win:
      running = self.win_update()
    elif self.mode == Mode.lose:
      running = self.lose_update()
    elif self.mode == Mode.hiscores:
      running = self.hiscores_update()

    return running

  def draw(self):
    if self.mode == Mode.start_menu:
      self.start_menu_draw()
    elif self.mode == Mode.playing:
      self.playing_draw()
    elif self.mode == Mode.correcting:
      self.correcting_draw()
    elif self.mode == Mode.win:
      self.win_draw()
    elif self.mode == Mode.lose:
      self.lose_draw()
    elif self.mode == Mode.hiscores:
      self.hiscores_draw()

  # UPDATE FUNCTIONS

  def start_menu_update(self):
    running = True

    if terminal.has_input():
      key = terminal.read()

      if key == terminal.TK_1:
        self.__init__(self.width, self.height)
        self.mode = Mode.playing
        self.start_time = self.current_time()
      elif key == terminal.TK_2:
        self.mode = Mode.hiscores
      elif key == terminal.TK_3 or key == terminal.TK_CLOSE:
        running = False

    return running

  def playing_update(self):
    running = True

    if self.counting:
      self.curr_time = self.current_time()

    if terminal.has_input():
      key = terminal.read()

      if key == terminal.TK_CLOSE:
        running = False
      elif key == terminal.TK_TAB:
        self.mode = Mode.win
      elif key == terminal.TK_SPACE:
        key = terminal.read()

        talk_dir = (0, 0)

        if key == terminal.TK_UP:
          talk_dir = (0, -1)
        elif key == terminal.TK_DOWN:
          talk_dir = (0, 1)
        elif key == terminal.TK_LEFT:
          talk_dir = (-1, 0)
        elif key == terminal.TK_RIGHT:
          talk_dir = (1, 0)

        # Position the player wants to talk to
        new_pos = (self.player.x + talk_dir[0], self.player.y + talk_dir[1])
        to_remove = []

        # Go through current screens reporters
        # If player corrects them, add them to a list for later removal
        for r in self.reporters_map[self.map_pos]:
          if r.x == new_pos[0] and r.y == new_pos[1]:
            to_remove.append(r)

            self.corrected_reporters += 1

            shuffle(self.answers)

            self.mode = Mode.correcting

        for item in to_remove:
          self.reporters_map[self.map_pos].remove(item)

      elif key == terminal.TK_W:
        dir = Dir.up
        move_resp = self.player.can_move(dir, self.width, self.height, self.scr.tiles)

        if move_resp == MoveResponse.can_move:
          self.player.y -= 1
        elif move_resp == MoveResponse.move_scr:
          (mx, my) = self.map_pos
          new_pos = (mx, my - 1)

          if new_pos in self.map_gen.map:
            curr_layout = self.map_gen.layout_map[new_pos]
            self.scr = Screen('rooms/%s.txt' % curr_layout)
            self.map_pos = new_pos

            self.player.y = 15

            if not self.map_pos in self.discovered:
              self.discovered.append(self.map_pos)
      elif key == terminal.TK_S:
        dir = Dir.down
        move_resp = self.player.can_move(dir, self.width, self.height, self.scr.tiles)

        if move_resp == MoveResponse.can_move:
          self.player.y += 1
        elif move_resp == MoveResponse.move_scr:
          (mx, my) = self.map_pos
          new_pos = (mx, my + 1)

          if new_pos in self.map_gen.map:
            curr_layout = self.map_gen.layout_map[new_pos]
            self.scr = Screen('rooms/%s.txt' % curr_layout)
            self.map_pos = new_pos

            self.player.y = 0

            if not self.map_pos in self.discovered:
              self.discovered.append(self.map_pos)
      elif key == terminal.TK_A:
        dir = Dir.left
        move_resp = self.player.can_move(dir, self.width, self.height, self.scr.tiles)

        if move_resp == MoveResponse.can_move:
          self.player.x -= 1
        elif move_resp == MoveResponse.move_scr:
          (mx, my) = self.map_pos
          new_pos = (mx - 1, my)

          if new_pos in self.map_gen.map:
            curr_layout = self.map_gen.layout_map[new_pos]
            self.scr = Screen('rooms/%s.txt' % curr_layout)
            self.map_pos = new_pos

            self.player.x = 15

            if not self.map_pos in self.discovered:
              self.discovered.append(self.map_pos)
      elif key == terminal.TK_D:
        dir = Dir.right
        move_resp = self.player.can_move(dir, self.width, self.height, self.scr.tiles)

        if move_resp == MoveResponse.can_move:
          self.player.x += 1
        elif move_resp == MoveResponse.move_scr:
          (mx, my) = self.map_pos
          new_pos = (mx + 1, my)

          if new_pos in self.map_gen.map:
            curr_layout = self.map_gen.layout_map[new_pos]
            self.scr = Screen('rooms/%s.txt' % curr_layout)
            self.map_pos = new_pos

            self.player.x = 0

            if not self.map_pos in self.discovered:
              self.discovered.append(self.map_pos)

      elif key == terminal.TK_PERIOD and terminal.state(terminal.TK_SHIFT):
        if self.basement_loc == self.map_pos:
          if self.player.x == self.basement_x and self.player.y == self.basement_y:
            if self.corrected_reporters == 10: # ADD TIME COMPONENT
              self.mode = Mode.win
            else:
              self.mode = Mode.lose

    return running

  def correcting_update(self):
    running = True

    if self.counting:
      self.curr_time = self.current_time()

    if terminal.has_input():
      key = terminal.read()

      if key == terminal.TK_CLOSE:
        running = False
      elif key == terminal.TK_ESCAPE:
        self.corrected_reporters += 1
        self.mode = Mode.playing
      elif key == terminal.TK_UP:
        if self.cursor_pos > 0:
          self.cursor_pos -= 1
        else:
          self.cursor_pos = len(self.answers) - 1
      elif key == terminal.TK_DOWN:
        if self.cursor_pos >= len(self.answers) - 1:
          self.cursor_pos = 0
        else:
          self.cursor_pos += 1

      elif key == terminal.TK_SPACE:
        if self.answers[self.cursor_pos] == self.correct:
          self.mode = Mode.playing

    return running

  def win_update(self):
    running = True

    if terminal.has_input():
      key = terminal.read()

      if key == terminal.TK_CLOSE:
        running = False
      elif key == terminal.TK_SPACE:
        import easygui

        name = easygui.enterbox('name', title='Hi Scores')

        if name != None:
          (h, m, s) = (self.curr_time.hour - self.start_time.hour, self.curr_time.minute - self.start_time.minute, self.curr_time.second - self.start_time.second)
          self.score -= (h * 1000)
          self.score -= (m * 100)
          self.score -= (s * 10)

          print(self.score)

          f = open('hiscores.txt', 'a')

          f.write('\n%s %s' % (name, self.score))

          f.close()

        self.mode = Mode.start_menu

    return running

  def lose_update(self):
    running = True

    if terminal.has_input():
      key = terminal.read()

      if key == terminal.TK_CLOSE:
        running = False

      elif key == terminal.TK_SPACE:
        self.mode = Mode.start_menu

    return running

  def hiscores_update(self):
    running = True
    key = terminal.read()

    if key == terminal.TK_CLOSE:
        running = False

    elif key == terminal.TK_SPACE:
      self.mode = Mode.start_menu

    return running

  # DRAW FUNCTIONS

  def start_menu_draw(self):
    terminal.clear()

    print_terminal(center_text(48, 'Jack Ruby Sim'), 1 + 8, 'Jack Ruby Sim', 'white')
    print_terminal(center_text(48, '-------------'), 2 + 8, '-------------', 'white')
    print_terminal(center_text(48, '1) New Game'), 4 + 8, '1) New Game', 'white')
    print_terminal(center_text(48, '2) Hi Scores'), 5 + 8, '2) Hi Scores', 'white')
    print_terminal(center_text(48, '2) Hi Scores'), 6 + 8, '3) Quit', 'white')

    terminal.refresh()

  def playing_draw(self):
    terminal.clear()

    self.scr.draw()

    self.player.draw()

    if self.map_pos in self.reporters_map:
      for reporter in self.reporters_map[self.map_pos]:
        print_terminal(reporter.x + 8, reporter.y + 8, 'R', 'green' if reporter.corrected else 'red')

    (h, m, s) = (self.curr_time.hour - self.start_time.hour, self.curr_time.minute - self.start_time.minute, self.curr_time.second - self.start_time.second)

    print_terminal(32, 0, '*'* 16, 'white')
    print_terminal(32, 31, '*'* 16, 'white')

    print_terminal(32, 0, '*\n'* 32, 'white')
    print_terminal(47, 0, '*\n'* 32, 'white')

    print_terminal(33, 1, "Timer: %s:%s:%s" % (h, m, s), 'white')

    mission_strs = wrap("You must correct all 10 reporters in the Dallas Police Station before shooting Lee Harvey Oswald in the basement as he is being moved.", 14)

    mission_end_y = 0

    for (e, s) in enumerate(mission_strs):
      print_terminal(33, e + 3, s, 'red')
      mission_end_y = e + 3
    
    print_terminal(33, mission_end_y + 2, "Reps: %s/10" % self.corrected_reporters, 'white')

    print_terminal(33, mission_end_y + 3, 'Oswald: %s' % ('Alive' if self.oswald else 'Dead'), 'white')

    print_terminal(33, mission_end_y + 4, '*'* 16, 'white')

    for ((x, y), tile) in self.map_gen.map.items():
      if (x, y) in self.discovered:
        print_terminal(33 + x, mission_end_y + 2 + y, tile.glyph, 'red' if (x, y) == self.map_pos else 'white')
      else:
        print_terminal(33 + x, mission_end_y + 2 + y, tile.glyph, 'white')

    if self.map_pos == self.basement_loc:
      print_terminal(self.basement_x + 8, self.basement_y + 8, '>', 'blue')

    terminal.refresh()

  def paused_draw(self):
    terminal.clear()

    print_terminal(0, 0, 'paused', 'white')

    terminal.refresh()

  def correcting_draw(self):
    terminal.clear()

    offset = 0
    for (e, answer) in enumerate(self.answers):
      if e == self.cursor_pos:
        print_terminal(13, 4 + e + offset, '%s <' % answer, 'red')
      else:
        print_terminal(13, 4 + e + offset, answer, 'white')

      offset += 1

    terminal.refresh()

  def win_draw(self):
    terminal.clear()

    terminal.put(0, 0, 0xE001)
    terminal.printf(17, 16, '[color=red]GOOD JOB ASSET')
    terminal.printf(9, 17, '[color=red]TIME FOR YOUR CANCER INJECTION')
    terminal.printf(0, 31, '[color=white]<press spacebar>')

    terminal.refresh()

  def lose_draw(self):
    terminal.clear()

    terminal.put(0, 0, 0xE001)
    terminal.printf(15, 16, '[color=red]SOME ASSET YOU ARE')
    terminal.printf(9, 17, '[color=red]TIME FOR YOUR CANCER INJECTION')
    terminal.printf(16, 19, '[color=white]<PRESS SPACEBAR>')

    terminal.refresh()

  def hiscores_draw(self):
    terminal.clear()

    hiscores = read_and_sort_hiscores('hiscores.txt')

    print_terminal(20, 0, 'HISCORES', 'white')

    for (e, (name, score)) in enumerate(hiscores):
      s = "%s: %s" % (name, score)
      x = int((48 - len(s)) / 2)

      print_terminal(x, e + 2, s, 'white')

    terminal.refresh()