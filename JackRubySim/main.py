from bearlibterminal import terminal
from game import Game

def main():
  playing = True
  game = Game(16, 16)

  terminal.open()
  settings = open("settings.txt", "r").read()
  terminal.set(settings)

  while playing:
    game.draw()
    playing = game.update()
  terminal.close()

if __name__ == "__main__":
  main()