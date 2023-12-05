'''
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

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

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
'''
import re

def is_symbol(char):
    char = char.strip()
    char_is_symbol = bool(char!='.' and re.search(r'\W', char))
    if char_is_symbol:
        print(f'{char} is a symbol')
    return char_is_symbol
assert not is_symbol('.')
assert not is_symbol('3')
assert is_symbol('*')


def has_adjacent_symbol(adjacent_row, num_start_index, num_end_index):
    if not adjacent_row:
        return False
    for row_above_index in range(num_start_index-1, num_end_index+2):
        if row_above_index >= 0 and row_above_index < len(adjacent_row):
            if is_symbol(adjacent_row[row_above_index]):
                return True
    return False

def test_has_adjacent_symbol():
    adjacent_row = '...*......'
    num_start_index = 0
    num_end_index = 2
    assert has_adjacent_symbol(adjacent_row, num_start_index, num_end_index)
    num_start_index = 5
    num_end_index = 7
    assert not has_adjacent_symbol(adjacent_row, num_start_index, num_end_index)

test_has_adjacent_symbol()

def part_numbers_in_row(row_above, curr_row, row_below):
    i = 0
    part_numbers = []
    while i < len(curr_row):
        if re.search(r'\d', curr_row[i]):
            num_start_index = i
            num_end_index = i
            for j in range(i+1, len(curr_row)):
                if not re.search(r'\d', curr_row[j]):
                    break
                num_end_index = j
            is_part_num = (
                has_adjacent_symbol(row_above, num_start_index, num_end_index)
                or has_adjacent_symbol(curr_row, num_start_index, num_end_index)
                or has_adjacent_symbol(row_below, num_start_index, num_end_index)
            )
            if is_part_num:
                part_num = int(curr_row[num_start_index:num_end_index+1])
                print(f'{part_num} is a part')
                part_numbers.append(part_num)     
            i = num_end_index + 1
        else: 
            i += 1
    return part_numbers       

assert part_numbers_in_row(None, '467..114..', '...*......') == [467]
assert part_numbers_in_row('...*......', '..35..633.', '......#...') == [35, 633]


_SAMPLE = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''
def get_input_lines(use_sample):
    if use_sample:
        return _SAMPLE.splitlines()
    with open('input.txt') as f:
        return f.readlines()

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
        total_sum += sum(part_numbers_in_row(row_above, input_lines[curr_row_num], row_below))
    print(total_sum)

if __name__ == '__main__':
    main()
