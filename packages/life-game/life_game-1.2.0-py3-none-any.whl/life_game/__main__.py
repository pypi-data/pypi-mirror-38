# from life_game import life

import os, sys

if not __package__:
  path = os.path.join(os.path.dirname(__file__), os.pardir)
  sys.path.insert(0, path)

from life_game import life

print('''
Welcome to Life Game!
press SPACE to pause game.
click MOUSE LEFT BUTTON to create a life, or death a life.
press F11 to fullscreen.
''')

life.main()