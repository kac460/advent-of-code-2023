'''
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
'''

from part_1 import get_input_lines, get_maps, get_locations

def get_location(seed: int, src_to_dest_maps: list[dict]) -> int:
    return list(get_locations([seed], src_to_dest_maps))[0]

def get_seed_range_end(start_seed: int, upper_inclusive_bound_seed: int, src_to_dest_maps: list[dict]) -> int:
    lower_seed = start_seed
    upper_seed = upper_inclusive_bound_seed
    if lower_seed == upper_seed:
        return lower_seed
    start_location = get_location(start_seed, src_to_dest_maps)
    while lower_seed <= upper_seed:
        mid_seed = int((upper_seed + lower_seed) / 2)
        mid_dist_from_start_seed = mid_seed - start_seed
        mid_location = get_location(mid_seed, src_to_dest_maps)
        mid_in_start_seed_range = mid_location == start_location + mid_dist_from_start_seed
        next_seed = mid_seed + 1
        if mid_in_start_seed_range and next_seed <= upper_inclusive_bound_seed:
            next_dist_from_start_seed = next_seed - start_seed
            next_seed_location = get_location(next_seed, src_to_dest_maps)
            if next_seed_location != start_location + next_dist_from_start_seed:
                # If mid_seed is in the seed range
                # but the very next seed is outside of the seed range
                # Then mid is the upper limit of the seed range
                return mid_seed
        # if the above doesn't return, then we know mid_seed is not the end of the seed range
        if not mid_in_start_seed_range: 
            # we've found a new upper bound
            upper_seed = mid_seed - 1
        else:
            # We've found a new lower bound
            lower_seed = mid_seed + 1
    # if we've failed up to this point then it must just be the original upper bound
    return upper_inclusive_bound_seed

def test_get_seed_range_end():
    start_seed = 79
    upper_inclusive_bound_seed = 92
    input_lines = get_input_lines(use_sample=True)
    maps = get_maps(input_lines)
    end_seed = get_seed_range_end(start_seed, upper_inclusive_bound_seed, maps)
    print(end_seed)
    assert end_seed == 81
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
    main()
    
