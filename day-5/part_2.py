'''
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
'''

from part_1 import get_input_lines, get_locations, MAP_NAMES, DestObj

def source_to_destination_map(map_name: str, input_lines: list[str]) -> dict:
    header_index = input_lines.index(f'{map_name} map:')
    src_to_dest_map = {}
    for line in input_lines[header_index+1:]:
        if 'map' in line or not line.strip():  # start of next map / end of input
            break
        dest, src, range_length = (int(num_str) for num_str in line.split())
        src_to_dest_map[src] = DestObj(dest, range_length)
    sorted_sources = sorted(list(src_to_dest_map.keys()))
    if not src_to_dest_map.get(0):
        range_length = sorted_sources[0]
        src_to_dest_map[0] = DestObj(0, range_length)
    for i in range(len(sorted_sources)):
        # e.g. (2, 3) = 2, 3, 4 => start of next implicit range is 5 = 2+3
        start_of_next_implicit_range = sorted_sources[i] + src_to_dest_map[sorted_sources[i]].range_length
        start_of_next_explicit_range = src_to_dest_map[sorted_sources[i+1]].dest_start if i + 1 < len(sorted_sources) else float('inf')
        if not src_to_dest_map.get(start_of_next_implicit_range):
            range_length = start_of_next_explicit_range - start_of_next_implicit_range
            src_to_dest_map[start_of_next_implicit_range] = DestObj(start_of_next_implicit_range, range_length)

    return src_to_dest_map

def test_source_to_destination_map():
    input_lines = get_input_lines(use_sample=True)
    src_to_dest_map = source_to_destination_map('light-to-temperature', input_lines)
    import pprint
    pprint.pprint(src_to_dest_map)
test_source_to_destination_map()

def get_maps(input_lines: list[str]) -> list[dict]:
    return [
        source_to_destination_map(map_name, input_lines)
        for map_name in MAP_NAMES
    ]

def get_location(seed: int, src_to_dest_maps: list[dict]) -> int:
    return list(get_locations([seed], src_to_dest_maps))[0]


def get_seed_range_end_and_location(
    start_seed: int, 
    upper_inclusive_bound_seed: int, 
    src_to_dest_maps: list[dict]
) -> tuple[int, int]:
    # Suppose seed x maps to soil y which belongs to range (y-i, y+j)
    # Then, the upper bound of seed range cannot exceed x+j
    # Then suppose y maps to fertilizer z belonging to (z-l, z+m)
    # Then, the upper bound of seed range cannot exceed min(x+j, z+m)
    # Continue on with the above until we reach the final map and return the min upper bound found.
    seed_range_end = upper_inclusive_bound_seed
    src = start_seed
    for src_to_dest_map in src_to_dest_maps:
        # Find which range this belongs to in the map
        for map_src, dest_obj in src_to_dest_map.items():
            if src >= map_src and src <= map_src + dest_obj.range_length:
                break
        # Our comments above used dest_dist_from_map_dest_end but this is equal to src_dist_from_map_src_end = (map_src + dest_obj.range_length) - src
        src_dist_from_map_src_end = (map_src + dest_obj.range_length) - src
        # note start_seed + src_dist_from_map_src_end gets us the start of the next range
        # e.g. if map_src = 50 and range_length = 2, up to 51
        # therefore, subtract 1
        seed_range_end = min(seed_range_end, start_seed + src_dist_from_map_src_end - 1)
        src_dist_from_map_src = src - map_src
        dest = dest_obj.dest_start + src_dist_from_map_src
        src = dest
    # Final dest is the location
    return (seed_range_end, dest)

def test_get_seed_range_end():
    start_seed = 79
    upper_inclusive_bound_seed = 92
    input_lines = get_input_lines(use_sample=True)
    maps = get_maps(input_lines)
    end_seed, location = get_seed_range_end_and_location(start_seed, upper_inclusive_bound_seed, maps)
    print(end_seed)
    print(location)
    assert end_seed == 81
    assert location == 82
test_get_seed_range_end()

_SEED_START_INDEX = 0
_RANGE_LENGTH_INDEX = 1
# I.e., those defined in the input, not our "seed ranges" defined in our notes.
# returns [(start_seed: int, range: int)]
def get_explicit_seed_ranges(seed_line: str) -> list[tuple[int, int]]:
    # return [int(seed) for seed in seed_line.split(':')[1].split()]
    seed_line_nums = [int(num) for num in seed_line.split(':')[1].split()]
    return [
        (seed_line_nums[i], seed_line_nums[i+1])
        for i in range(0, len(seed_line_nums), 2)
    ]
assert get_explicit_seed_ranges('seeds: 79 14 55 13') == [(79, 14), (55, 13)]

def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    src_to_dest_maps = get_maps(input_lines)
    explicit_seed_ranges = get_explicit_seed_ranges(input_lines[0])
    print(explicit_seed_ranges)
    candidate_seed = explicit_seed_ranges[0][_SEED_START_INDEX]
    curr_lowest_location = get_location(candidate_seed, src_to_dest_maps)
    for explicit_seed_range in explicit_seed_ranges:
        explicit_inclusive_upper_bound = explicit_seed_range[_SEED_START_INDEX] + explicit_seed_range[_RANGE_LENGTH_INDEX] - 1
        end_seed_range = get_seed_range_end(explicit_seed_range[_SEED_START_INDEX], explicit_inclusive_upper_bound, src_to_dest_maps)
        # e.g. if we have (5, 2), we stop at 5 + 2 - 1 = 6
        while end_seed_range != explicit_inclusive_upper_bound:
            start_seed_range = end_seed_range + 1
            print(f'explicit_inclusive_upper_bound: {explicit_inclusive_upper_bound}, start_seed_range: {start_seed_range} end_seed_range: {end_seed_range}')
            candidate_location = get_location(start_seed_range, src_to_dest_maps)
            print(f'candidate_location: {candidate_location}')
            if candidate_location < curr_lowest_location:
                curr_lowest_location = candidate_location
            end_seed_range = get_seed_range_end(start_seed_range, explicit_inclusive_upper_bound, src_to_dest_maps)
    print(f'Final answer: {curr_lowest_location}')

if __name__ == '__main__':
    # main()
    pass
    
