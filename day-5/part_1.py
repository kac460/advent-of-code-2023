'''
The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
'''
from collections import namedtuple
DestObj = namedtuple('DestObj', ['dest_start', 'range_length'])

_SAMPLE = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
_MAP_NAMES = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location'
]

def get_input_lines(use_sample) -> list[str]:
    if use_sample:
        return _SAMPLE.splitlines()
    with open('day-5/input.txt') as f:
        return [line.strip() for line in f.readlines()]


def source_to_destination_map(map_name: str, input_lines: list[str]) -> dict:
    header_index = input_lines.index(f'{map_name} map:')
    src_to_dest_map = {}
    for line in input_lines[header_index+1:]:
        if 'map' in line or not line.strip():  # start of next map / end of input
            break
        dest, src, range_length = (int(num_str) for num_str in line.split())
        src_to_dest_map[src] = DestObj(dest, range_length)
    return src_to_dest_map


def get_destination(src_to_destination_map: dict[int, DestObj], src: int) -> int:
    for map_src, dest_obj in src_to_destination_map.items():
        range_length = dest_obj.range_length
        if src >= map_src and src <= map_src + range_length:
          return dest_obj.dest_start + (src - map_src)
    return src

def test_get_destination():
    src_to_dest_map = {
        50: DestObj(dest_start=52, range_length=48),
        98: DestObj(dest_start=50, range_length=2)
    }
    ret = get_destination(src_to_dest_map, 49) 
    assert ret == 49
    ret = get_destination(src_to_dest_map, 50)
    assert ret ==  52
    assert get_destination(src_to_dest_map, 97) == 99

test_get_destination()

def get_maps(input_lines: list[str]) -> list[dict]:
    return [
        source_to_destination_map(map_name, input_lines)
        for map_name in _MAP_NAMES
    ]

def get_seeds(seed_line: str) -> list[int]:
    return [int(seed) for seed in seed_line.split(':')[1].split()]
assert get_seeds('seeds: 79 14 55 13') == [79, 14, 55, 13]

def get_locations(seeds: list[int], src_to_dest_maps: list[dict]) -> set[int]:
    locations = set()
    for seed in seeds:
        src = seed
        for src_to_dest_map in src_to_dest_maps:
            src = get_destination(src_to_dest_map, src)
        # at end, src is a location
        # print(f'Location for {seed} is {src}')
        locations.add(src)
    return locations
# l = locations(get_input_lines(use_sample=True))
# assert l == {35, 82, 43, 86}

def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    seeds = get_seeds(input_lines[0])
    seed_locations = get_locations(seeds, src_to_dest_maps=get_maps(input_lines))
    print(f'Final answer: {min(seed_locations)}')

if __name__ == '__main__':
    main()