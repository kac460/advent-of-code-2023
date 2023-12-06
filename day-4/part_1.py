'''
The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, all with their opaque covering already scratched off. Picking one up, it looks like each card has two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have. You organize the information into a table (your puzzle input).

As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the list of winning numbers. The first match makes the card worth one point and each match after the first doubles the point value of that card.

For example:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86) are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three times for each of the three matches after the first).

    Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
    Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
    Card 4 has one winning number (84), so it is worth 1 point.
    Card 5 has no winning numbers, so it is worth no points.
    Card 6 has no winning numbers, so it is worth no points.

So, in this example, the Elf's pile of scratchcards is worth 13 points.

Take a seat in the large pile of colorful cards. How many points are they worth in total?
'''
_SAMPLE = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''

def get_input_lines(use_sample: bool) -> list[str]:
    if use_sample:
        return _SAMPLE.splitlines()
    with open('input.txt') as f:
        return f.readlines()
    

def points_for_card(card_line: str) -> int:
    winning_nums_str, your_nums_str = card_line.split(':')[1].split('|')
    winning_nums = set(num_str for num_str in winning_nums_str.split())
    your_nums = set(num_str for num_str in your_nums_str.split())
    val = 0
    for your_num in your_nums:
        if your_num in winning_nums:
            val = 1 if not val else val * 2
    return val 

assert points_for_card('Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53') == 8
assert points_for_card('Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83') == 1
assert points_for_card('Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36') == 0


def main() -> None:
    input_lines = get_input_lines(use_sample=False)
    answer = sum(points_for_card(line) for line in input_lines)
    print(f'FINAL ANSWER: {answer}')

if __name__ == '__main__':
    main()