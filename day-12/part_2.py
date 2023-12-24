'''
To unfold the records, on each row, replace the list of spring conditions with five copies of itself (separated by ?) and replace the list of contiguous groups of damaged springs with five copies of itself (separated by ,).

So, this row:

.# 1

Would become:

.#?.#?.#?.#?.# 1,1,1,1,1

The first line of the above example would become:

???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3

In the above example, after unfolding, the number of possible arrangements for some rows is now much larger:

    ???.### 1,1,3 - 1 arrangement
    .??..??...?##. 1,1,3 - 16384 arrangements
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    ????.#...#... 4,1,1 - 16 arrangements
    ????.######..#####. 1,6,5 - 2500 arrangements
    ?###???????? 3,2,1 - 506250 arrangements

After unfolding, adding all of the possible arrangement counts together produces 525152.

Unfold your condition records; what is the new sum of possible arrangement counts?
'''

from part_1 import get_input_lines, is_valid_arrangement, powerset

def transform_line(line: str) -> str:
    records, sizes = line.split()
    new_records = records
    new_sizes = sizes
    for i in range(4):
        new_records += f'?{records}'
        new_sizes += f',{sizes}'
    return f'{new_records} {new_sizes}'


def get_valid_arrangements(line: str) -> list[set[int]]:
    records, group_size_part = line.split()
    group_sizes = [int(group_size) for group_size in group_size_part.split(',')]
    unknown_indices = [i for i, char in enumerate(records) if char == '?']
    max_num_assignments = sum(group_sizes)
    all_subsets = powerset(unknown_indices)
    return [
        set(possible_assignment)
        for possible_assignment in all_subsets
        if len(possible_assignment) <= max_num_assignments and is_valid_arrangement(
            records,
            group_sizes,
            set(possible_assignment)
        )
    ]

def part_2_num_arrangements(input_line: str) -> int:
    part_1_arrangements = get_valid_arrangements(input_line)
    records, group_sizes = input_line.split()
    # Two decisions:
    #   1) Do we:
    #       a) count the ? joiner as the end of a copy
    #           4 copies like '<original_record>?'
    #           1 copy like '<original_record>'
    #       b) count the ? joiner as the start of a copy
    #           4 copies like '?<original_record>?'
    #           1 copy like '<original_record>'
    #   2) Do we:
    #       a) make the ? joiner a '#'
    #           => could invalidate the adjacent copy
    #               (if ? is end of copy, then we might invalidate the next copy)
    #               (if ? is start of copy, then we might invalidate the prev copy)
    #           Q: what are the circumstances in which we invalidate the adj copy?
    #               WLOG, say we chose ? as end of copy.
    #               Then each of the prev copy's arrangements is invalidated iff:
    #                   The final char is damaged
    #                   (i.e., either '#', or '?' chosen in that arrangement as a '#')
    #               (the opposite to the above applies if we chose ? as start of copy)
    #       b) make the ? joiner a '.'
    #           (never invalidates anything)
    #           (actually, in this case, the "expanded" records have exactly  
    #            same arrangements as the unexpanded, part 1 copy)
    #           (notice if this is the best decision for one copy, it is such for all copies)
    #               (as they all have the same char next to the adjacent copy's ? joiner)
    #   So in total we have 3 possibilities:
    #      1) Treat the ? joiner as a '.' => part_1_num_arrangements ** 5
    #      2) Treat the ? joiner as a '#' at the end of a copy
    #           => Filter out part_1 arrangements where the first char is damaged
    #           => filtered_part_1_arrangements * (expanded_arrangements ** 4)
    #      3) Treat the ? joiner as a '#' at the start of a copy
    #           => Filter out part_1 arrangements where the final char is damaged
    #           => filtered_part_1_arrangements * (expanded_arrangements ** 4)
    #   Return the max of the above
    # Not sure if the above is double-counting things...
    #   We could instead some kind of set.union of all arrangements from the above 3?
    undamaged_joiner_ans = len(part_1_arrangements) ** 5

    if records[0] == '#':
        end_of_copy_joiner_ans = 0
    else:
        if records[0] == '.':
            end_of_copy_joiner_expanded_arrangements = get_valid_arrangements(f'{records}? {group_sizes}')
            end_of_copy_joiner_ans = len(part_1_arrangements) * (len(end_of_copy_joiner_expanded_arrangements) ** 4)
        else:  # '?'
            end_of_copy_joiner_filtered_part_1_num_arrangements = sum(
                1 for arrangement in part_1_arrangements
                if 0 not in arrangement
            )
            # Short-circuit if all the arrangements used the '?' as a '#':
            if end_of_copy_joiner_filtered_part_1_num_arrangements == 0:
                end_of_copy_joiner_ans = 0
            else:
                end_of_copy_joiner_expanded_arrangements = get_valid_arrangements(f'{records}? {group_sizes}')
                end_of_copy_joiner_ans = end_of_copy_joiner_filtered_part_1_num_arrangements * (len(end_of_copy_joiner_expanded_arrangements) ** 4)
    
    if records[-1] == '#':
        start_of_copy_joiner_ans = 0
    else:
        if records[-1] == '.':
            start_of_copy_joiner_expanded_arrangements = get_valid_arrangements(f'?{records} {group_sizes}')
            start_of_copy_joiner_ans = len(part_1_arrangements) * (len(start_of_copy_joiner_expanded_arrangements) ** 4)
        else:
            start_of_copy_joiner_filtered_part_1_num_arrangements = sum(
                1 for arrangement in part_1_arrangements
                if (len(records) - 1) not in arrangement
            )
            # Short-circuit if all the arrangements used the '?' as a '#':
            if start_of_copy_joiner_filtered_part_1_num_arrangements == 0:
                start_of_copy_joiner_ans = 0
            else:
                start_of_copy_joiner_expanded_arrangements = get_valid_arrangements(f'?{records} {group_sizes}')
                start_of_copy_joiner_ans = start_of_copy_joiner_filtered_part_1_num_arrangements * (len(start_of_copy_joiner_expanded_arrangements) ** 4)
    
    return max(undamaged_joiner_ans, end_of_copy_joiner_ans, start_of_copy_joiner_ans)

def test_part_2_num_arrangements() -> None:
    input_lines = get_input_lines(use_sample=True)
    for line in input_lines:
        print(f'{line} - {part_2_num_arrangements(line)} arrangements')
        # print(transform_line(line))
        # print('==============')
# test_part_2_num_arrangements()

def main() -> None:
    input_lines = get_input_lines(use_sample=True)
    answer = sum(
        part_2_num_arrangements(line)
        for line in input_lines
    )
    print(f'FINAL ANSWER: {answer}')

        
if __name__ == '__main__':
    main()