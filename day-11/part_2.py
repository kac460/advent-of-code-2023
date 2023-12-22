'''
Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
'''
from part_1 import get_input_lines, Location, galaxy_locations, all_location_pairs

def get_expanded_rows_and_cols(input_lines: list[str]) -> tuple[set[int], set[int]]:
    col_has_galaxy = {
        col: False
        for col in range(len(input_lines[0]))
    }
    expanded_rows: set[int] = set()
    
    for row, line in enumerate(input_lines):
        if '#' not in line:
            expanded_rows.add(row)
        
        for col, char in enumerate(input_lines[row]):
            if char == '#':
                col_has_galaxy[col] = True
    expanded_cols = set(
        col
        for col, has_galaxy in col_has_galaxy.items()
        if not has_galaxy
    )
    return expanded_rows, expanded_cols

def test_get_expanded_rows_and_cols() -> None:
    input_lines = get_input_lines(use_sample=True)
    expanded_rows_and_cols = get_expanded_rows_and_cols(input_lines)
    print(expanded_rows_and_cols)
test_get_expanded_rows_and_cols()

def get_dist(
    location_1: Location, 
    location_2: Location, 
    expanded_rows: set[int], 
    expanded_cols: set[int], 
    expansion_factor: int
) -> int:
    # row = 3
    # location_1 row = 2
    # location_2 row = 4
    # min(loc1 row, loc2 row) < row
    # max(loc1 row, loc2 row) > row
    # => row between loc1 row and loc2 row
    num_expanded_rows_between = len([
        row for row in expanded_rows
        if (
            min(location_1.row, location_2.row) < row
            and max(location_1.row, location_2.row) > row
        )
    ])
    num_expanded_cols_between = len([
        col for col in expanded_cols
        if (
            min(location_1.col, location_2.col) < col
            and max(location_1.col, location_2.col) > col
        )
    ])
    
    unexpanded_row_dist = abs(location_1.row - location_2.row)
    expanded_row_dist = unexpanded_row_dist + (expansion_factor - 1) * num_expanded_rows_between

    unexpanded_col_dist = abs(location_1.col - location_2.col)
    expanded_col_dist = unexpanded_col_dist + (expansion_factor - 1) * num_expanded_cols_between

    return expanded_row_dist + expanded_col_dist

def main() -> None:
    use_sample = False
    expansion_factor = 100 if use_sample else 1000000
    input_lines = get_input_lines(use_sample)
    expanded_rows, expanded_cols = get_expanded_rows_and_cols(input_lines)
    pairs = all_location_pairs(galaxy_locations(input_lines))
    print('FINAL ANSWER:')
    print(sum(
        get_dist(
            pair[0],
            pair[1],
            expanded_rows,
            expanded_cols,
            expansion_factor
        )
        for pair in pairs
    ))
if __name__ == '__main__':
    main()