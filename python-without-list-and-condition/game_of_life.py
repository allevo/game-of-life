
class GameOfLife(object):
    def __init__(self):
        self.table = set()

    def set_alive(self, *points):
        for point in points:
            key = self.__format(point)
            self.table.add(key)

    def set_dead(self, *points):
        for point in points:
            key = self.__format(point)
            try:
                self.table.remove(key)
            except KeyError as e:
                pass

    def next_cell_status(self, cell):
        count = self.get_neighbors_count(cell)

        conditionsByCurrentState = {
            True: lambda c: c in (2, 3),
            False: lambda c: c == 3,
        }
        rules = {
            True: {
                True: True,
                False: False,
            },
            False: {
                True: True,
                False: False,
            },
        }
        isPresent = cell in self
        return rules[ isPresent ][ conditionsByCurrentState[ isPresent ](count) ]

    def get_neighbors_count(self, cell):
        return sum(map(lambda c: int(c in self), self.get_neighbor(cell)))

    def get_neighbor(self, cell):
        deltas = ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1))
        for delta in deltas:
            yield dict(x=cell['x'] + delta[0], y=cell['y'] + delta[1])

    def get_important_cells(self):
        for key in self.table:
            point = self.__unformat(key)
            for neighbor in self.get_neighbor(point):
                yield neighbor

    def next_step(self):
        next_table = set()
        do_when = {
            True: lambda cell: next_table.add(self.__format(cell)),
            False: lambda cell: False # do nothing
        }
        for cell in self.get_important_cells():
            next_status = self.next_cell_status(cell)
            do_when[next_status](cell)

        self.table = next_table

    def __str__(self):

        minx = min(0, min( int(self.__unformat(point)['x']) for point in self.table ))
        maxx = min(100, max( int(self.__unformat(point)['x']) for point in self.table ))

        miny = min(0, min( int(self.__unformat(point)['y']) for point in self.table ))
        maxy = min(100, max( int(self.__unformat(point)['y']) for point in self.table ))

        repr_map = {
            True: 'x',
            False: ' ',
        }

        s = ''
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                s += repr_map[dict(x=x, y=y) in self]
            s += '\n'
        return s[:-1]

    def __format(self, point):
        return '{x}:{y}'.format(**point)

    def __unformat(self, key):
        return dict(zip(('x', 'y'), map(int, key.split(':'))))

    def __contains__(self, point):
        return self.__format(point) in self.table

    @staticmethod
    def import_from_file(filepath):
        gol = GameOfLife()
        mapForInserting = {
            True: lambda x, y: gol.set_alive(dict(x=x, y=y)),
            False: lambda x, y: x # do nothing
        }
        with open(filepath) as source:
            y = 0
            for line in source.readlines():
                x = 0
                for c in line:
                    mapForInserting[c == 'x'](x, y)
                    x += 1
                y += 1

        return gol
