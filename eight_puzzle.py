from typing import NamedTuple, List, Callable
from functools import partial, reduce
from itertools import repeat
from operator import le as lessOrEqualThan
from operator import gt as greaterThan
from operator import and_
from pprint import PrettyPrinter

Tile = int
Board = List[List[Tile]]


SIZE = 3
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
INITIAL = [[2, 3, 0], [1, 4, 5], [7, 8, 6]]


class Position(NamedTuple):
    row: int
    column: int


def to(moviment: Position):
    def _to(position: Position):
        return position._replace(row=position.row + moviment.row,
                                 column=position.column + moviment.column)
    return _to


up = to(Position(-1, 0))
down = to(Position(1, 0))
right = to(Position(0, 1))
left = to(Position(0, -1))


nonNegative = partial(lessOrEqualThan, 0)
lessThanSize = partial(greaterThan, SIZE)


def rowAndColumnAre(f: Callable[[int], bool], position: Position):
    return f(position.row) and f(position.column)


def getTile(board: Board, position: Position) -> Tile:
    return board[position.row][position.column]


def allowedPosition(position: Position) -> bool:
    conditions = [nonNegative, lessThanSize]
    check = map(rowAndColumnAre, conditions, repeat(position))
    return reduce(and_, check)


def possiblePositions(position: Position) -> List[Position]:
    def apply(f, p):
        return f(p)
    return list(map(apply, [up, left, down, right], repeat(position)))


def validPossiblePositions(position: Position) -> List[Position]:
    return list(filter(allowedPosition, possiblePositions(position)))


def exchangeTiles(board: Board, tileP1: Position, tileP2: Position) -> Board:
    copy = list(map(list.copy, board))
    copy[tileP1.row][tileP1.column] = board[tileP2.row][tileP2.column]
    copy[tileP2.row][tileP2.column] = board[tileP1.row][tileP1.column]
    return copy


def neighbours(zeroPosition, board) -> List[Board]:
    exchangeZero = partial(exchangeTiles, board, zeroPosition)
    return list(map(exchangeZero, validPossiblePositions(zeroPosition)))


def findZero(board: Board) -> Position:
    row = list(filter(lambda r: 0 in r, board))[0]
    return Position(board.index(row), row.index(0))


def flatten(matrix):
    def concat(x, y):
        x.extend(y)
        return x
    blank = []
    return reduce(concat, matrix, blank)


def solve(states, deep):
    if deep == 0 or states == []:
        return []

    if states[0] == GOAL:
        return [states[0]]

    sons = solve(neighbours(findZero(states[0]), states[0]), deep - 1)

    if sons != []:
        return [states[0], *sons]

    return solve(states[1:], deep)


def isSolvable(board: Board):
    flat = flatten(board)
    tiles = range(0, len(flat))

    def howMany(f, l):
        n = len(list(filter(f, l))) - 1
        return n if n > 0 else 0

    def isLessThan(element):
        return partial(greaterThan, flat[element])

    def inversion(element):
        after_element = flat[element:]
        return howMany(isLessThan(element), after_element)

    def isEven(number):
        return number % 2 == 0

    inversions = list(map(inversion, tiles))
    summation = sum(inversions)
    return isEven(summation) and summation != 0


def interactive(deep):
    res = solve([INITIAL], deep)
    if res != []:
        return res
    return interactive(deep + 1)


if __name__ == '__main__':
    if isSolvable(INITIAL):
        answer = interactive(0)
        PrettyPrinter().pprint(answer)
        print(len(answer) - 1)
    else:
        print(":/ unsolvable")
