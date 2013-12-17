from time import sleep 

from screen import Screen
from game_of_life import GameOfLife

gol = GameOfLife.import_from_file('./glider')
screen = Screen(gol)

screen.print_table()

for table in screen:
    screen.clear_screen()
    screen.print_table()
    sleep(0.5)
