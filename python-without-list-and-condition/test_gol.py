
import unittest
from game_of_life import GameOfLife

class TestGameOfLife(unittest.TestCase):
    def test_init(self):
        gol = GameOfLife()

        self.assertTrue(isinstance(gol.table, set))
        self.assertEqual(0, len(gol.table))

    def test_set_alive(self):
        gol = GameOfLife()

        gol.set_alive(dict(x=2, y=4))

        self.assertTrue('2:4' in gol.table)

    def test_set_dead(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=4))
        gol.set_alive(dict(x=1, y=5))

        gol.set_dead(dict(x=2, y=4))

        self.assertFalse('2:4' in gol.table)
        self.assertTrue('1:5' in gol.table)
        self.assertEqual(1, len(gol.table))

    def test_set_dead_not_present(self):
        gol = GameOfLife()

        gol.set_dead(dict(x=2, y=4))

        self.assertFalse('2:4' in gol.table)
        self.assertEqual(0, len(gol.table))

    def test_get_neighbors_count(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=2), dict(x=2, y=4), dict(x=3, y=3), dict(x=3, y=4), dict(x=5, y=-3))

        count = gol.get_neighbors_count(dict(x=2, y=3))

        self.assertEqual(4, count)

    def test_get_neighbors_count_zero_empty(self):
        gol = GameOfLife()

        count = gol.get_neighbors_count(dict(x=2, y=3))

        self.assertEqual(0, count)

    def test_get_neighbors_count_zero(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=2), dict(x=2, y=4), dict(x=3, y=3), dict(x=3, y=4), dict(x=5, y=-3))

        count = gol.get_neighbors_count(dict(x=-1, y=-1))

        self.assertEqual(0, count)

    def test_next_cell_status_I(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=4))

        status = gol.next_cell_status(dict(x=2, y=3))

        self.assertFalse(status)

    def test_next_cell_status_II(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=3), dict(x=2, y=4), dict(x=2, y=2))

        status = gol.next_cell_status(dict(x=2, y=3))

        self.assertTrue(status)

    def test_next_cell_status_III(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=2), dict(x=2, y=4), dict(x=3, y=3))

        status = gol.next_cell_status(dict(x=2, y=3))

        self.assertTrue(status)

    def test_next_cell_status_IV(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=2), dict(x=2, y=4), dict(x=3, y=3), dict(x=3, y=4))

        status = gol.next_cell_status(dict(x=2, y=3))

        self.assertFalse(status)

    def test_get_important_cells_I(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=3))

        cells = sorted(tuple(gol.get_important_cells()))

        self.assertEqual(
            sorted((dict(x=1, y=3), dict(x=1, y=2), dict(x=2, y=2), dict(x=3, y=2), dict(x=3, y=3), dict(x=3, y=4), dict(x=2, y=4), dict(x=1, y=4))),
            cells
        )

    def test_get_important_cells_II(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=3), dict(x=4, y=3))

        cells = sorted(tuple(gol.get_important_cells()))

        self.assertEqual(
            sorted((
                dict(x=1, y=3), dict(x=1, y=2), dict(x=2, y=2), dict(x=3, y=2), dict(x=3, y=3), dict(x=3, y=4), dict(x=2, y=4), dict(x=1, y=4),
                dict(x=3, y=3), dict(x=3, y=2), dict(x=4, y=2), dict(x=5, y=2), dict(x=5, y=3), dict(x=5, y=4), dict(x=4, y=4), dict(x=3, y=4)
            )),
            cells
        )

    def test_blinker(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=3), dict(x=2, y=4), dict(x=2, y=2))

        gol.next_step()

        self.assertTrue('1:3' in gol.table)
        self.assertTrue('2:3' in gol.table)
        self.assertTrue('3:3' in gol.table)
        self.assertEqual(3, len(gol.table))

    def test_static_block(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=1, y=1), dict(x=2, y=1), dict(x=2, y=2), dict(x=1, y=2))

        gol.next_step()

        self.assertTrue('1:1' in gol.table)
        self.assertTrue('2:2' in gol.table)
        self.assertTrue('1:2' in gol.table)
        self.assertTrue('2:1' in gol.table)
        self.assertEqual(4, len(gol.table))

    def test_import_from_file(self):
        gol = GameOfLife.import_from_file('./example')

        self.assertTrue('1:0' in gol.table)
        self.assertTrue('2:0' in gol.table)
        self.assertTrue('0:1' in gol.table)
        self.assertTrue('2:1' in gol.table)
        self.assertTrue('1:2' in gol.table)
        self.assertEqual(5, len(gol.table))

    def test_get_neighbors(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=1), dict(x=3, y=1), dict(x=2, y=2), dict(x=3, y=2), dict(x=3, y=3))

        neighbors_count = gol.get_neighbors_count(dict(x=1, y=1))

        self.assertEqual(2, neighbors_count)

        neighbors_count = gol.get_neighbors_count(dict(x=2, y=1))

        self.assertEqual(3, neighbors_count)

        neighbors_count = gol.get_neighbors_count(dict(x=3, y=1))

        self.assertEqual(3, neighbors_count)

        neighbors_count = gol.get_neighbors_count(dict(x=3, y=1))

        self.assertEqual(3, neighbors_count)

        neighbors_count = gol.get_neighbors_count(dict(x=2, y=2))

        self.assertEqual(4, neighbors_count)

        neighbors_count = gol.get_neighbors_count(dict(x=3, y=2))

        self.assertEqual(4, neighbors_count)

        neighbors_count = gol.get_neighbors_count(dict(x=3, y=3))

        self.assertEqual(2, neighbors_count)



    def test_next_cell_status_V(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=2, y=1), dict(x=3, y=1), dict(x=2, y=2), dict(x=3, y=2), dict(x=3, y=3))

        status = gol.next_cell_status(dict(x=1, y=1))

        self.assertFalse(status)

        status = gol.next_cell_status(dict(x=2, y=1))

        self.assertTrue(status)

        status = gol.next_cell_status(dict(x=3, y=1))

        self.assertTrue(status)

        status = gol.next_cell_status(dict(x=3, y=1))

        self.assertTrue(status)

        status = gol.next_cell_status(dict(x=2, y=2))

        self.assertFalse(status)

        status = gol.next_cell_status(dict(x=3, y=2))

        self.assertFalse(status)

        status = gol.next_cell_status(dict(x=3, y=3))

        self.assertTrue(status)

        status = gol.next_cell_status(dict(x=4, y=2))

        self.assertTrue(status)

        status = gol.next_cell_status(dict(x=2, y=3))

        self.assertTrue(status)

    def test_boat(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=1, y=1), dict(x=2, y=1), dict(x=1, y=2), dict(x=3, y=2), dict(x=2, y=3))

        gol.next_step()

        self.assertEqual(set(['1:1', '2:1', '1:2', '3:2', '2:3']), gol.table)

    def test_glider(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=1, y=1), dict(x=2, y=1), dict(x=3, y=1), dict(x=1, y=2), dict(x=2, y=3))

        gol.next_step()

        self.assertEqual(set(['3:2', '1:1', '1:2', '2:1', '2:0']), gol.table)

    def test_print(self):
        gol = GameOfLife()
        gol.set_alive(dict(x=1, y=1), dict(x=2, y=1), dict(x=3, y=1), dict(x=1, y=2), dict(x=2, y=3))

        s = str(gol)

        expected = [
            '    ',
            ' xxx',
            ' x  ',
            '  x '
        ]
        self.assertEqual('\n'.join(expected), s)


if __name__ == '__main__':
    unittest.main()