from part_1 import get_input_lines, get_locations, get_maps

def get_location(seed: int, src_to_dest_maps: list[dict]) -> int:
    return list(get_locations([seed], src_to_dest_maps))[0]


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
    explicit_seed_ranges = get_explicit_seed_ranges(input_lines[0])
    src_to_dest_maps = get_maps(input_lines)
    curr_lowest_location = float('inf')
    for explicit_seed_range in explicit_seed_ranges:
        print(f'Checking seeds {explicit_seed_range}')
        first_seed_in_range = explicit_seed_range[0]
        # e.g. if we have (2, 2) then the final seed is 2 + 2 - 1 = 3
        final_seed_in_range = first_seed_in_range + explicit_seed_range[1] - 1
        for seed in range(first_seed_in_range, final_seed_in_range + 1):
            candidate_location = get_location(seed, src_to_dest_maps)
            if candidate_location < curr_lowest_location:
                curr_lowest_location = candidate_location
    print(f'Final answer: {curr_lowest_location}')

if __name__ == '__main__':
    main()