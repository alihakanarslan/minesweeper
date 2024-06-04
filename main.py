from random import randint

MINE = -1
EMPTY = 0
OPENED = 9
HIDDEN = -2
MARKED = -3

SIZE = 9
MINE_COUNT = 10
MAIN_TABLE = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
PLAYER_TABLE = [[HIDDEN for _ in range(SIZE)] for _ in range(SIZE)]


def place_mines(_table: list[list[int]], mine_count: int, exclude: list[tuple[int, int]]):
    placed_mines = 0
    while placed_mines < mine_count:
        row, col = randint(0, len(_table) - 1), randint(0, len(_table) - 1)
        if _table[row][col] == MINE or (row, col) in exclude:
            continue
        _table[row][col] = MINE
        placed_mines += 1


def fix_position(_table: list[list[int]], _row: int, _col: int):
    row = max(min(len(_table) - 1, _row), 0)
    col = max(min(len(_table[row]) - 1, _col), 0)

    return row, col


def neighbour_cells(_table: list[list[int]], _row: int, _col: int):
    neighbours = []
    for offset in [(-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1)]:
        neighbours.append(fix_position(_table, _row + offset[0], _col + offset[1]))
    neighbours = set(neighbours)
    if (_row, _col) in neighbours:
        neighbours.remove((_row, _col))

    return neighbours


def near_mines(_table: list[list[int]], _row: int, _col: int) -> int:
    mines_in_neighbours = 0
    for r, c in neighbour_cells(_table, _row, _col):
        if _table[r][c] == MINE:
            mines_in_neighbours += 1
    return mines_in_neighbours


def place_numbers(_table: list[list[int]]):
    for row in range(len(_table)):
        for col in range(len(_table[row])):
            if _table[row][col] == MINE:
                continue

            _table[row][col] = near_mines(_table, row, col) or EMPTY


def show_table(_table: list[list[int]]):
    for row in _table:
        for col in row:
            print(f'{col:>2} ', end='')
        print()


def all_hidden(_player_table: list[list[int]]):
    for row in _player_table:
        for col in row:
            if col != HIDDEN:
                return False
    return True


def open_cell(_main_table: list[list[int]], _player_table: list[list[int]], _row: int, _col: int) -> bool:
    if all_hidden(_player_table):
        place_mines(_main_table, MINE_COUNT, exclude=[(_row, _col), *neighbour_cells(_main_table, _row, _col)])
        place_numbers(_main_table)

    if _main_table[_row][_col] == MINE:
        return False

    def flood_fill(__row, __col, visited=None):
        if not visited:
            visited = set()

        visited.add((__row, __col))

        PLAYER_TABLE[__row][__col] = _main_table[__row][__col]
        if near_mines(_main_table, __row, __col) == 0:
            for n_row, n_col in neighbour_cells(_main_table, __row, __col):
                if (n_row, n_col) not in visited:
                    flood_fill(n_row, n_col, visited)

    flood_fill(_row, _col)

    return True


def main():
    open_cell(MAIN_TABLE, PLAYER_TABLE, 0, 0)
    show_table(PLAYER_TABLE)


if __name__ == '__main__':
    main()
