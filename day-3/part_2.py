'''
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
'''
import re
import math
from part_1 import get_input_lines

def is_num(char):
    return bool(re.search(r'\d', char))

def get_num_start_and_end_index(s, index):
    start_index = index
    while start_index - 1 >= 0 and is_num(s[start_index - 1]):
        start_index -= 1
    print(f'start_index: {start_index}')
    end_index = index
    while end_index + 1 < len(s) and is_num(s[end_index + 1]):
        end_index += 1
    print(f'end_index: {end_index}')
    return start_index, end_index

assert get_num_start_and_end_index('9..', 0) == (0, 0)
assert get_num_start_and_end_index('99.', 1) == (0, 1)
assert get_num_start_and_end_index('999', 1) == (0, 2)
assert get_num_start_and_end_index('.99', 1) == (1, 2)


def adjacent_numbers(adjacent_row, index):
    if not adjacent_row:
        return []
    nums = []
    # Cases:
    # .*.
    # 9.. -> left num only
    # .9. -> center num only
    # ..9 -> right num only
    # 99. -> left num only
    # 9.9 -> left and right num
    # .99 -> center num only
    # 999 -> left num only

    if index - 1 > 0 and is_num(adjacent_row[index - 1]):
        # adjacent number at left of gear
        left_num_start_index, left_num_end_index = get_num_start_and_end_index(adjacent_row, index - 1)
        nums.append(int(adjacent_row[left_num_start_index:left_num_end_index+1]))
        if left_num_end_index == index - 1 and index + 1 < len(adjacent_row) and is_num(adjacent_row[index + 1]):
            # adjacent number at left of gear, no center num, adjacent number at right of gear
            right_num_start_index, right_num_end_index = get_num_start_and_end_index(adjacent_row, index + 1)
            nums.append(int(adjacent_row[right_num_start_index:right_num_end_index+1]))
    elif is_num(adjacent_row[index]):
        # no adjacent num at left of gear but adjacent num in center
        center_num_start_index, center_end_index = get_num_start_and_end_index(adjacent_row, index)
        nums.append(int(adjacent_row[center_num_start_index:center_end_index+1]))
    elif index + 1 < len(adjacent_row) and is_num(adjacent_row[index + 1]):
        # no adjacent num at left or center of gear
        right_num_start_index, right_num_end_index = get_num_start_and_end_index(adjacent_row, index + 1)
        nums.append(int(adjacent_row[right_num_start_index:right_num_end_index+1]))
    print(f'adjacent nums: {nums}')
    return nums

def test_adjacent_numbers():
    index = 2
    assert adjacent_numbers('89..', index) == [89]
    assert adjacent_numbers('89.5', index) == [89, 5]
    assert adjacent_numbers('895', index) == [895]
    assert adjacent_numbers('9...5', index) == []

test_adjacent_numbers()
        


def gear_ratios_in_row(row_above, curr_row, row_below):
    gear_ratios_in_row = []
    for i in range(len(curr_row)):
        if curr_row[i] == '*':
            potential_adj_nums = (
                adjacent_numbers(row_above, i)
                + adjacent_numbers(curr_row, i)
                + adjacent_numbers(row_below, i)
            )
            if len(potential_adj_nums) != 2:
                print(f'index {i} of {curr_row} is not a gear')
            else:
                print(f'index {i} of {curr_row} is a gear for {potential_adj_nums}')
                gear_ratios_in_row.append(math.prod(potential_adj_nums))
    print(f'final gear_ratios_in_row: {gear_ratios_in_row}')
    return gear_ratios_in_row
            
def test_gear_ratios_in_row():
    row_above = '467..114..'
    curr_row =  '...*......'
    row_below = '..35..633.'
    assert gear_ratios_in_row(row_above, curr_row, row_below) == [467*35]

    row_above = '467..114..'
    curr_row =  '...*......'
    row_below = '......633.'
    assert gear_ratios_in_row(row_above, curr_row, row_below) == []

    row_above = '467.1114..'
    curr_row =  '...*......'
    row_below = '...5..633.'
    assert gear_ratios_in_row(row_above, curr_row, row_below) == []

    row_above = '467..114..'
    curr_row =  '...*.*....'
    row_below = '..35..633.'
    assert gear_ratios_in_row(row_above, curr_row, row_below) == [467*35, 114*633]
test_gear_ratios_in_row()

def main():
    input_lines = get_input_lines(use_sample=False)
    total_sum = 0
    for curr_row_num in range(len(input_lines)):
        row_above_num = curr_row_num - 1
        if row_above_num >= 0:
            row_above = input_lines[row_above_num]
        else:
            row_above = None
        
        row_below_num = curr_row_num + 1
        if row_below_num < len(input_lines):
            row_below = input_lines[row_below_num]
        else:
            row_below = None
        total_sum += sum(gear_ratios_in_row(row_above, input_lines[curr_row_num], row_below))
    print('Final answer: ')
    print(total_sum)

if __name__ == '__main__':
    main()