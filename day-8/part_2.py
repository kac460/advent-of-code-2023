from part_1 import (
    get_instructions,
    get_map
)

def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample_2.txt' if use_sample else 'input.txt'
    with open(f'day-8/{filename}') as f:
        return f.readlines()

def get_starting_locations(desert_map: dict[str, tuple[str, str]]) -> list[str]:
    return [
        node for node in desert_map.keys() if node[-1] == 'A'
    ]

def test_get_starting_locations() -> None:
    input_lines = get_input_lines(use_sample=True)
    desert_map = get_map(input_lines)
    starting_locations = get_starting_locations(desert_map)
    assert starting_locations == ['11A', '22A']
test_get_starting_locations()

def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    instructions = get_instructions(input_lines[0])
    desert_map = get_map(input_lines)
    curr_nodes = get_starting_locations(desert_map)
    cnt = 0
    while True:
        for instruction in instructions:
            some_non_z_node = False
            cnt += 1
            for i in range(len(curr_nodes)):
                dest = desert_map[curr_nodes[i]][instruction]
                curr_nodes[i] = dest
                if dest[-1] != 'Z':
                    some_non_z_node = True
            if not some_non_z_node:
                print(f'Final answer: {cnt}')
                return
            
if __name__ == '__main__':
    main()
    