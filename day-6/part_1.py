'''
For example:

Time:      7  15   30
Distance:  9  40  200

This document describes three races:

    The first race lasts 7 milliseconds. The record distance in this race is 9 millimeters.
    The second race lasts 15 milliseconds. The record distance in this race is 40 millimeters.
    The third race lasts 30 milliseconds. The record distance in this race is 200 millimeters.

Your toy boat has a starting speed of zero millimeters per millisecond. For each whole millisecond you spend at the beginning of the race holding down the button, the boat's speed increases by one millimeter per millisecond.

So, because the first race lasts 7 milliseconds, you only have a few options:

    Don't hold the button at all (that is, hold it for 0 milliseconds) at the start of the race. The boat won't move; it will have traveled 0 millimeters by the end of the race.
    Hold the button for 1 millisecond at the start of the race. Then, the boat will travel at a speed of 1 millimeter per millisecond for 6 milliseconds, reaching a total distance traveled of 6 millimeters.
    Hold the button for 2 milliseconds, giving the boat a speed of 2 millimeters per millisecond. It will then get 5 milliseconds to move, reaching a total distance of 10 millimeters.
    Hold the button for 3 milliseconds. After its remaining 4 milliseconds of travel time, the boat will have gone 12 millimeters.
    Hold the button for 4 milliseconds. After its remaining 3 milliseconds of travel time, the boat will have gone 12 millimeters.
    Hold the button for 5 milliseconds, causing the boat to travel a total of 10 millimeters.
    Hold the button for 6 milliseconds, causing the boat to travel a total of 6 millimeters.
    Hold the button for 7 milliseconds. That's the entire duration of the race. You never let go of the button. The boat can't move until you let go of the button. Please make sure you let go of the button so the boat gets to move. 0 millimeters.

Since the current record for this race is 9 millimeters, there are actually 4 different ways you could win: you could hold the button for 2, 3, 4, or 5 milliseconds at the start of the race.

In the second race, you could hold the button for at least 4 milliseconds and at most 11 milliseconds and beat the record, a total of 8 different ways to win.

In the third race, you could hold the button for at least 11 milliseconds and no more than 19 milliseconds and still beat the record, a total of 9 ways you could win.

To see how much margin of error you have, determine the number of ways you can beat the record in each race; in this example, if you multiply these values together, you get 288 (4 * 8 * 9).

Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?
'''
import math
from typing import NamedTuple

class Race(NamedTuple):
    time: int
    record_distance: int

SAMPLE = '''Time:      7  15   30
Distance:  9  40  200'''

def get_races(use_sample: bool) -> list[Race]:
    if use_sample:
        input_lines = SAMPLE.splitlines()
    else: 
        with open('day-6/input.txt') as f:
            input_lines = f.readlines()
    times = input_lines[0].split()[1:]
    record_distances = input_lines[1].split()[1:]
    assert len(times) == len(record_distances)
    return [
        Race(time=int(times[i]), record_distance=int(record_distances[i]))
        for i in range(len(times))
    ]

def test_get_races() -> None:
    assert get_races(use_sample=True) == [
        Race(time=7, record_distance=9), 
        Race(time=15, record_distance=40), 
        Race(time=30, record_distance=200)
    ]
test_get_races()

def num_ways_to_win_race(race: Race) -> int:
    num_ways = 0
    for hold_time in range(1, race.time):
        time_spent_moving = race.time - hold_time
        dist = time_spent_moving * hold_time
        if dist > race.record_distance:
            num_ways += 1
    return num_ways

def test_num_ways_to_win_race() -> None:
    races = get_races(use_sample=True)
    assert num_ways_to_win_race(races[0]) == 4
test_num_ways_to_win_race()

def main() -> None:
    races = get_races(use_sample=False)
    answer = math.prod(num_ways_to_win_race(race) for race in races)
    print(f'Final answer: {answer}')

if __name__ == '__main__':
    main()
