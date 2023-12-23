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
test_transform_line()

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
    expanded_line = f'?{records} {group_sizes}'
    expanded_line_num_arrangements = num_arrangements(expanded_line)
    return part_1_num_arrangements * (expanded_line_num_arrangements ** 4)


def test_part_2_num_arrangements() -> None:
    print(part_2_num_arrangements('.??..??...?##. 1,1,3'))
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