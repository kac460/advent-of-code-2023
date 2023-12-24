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

from part_1 import get_input_lines, num_arrangements

def transform_line(line: str) -> str:
    records, sizes = line.split()
    new_records = records
    new_sizes = sizes
    for i in range(4):
        new_records += f'?{records}'
        new_sizes += f',{sizes}'
    return f'{new_records} {new_sizes}'


def test_transform_line() -> None:
    line = '.# 1'
    assert transform_line(line) == '.#?.#?.#?.#?.# 1,1,1,1,1'
    line = '????.#...#... 4,1,1'
    print(line)
    print(transform_line(line))
    line = '.??..??...?##. 1,1,3'
    print(f'?{line}')
    print(num_arrangements(f'?{line}'))
    print(transform_line(line))
# test_transform_line()

# def num_arrangements(records: str, group_sizes: list[int]) -> int:
#     if len(group_sizes) == 0:
#         return 1
#     i = 0
#     while records[i] != '?':
#         if records[i] == '#':
#             group_sizes[0] -= 1
#             if group_sizes[0] == 0:
#                 group_sizes.pop(0)
#         i += 1
#         if i == len(records):
#             return 1
#     # Case 1: make records[i] '#'
    

def part_2_num_arrangements(input_line: str) -> int:
    part_1_num_arrangements = num_arrangements(input_line)
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
    #           => Filter out part_1 arrangements where the final char is damaged
    #           => filtered_part_1_arrangements * (expanded_arrangements ** 4)
    #      3) Treat the ? joiner as a '#' at the start of a copy
    #           => Filter out part_1 arrangements where the first char is damaged
    #           => filtered_part_1_arrangements * (expanded_arrangements ** 4)
    #   Return the max of the above
    # TODO: rather than num_arrangements, do get_valid_arrangements
    # Not sure if the above is double-counting things...
    #   We could instead some kind of set.union of all arrangements from the above 3?
    


def test_part_2_num_arrangements() -> None:
    input_lines = get_input_lines(use_sample=True)
    for line in input_lines:
        print(f'{line} - {part_2_num_arrangements(line)} arrangements')
        # print(transform_line(line))
        # print('==============')
test_part_2_num_arrangements()

def main() -> None:
    input_lines = get_input_lines(use_sample=True)
    # transformed_lines = [
    #     transform_line(line) for line in input_lines
    # ]
    answer = 0
    for input_line in input_lines:
        input_line_num_arrangements = num_arrangements(input_line)
        records, group_sizes = input_line.split()
        expanded_line = f'?{records} {group_sizes}'
        expanded_line_num_arrangements = num_arrangements(expanded_line)
        total_line_arrangements = input_line_num_arrangements * (expanded_line_num_arrangements ** 4)
        answer += total_line_arrangements
    print(f'FINAL ANSWER: {answer}')

        
# if __name__ == '__main__':
#     main()