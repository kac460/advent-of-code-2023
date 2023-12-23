'''
In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1

However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1

Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.

In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#), making the whole row #.#.###.

The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ? must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible arrangements of springs.

The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of unknown spring conditions have many different ways they could hold groups of two and one broken springs:

?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#

In this example, the number of possible arrangements for each row is:

    ???.### 1,1,3 - 1 arrangement
    .??..??...?##. 1,1,3 - 4 arrangements
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    ????.#...#... 4,1,1 - 1 arrangement
    ????.######..#####. 1,6,5 - 4 arrangements
    ?###???????? 3,2,1 - 10 arrangements

Adding all of the possible arrangement counts together produces a total of 21 arrangements.

For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?
'''
from itertools import combinations, chain

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample.txt' if use_sample else 'input.txt'
    with open(f'day-12/{filename}') as f:
        return [line.strip() for line in f.readlines()]


_DAMAGED = '#'
def is_valid_arrangement(
    records: str, 
    damaged_group_sizes: list[int], 
    assigned_damaged_indices: set[int]
) -> bool:
    def is_damaged(i: int) -> bool:
        return records[i] == _DAMAGED or i in assigned_damaged_indices
    i = 0
    for target_group_size in damaged_group_sizes:
        curr_group_size = 0
        while i != len(records) and not is_damaged(i):
            i += 1
        
        while i != len(records) and is_damaged(i):
            curr_group_size += 1
            i += 1
        if curr_group_size != target_group_size:
            return False
    while i != len(records):
        # More damaged groups than expected
        if is_damaged(i):
            return False
        i += 1
    return True


def test_is_valid_arrangement() -> None:
    line = '.??..??...?##. 1,1,3'
    records, group_size_part = line.split()
    group_sizes = [int(group_size) for group_size in group_size_part.split(',')]
    valid_assignments = [
        {1, 5, 10},
        {1, 6, 10}, 
        {2, 5, 10},
        {2, 6, 10}
    ]
    for valid_assignment in valid_assignments:
        assert is_valid_arrangement(records, group_sizes, valid_assignment)

    invalid_assignments = [
        {1, 2, 10},
        {1, 5, 6}
    ]
    for invalid_assignment in invalid_assignments:
        assert not is_valid_arrangement(records, group_sizes, invalid_assignment)

    line = '?#?#?#?#?#?#?#? 1,3,1,6'
    #       .#.###.#.######
    records, group_size_part = line.split()
    group_sizes = [int(group_size) for group_size in group_size_part.split(',')]
    valid_assignment = {4, 10, 12, 14}
    assert is_valid_arrangement(records, group_sizes, valid_assignment)
    invalid_assignment = {4, 10, 12, 14, 0}
    assert not is_valid_arrangement(records, group_sizes, invalid_assignment)
    invalid_assignment = {10, 12, 14, 0}
    assert not is_valid_arrangement(records, group_sizes, invalid_assignment)
    print('test_is_valid_arrangement passed')
test_is_valid_arrangement()


def num_arrangements(line: str) -> int:
    records, group_size_part = line.split()
    group_sizes = [int(group_size) for group_size in group_size_part.split(',')]
    unknown_indices = [i for i, char in enumerate(records) if char == '?']
    max_num_assignments = sum(group_sizes)
    all_subsets = powerset(unknown_indices)

    count = 0
    for possible_assignment in all_subsets:
        if len(possible_assignment) <= max_num_assignments and is_valid_arrangement(
            records,
            group_sizes,
            set(possible_assignment)
        ):
            count += 1
    return count


def test_num_arrangements() -> None:
    assert num_arrangements('???.### 1,1,3') == 1
    assert num_arrangements('.??..??...?##. 1,1,3') == 4
    assert num_arrangements('?#?#?#?#?#?#?#? 1,3,1,6') == 1
    assert num_arrangements('????.#...#... 4,1,1') == 1
    assert num_arrangements('????.######..#####. 1,6,5') == 4
    assert num_arrangements('?###???????? 3,2,1') == 10
    print('test_num_arrangements passed')
test_num_arrangements()

def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    answer = sum(
        num_arrangements(line)
        for line in input_lines
    )
    print(f'FINAL ANSWER: {answer}')

if __name__ == '__main__':
    main()