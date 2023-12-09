'''
After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
'''
def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample.txt' if use_sample else 'input.txt'
    with open(f'day-8/{filename}') as f:
        return f.readlines()

_LEFT = 0
_RIGHT = 1

def _get_dests(dest_str: str) -> tuple[str, str]:
    dest_str_split = dest_str.split()
    return (
        dest_str_split[0][1:4],
        dest_str_split[1][:3]
    )



def get_map(input_lines: list[str]) -> dict[str, tuple[str, str]]:
    split_lines = [line.split(' = ') for line in input_lines[2:]]
    return {
        split_line[0]: _get_dests(split_line[1])
        for split_line in split_lines
    }

def test_get_map() -> None:
    assert get_map(get_input_lines(use_sample=True)) == {
        'AAA': ('BBB', 'BBB'), 
        'BBB': ('AAA', 'ZZZ'), 
        'ZZZ': ('ZZZ', 'ZZZ')
    }
test_get_map()

def get_instructions(instruction_line: str) -> list[int]:
    return [
        _LEFT if instruction == 'L'
        else _RIGHT
        for instruction in instruction_line.strip()
    ]

def test_get_instructions() -> None:
    assert get_instructions('LLR') == [_LEFT, _LEFT, _RIGHT]
test_get_instructions()

def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    instructions = get_instructions(input_lines[0])
    desert_map = get_map(input_lines)
    curr_node = 'AAA'
    cnt = 0
    while True:
        for instruction in instructions:
            curr_node = desert_map[curr_node][instruction]
            cnt += 1
            if curr_node == 'ZZZ':
                print(f'Final answer: {cnt}')
                return

if __name__ == '__main__':
    main()
    