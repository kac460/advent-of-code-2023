'''
The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

    Between galaxy 1 and galaxy 7: 15
    Between galaxy 3 and galaxy 6: 17
    Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
'''
from typing import NamedTuple
from itertools import combinations

def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample.txt' if use_sample else 'input.txt'
    with open(f'day-11/{filename}') as f:
        return [line.strip() for line in f.readlines()]

class Location(NamedTuple):
    row: int
    col: int

def expanded_universe(unexpanded_universe: list[str]) -> list[list[str]]:
    col_has_galaxy = {
        col: False
        for col in range(len(unexpanded_universe[0]))
    }
    expanded_rows_universe: list[str] = []
    for row in range(len(unexpanded_universe)):
        expanded_rows_universe.append(unexpanded_universe[row])
        if '#' not in unexpanded_universe[row]:
            expanded_rows_universe.append(unexpanded_universe[row])
        for col in range(len(unexpanded_universe[row])):
            if unexpanded_universe[row][col] == '#':
                col_has_galaxy[col] = True
    expanded_universe: list[list[str]] = []
    for row in range(len(expanded_rows_universe)):
        expanded_universe.append([])
        for col in range(len(expanded_rows_universe[row])):
            expanded_universe[row].append(expanded_rows_universe[row][col])
            if not col_has_galaxy[col]:
                expanded_universe[row].append(expanded_rows_universe[row][col])
    return expanded_universe
    
def test_expanded_universe() -> None:
    input_lines = get_input_lines(use_sample=True)
    exp_universe = expanded_universe(input_lines)
    print('EXPANDED UNIVERSE:')
    for cols in exp_universe:
        print(''.join(cols))
test_expanded_universe()

def galaxy_locations(universe: list[list[str]]) -> set[Location]:
    locations: set[Location] = set()
    for row in range(len(universe)):
        for col in range(len(universe[row])):
            if universe[row][col] == '#':
                locations.add(Location(row, col))
    return locations


def all_location_pairs(locations: set[Location]) -> set[tuple[Location, Location]]:
    return set(combinations(locations, 2))

def test_all_location_pairs() -> None:
    input_lines = get_input_lines(use_sample=True)
    locations = galaxy_locations(expanded_universe(input_lines))
    pairs = all_location_pairs(locations)
    print('PAIRS:')
    for pair in pairs:
        print(pair)
test_all_location_pairs()


def manhattan_distance(location_1: Location, location_2: Location) -> int:
    return abs(location_1.row - location_2.row) + abs(location_1.col - location_2.col)

def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    exp_univ = expanded_universe(input_lines)
    pairs = all_location_pairs(galaxy_locations(exp_univ))
    print('FINAL ANSWER:')
    print(sum(manhattan_distance(pair[0], pair[1]) for pair in pairs))

if __name__ == '__main__':
    main()
