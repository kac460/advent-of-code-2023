'''
There's really only one race - ignore the spaces between the numbers on each line.

So, the example from before:

Time:      7  15   30
Distance:  9  40  200

...now instead means this:

Time:      71530
Distance:  940200

Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!

How many ways can you beat the record in this one much longer race?
'''
from part_1 import Race, num_ways_to_win_race, SAMPLE

def get_race(use_sample: bool) -> Race:
    if use_sample:
        input_lines = SAMPLE.splitlines()
    else: 
        with open('day-6/input.txt') as f:
            input_lines = f.readlines()
    time = int(input_lines[0].split(':')[1].replace(' ', ''))
    dist = int(input_lines[1].split(':')[1].replace(' ', ''))
    return Race(time=time, record_distance=dist)
assert get_race(use_sample=True) == Race(
    time=71530,
    record_distance=940200
)

def main() -> None:
    race = get_race(use_sample=False)
    answer = num_ways_to_win_race(race)
    print(f'Final answer: {answer}')

if __name__ == '__main__':
    main()
