from part_1 import (
    get_instructions,
    get_map
)
from typing import TypeAlias, NamedTuple

DesertMap: TypeAlias = dict[str, tuple[str, str]]

def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample_2.txt' if use_sample else 'input.txt'
    with open(f'day-8/{filename}') as f:
        return f.readlines()

def get_starting_locations(desert_map: DesertMap) -> list[str]:
    return [
        node for node in desert_map.keys() if node[-1] == 'A'
    ]

def test_get_starting_locations() -> None:
    input_lines = get_input_lines(use_sample=True)
    desert_map = get_map(input_lines)
    starting_locations = get_starting_locations(desert_map)
    assert starting_locations == ['11A', '22A']
test_get_starting_locations()

# need to modify to have z_positionS_in_loop as a set
class LoopInfo(NamedTuple):
    size: int
    first_instruction_num: int
    # 0 if first node in loop
    z_positions_in_loop: set[int]

def get_loop_info(
    starting_location: str,
    desert_map: DesertMap, 
    instructions: list[int]
) -> LoopInfo:
    curr_location = starting_location
    loop_first_instruction_num = None
    # {N: j} in instruction_nums_to_node[i] 
    # if we're at N before executing instructions[i]
    # and we've executed j instructions up to this point
    instruction_nums_to_node: dict[int, dict[str, int]] = {
        i: dict()
        for i in range(len(instructions))
    }
    instructions_executed = 0
    in_loop_index = None
    while True:
        for i in range(len(instructions)):
            # print(curr_location, i, instruction_nums_to_node)
            # This if block needs to be before we add any z_positions
            # To handle the Z node being the start of the loop
            # (if this were after adding z_positions, we'd erroneously add the z_position at the start of the loop twice)
            # (but with z_position = loop_size)
            if in_loop_index is not None and in_loop_index == loop_size:
                loop_info = LoopInfo(
                    size=loop_size,
                    first_instruction_num=loop_first_instruction_num,
                    z_positions_in_loop=z_positions
                )
                print(f'Re-looped. Loop info: {loop_info}')
                return loop_info
            # in theory an optimization might be to store data s.t. we can infer the loop size without re-looping
            # however, we still need to re-loop to gather the z positions
            # we *could* also be storing the z positions everytime we see them regardless of if we know we're in a loop or not and then infer the z positions within the loop, but i don't think that's worth it...
            if curr_location in instruction_nums_to_node[i] and loop_first_instruction_num is None:
                loop_size = instructions_executed - instruction_nums_to_node[i][curr_location]
                loop_first_instruction_num = instruction_nums_to_node[i][curr_location]
                print('LOOP DISCOVERED', curr_location, loop_size, loop_first_instruction_num)
                in_loop_index = 0
                z_positions = set()
            if in_loop_index is not None and curr_location[-1] == 'Z':
                z_positions.add(in_loop_index)
            instruction_nums_to_node[i][curr_location] = instructions_executed
            curr_location = desert_map[curr_location][instructions[i]]
            instructions_executed += 1
            if in_loop_index is not None:
                in_loop_index += 1
def test_get_loop_info() -> None:
    input_lines = get_input_lines(use_sample=True)
    desert_map = get_map(input_lines)
    starting_location = '22A'
    instructions = get_instructions(input_lines[0])
    loop_info = get_loop_info(starting_location, desert_map, instructions)
    print(f'{starting_location} loop_info: {loop_info}')
    starting_location = '11A'
    loop_info = get_loop_info(starting_location, desert_map, instructions)
    print(f'{starting_location} loop_info: {loop_info}')
    print('--------------')
test_get_loop_info()

def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    instructions = get_instructions(input_lines[0])
    desert_map = get_map(input_lines)
    starting_locations = get_starting_locations(desert_map)
    loop_infos = [
        get_loop_info(starting_location, desert_map, instructions)
        for starting_location in starting_locations
    ]
    print(f'Loop infos: {loop_infos}')
    # i don't think my logic really works in all cases if z_positions_in_loop can have more than 1 element
    # but in our real input they only have 1 element each
    i = max(
        loop_info.first_instruction_num + max(loop_info.z_positions_in_loop)
        for loop_info in loop_infos
    )
    increm = max(
        loop_info.size
        for loop_info in loop_infos
    )
    while True:
        for loop_info in loop_infos:
            at_z_in_this_loop = False
            for z_position in loop_info.z_positions_in_loop:
                if (i - loop_info.first_instruction_num - z_position) % loop_info.size == 0:
                    at_z_in_this_loop = True
                    break
            if not at_z_in_this_loop:
                break
        if at_z_in_this_loop:
            print(f'Final answer: {i}')
            return
        i += increm
            
if __name__ == '__main__':
    main()
    