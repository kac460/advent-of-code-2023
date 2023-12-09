'''
Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
'''
from typing import NamedTuple
from functools import cmp_to_key

class Play(NamedTuple):
    hand: tuple[int, int, int, int, int]
    bid: int

def get_input_lines(use_sample: bool) -> list[str]:
    filename = 'sample.txt' if use_sample else 'input.txt'
    with open(f'day-7/{filename}') as f:
        return f.readlines()

_JOKER_VAL = 1
_CARD_TO_VALUE = {
    'J': _JOKER_VAL,
    **{str(i): i for i in range(2, 10)},
    'T': 10,
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
        Play(hand=(10, 5, 5, 1, 5), bid=684), 
        Play(hand=(13, 13, 6, 7, 7), bid=28), 
        Play(hand=(13, 10, 1, 1, 10), bid=220), 
        Play(hand=(12, 12, 12, 1, 14), bid=483)
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
    num_jokers = 0
    for label in hand:
        if label == _JOKER_VAL:
            num_jokers += 1
        else:
            label_counts[label] = label_counts.get(label, 0) + 1
    


    
    sorted_counts = list(sorted(label_counts.values()))
    # Fact: We want J to be whatever label we have the most of
    if len(sorted_counts) == 0: # edge case: all jokers
        return FIVE_OF_A_KIND
    sorted_counts[-1] += num_jokers
    if len(label_counts) == 1: # 5 of a kind
        return FIVE_OF_A_KIND
    
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
        
        