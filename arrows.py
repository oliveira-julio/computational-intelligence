'''

'''
from pprint import PrettyPrinter
INITIAL = list(">>>_<<<")
GOAL = list("<<<_>>>")


def blank_neighbors(state, blank):
    left = 2 if blank > 2 else blank
    right = 3 if blank <= 5 else blank - 5
    result = state[blank - left:blank + right]
    return result


def generate_moviments(state):
    hollow = state.index('_')
    neighbors = blank_neighbors(state, hollow)
    blank = neighbors.index('_')
    moviments = []

    while len(neighbors) < 6:
        neighbors.append(' ')

    if blank - 1 >= 0 and neighbors[blank - 1] == '>':
        moviments.append((hollow - 1, hollow))
    if blank - 2 >= 0 and neighbors[blank - 2] == '>' and neighbors[blank - 1] == '<':
        moviments.append((hollow - 2, hollow))
    if blank + 1 <= 4 and neighbors[blank + 1] == '<':
        moviments.append((hollow + 1, hollow))
    if blank + 2 <= 4 and neighbors[blank + 2] == '<' and neighbors[blank + 1] == '>':
        moviments.append((hollow + 2, hollow))

    def swap(point):
        copy = list(state).copy()
        copy[point[0]] = state[point[1]]
        copy[point[1]] = state[point[0]]
        return copy

    return list(map(swap, moviments))


def solve(states, deep):
    if deep == 0 or states == []:
        return []

    if states[0] == GOAL:
        return [states[0]]

    sons = solve(generate_moviments(states[0]), deep - 1)

    if sons != []:
        return [states[0], *sons]

    return solve(states[1:], deep)


def interactive(deep):
    res = solve([INITIAL], deep)
    if res != []:
        return res
    return interactive(deep + 1)


if __name__ == '__main__':

    answer = interactive(0)
    steps = list(map(lambda s: ''.join(s), answer))
    for step in steps:
        print(step)

