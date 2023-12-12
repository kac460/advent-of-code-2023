'''
For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0

Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?
'''

from part_1 import (
    get_input_lines,
    next_val,
    get_seq_from_line
)

def reversed_get_seq_from_line(line: str) -> list[int]:
    return list(reversed(get_seq_from_line(line)))

def test_reversed_get_seq_from_line() -> None:
    line = '10 13 16 21 30 45'
    assert reversed_get_seq_from_line(line) == [45, 30, 21, 16, 13, 10]
test_reversed_get_seq_from_line()

assert next_val([0, 0, 0]) == 0
assert next_val([45, 30, 21, 16, 13, 10]) == 5

def main() -> None:
    lines = get_input_lines(use_sample=False)
    answer = sum(next_val(reversed_get_seq_from_line(line)) for line in lines)
    print(f'Final answer: {answer}')

if __name__ == '__main__':
    main()
