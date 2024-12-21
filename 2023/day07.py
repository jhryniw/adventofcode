# from functools import cmp_to_key
import functools

val_dict = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

hands = []
bets = []

with open("day07full.txt") as f:
    for line in f:
        hand, bet = line.strip().split(" ")
        hands.append(tuple([val_dict[v] for v in hand]))
        bets.append(int(bet))

def strength(hand):
    assert len(hand) == 5
    counter = [0] * 15
    for c in hand:
        if c >= 2:
            counter[c] += 1

    num_jokers = sum([c == 1 for c in hand])
    m = max(counter)
    for i in range(len(counter)):
        if counter[i] == m:
            counter[i] += num_jokers
            break
    
    if any([c == 5 for c in counter]):
        return 7
    if any([c == 4 for c in counter]):
        return 6
    if any([c == 3 for c in counter]) and any([c == 2 for c in counter]):
        return 5
    if any([c == 3 for c in counter]):
        return 4
    if sum([c == 2 for c in counter]) == 2:
        return 3
    if any([c == 2 for c in counter]):
        return 2
    # if all([c <= 1 for c in counter]):
    return 0

def compare(hand1, hand2):
    s1 = strength(hand1)
    s2 = strength(hand2)
    if s1 != s2:
        return s1 - s2
    for val1, val2 in zip(hand1, hand2):
        if val1 != val2:
            return val1 - val2
    
    return 0

sorted_hands = sorted(hands, key=functools.cmp_to_key(compare))
ranks = dict([(hand, rank + 1) for rank, hand in enumerate(sorted_hands)])
assert len(ranks.keys()) == len(sorted_hands)
# print(ranks)
print([(hand, strength(hand)) for hand in hands])

# for rank, hand in 

print(sorted_hands[200:])

sum = 0
for hand, bet in zip(hands, bets):
    sum += (ranks[hand] * bet)
print(sum)
