'''--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
'''

_SAMPLE = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''
_USE_SAMPLE = False

def _get_input_lines() -> list[str]:
    if _USE_SAMPLE:
        return _SAMPLE.split()
    with open('input.txt') as f:
        return f.readlines()
    
_TO_DIGIT = {
    **{str(num): str(num) for num in range(1, 10)},  # 1 char
    'one': '1',  # 3 chars
    'two': '2',
    'three': '3',  # 5 chars
    'four': '4',  # 4 chars
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

_CHAR_LENGTHS = set(len(key) for key in _TO_DIGIT.keys())

def _calibration_value_from_line(line: str) -> int:
    first_num = None
    last_num = None
    for i in range(len(line)):
        for length in _CHAR_LENGTHS:
            # print(f'line[i:i+length]: {line[i:i+length]}')
            if i + length < len(line) and line[i:i+length] in _TO_DIGIT:
                first_num = _TO_DIGIT[line[i:i+length]]
                break
        if first_num:
            break
    
    for i in reversed(range(len(line))):
        for length in _CHAR_LENGTHS:
            # print(f'line[i-length:i+1]: {line[i-length+1:i+1]}')
            if i - length +1 >= 0 and line[i-length+1:i+1] in _TO_DIGIT:
                # wefj9
                last_num = _TO_DIGIT[line[i-length+1:i+1]]
                break
        if last_num:
            break
    return int(first_num + last_num)
    



def main() -> None:
    input_lines = _get_input_lines()
    print(sum(_calibration_value_from_line(line) for line in input_lines))

main()
