'''
Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
'''
from typing import NamedTuple
from functools import cmp_to_key
from enum import Enum

class Play(NamedTuple):
    hand: tuple[int, int, int, int, int]
    bid: int

def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample.txt' if use_sample else 'input.txt'
    with open(f'day-7/{filename}') as f:
        return f.readlines()

_CARD_TO_VALUE = {
    **{str(i): i for i in range(2, 10)},
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}
def get_plays(use_sample: bool) -> list[Play]:
    input_plays = [line.split() for line in get_input_lines(use_sample)]
    return [
        Play(
            hand=tuple(
                _CARD_TO_VALUE[input_play[0][i]] 
                for i in range(len(input_play[0]))
            ),
            bid=int(input_play[1])
        )
        for input_play in input_plays
    ]

def test_get_plays() -> None:
    assert get_plays(use_sample=True) == [
        Play(hand=(3, 2, 10, 3, 13), bid=765), 
        Play(hand=(10, 5, 5, 11, 5), bid=684), 
        Play(hand=(13, 13, 6, 7, 7), bid=28), 
        Play(hand=(13, 10, 11, 11, 10), bid=220), 
        Play(hand=(12, 12, 12, 11, 14), bid=483)
    ]
    print('test_get_plays PASSED')
test_get_plays()


FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

def type_strength(hand: tuple[int, int, int, int, int]) -> int:
    label_counts = {}
    for label in hand:
        label_counts[label] = label_counts.get(label, 0) + 1
    
    if len(label_counts) == 1: # 5 of a kind
        return FIVE_OF_A_KIND
    
    sorted_counts = list(sorted(label_counts.values()))
    if len(sorted_counts) == 2: # either full house or 4 of a kind
        if sorted_counts[0] == 1:  # XYYYY
            return FOUR_OF_A_KIND  # four of a kind
        return FULL_HOUSE  # XXYYY full house
    
    if len(sorted_counts) == 3: # either 2-pair of 3 of a kind
        if sorted_counts[1] == 1: # XYZZZ
            return THREE_OF_A_KIND
        return TWO_PAIR  # XYYZZ
    
    if len(sorted_counts) == 4:  # MNLOO
        return ONE_PAIR
    
    return HIGH_CARD



def cmp_plays(play_1: Play, play_2: Play) -> int:
    hand_1 = play_1.hand
    hand_2 = play_2.hand

    hand_1_type_strength = type_strength(hand_1)
    hand_2_type_strength = type_strength(hand_2)
    if hand_1_type_strength > hand_2_type_strength:
        return 1
    if hand_1_type_strength < hand_2_type_strength:
        return -1
    
    for i in range(len(hand_1)):
        if hand_1[i] > hand_2[i]:
            return 1
        if hand_1[i] < hand_2[i]:
            return -1
    print(f'{hand_1} == {hand_2}!')
    return 0

def main() -> None:
    plays = get_plays(use_sample=False)
    sorted_plays = sorted(
        plays,
        key=cmp_to_key(cmp_plays)
    )
    answer = sum(
        rank * sorted_plays[rank - 1].bid
        for rank in range(1, len(sorted_plays) + 1)
    )
    print(f'Final answer: {answer}')

if __name__ == '__main__':
    main()
        
        