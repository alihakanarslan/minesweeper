from random import randint

MINE = -1
EMPTY = 0
HIDDEN = -2
MARKED = -3

SIZE = 16
MINE_COUNT = 40
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
    for row in range(len(_table)):
        for col in _table[row]:
            print(f'{col:>2} ', end='')
        print()


def get_count(_player_table: list[list[int]], flag: int):
    count = 0
    for row in _player_table:
        for col in row:
            if col == flag:
                count += 1
    return count


def open_cell(_main_table: list[list[int]], _player_table: list[list[int]], _row: int, _col: int) -> bool:
    if get_count(_player_table, HIDDEN) == len(_main_table) * len(_main_table[_row]):
        place_mines(_main_table, MINE_COUNT, exclude=[(_row, _col), *neighbour_cells(_main_table, _row, _col)])
        place_numbers(_main_table)

    if _main_table[_row][_col] == MINE:
        PLAYER_TABLE[_row][_col] = MINE
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


def mark_cell(_player_table: list[list[int]], _row: int, _col: int):
    if _player_table[_row][_col] == HIDDEN:
        _player_table[_row][_col] = MARKED
        return None
    if _player_table[_row][_col] == MARKED:
        _player_table[_row][_col] = HIDDEN
        return None


def loop():
    show_table(PLAYER_TABLE)
    user_input = input('Mode (o/m), Row, Col: ')
    mode, row, column = (i.strip() for i in user_input.split(','))
    row, column = int(row), int(column)

    if mode == 'o':
        result = open_cell(MAIN_TABLE, PLAYER_TABLE, row, column)
        if not result:
            print(-1)
            return False

    if mode == 'm':
        mark_cell(PLAYER_TABLE, row, column)

    return True


def main():
    while loop():
        if get_count(PLAYER_TABLE, HIDDEN) == 0 and get_count(PLAYER_TABLE, MARKED) == MINE_COUNT:
            print(1)
            break


if __name__ == '__main__':
    main()
