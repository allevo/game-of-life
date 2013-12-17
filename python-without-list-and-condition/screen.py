import os

class Screen(object):
    def __init__(self, gol):
        self.gol = gol

    def __iter__(self):
        return self

    def next(self):
        self.gol.next_step()
        return str(self.gol)

    def clear_screen(self):
        os.system('clear')

    def print_table(self):
        print self.gol

