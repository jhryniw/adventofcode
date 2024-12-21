from collections import defaultdict

probs = []

with open('day8_input.txt', 'r') as f:
    for line in f:
        input_s, output_s = line.strip().split(' | ')
        probs.append((input_s.split(' '), output_s.split(' ')))

# probs = [(
#     ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'],
#     ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf']
# )]

# part 1
count = 0

for prob in probs:
    for digit_segments in prob[1]:
        # 1, 4, 7, 8
        if len(digit_segments) == 2 or len(digit_segments) == 4 or \
           len(digit_segments) == 3 or len(digit_segments) == 7:
            count += 1

print(count)


def find_pattern_with_length(patterns, length):
    for p in patterns:
        if len(p) == length:
            return p
    assert(False)


def find_letter_with_count(letter_counts, count):
    for k,v in letter_counts.items():
        if v == count:
            return set(k)
    assert(False)

def to_lookup(pattern):
    return ''.join(sorted(list(pattern)))

total = 0

# part 2
for prob in probs:
    # Determine the patterns for 1,4,7,8
    prob_input = list(map(lambda s: set(list(s)), prob[0]))
    prob_input_str = ''.join(prob[0])
    letter_counts = defaultdict(int)
    for letter in prob_input_str:
        letter_counts[letter] += 1

    one = find_pattern_with_length(prob_input, 2)
    four = find_pattern_with_length(prob_input, 4)
    seven = find_pattern_with_length(prob_input, 3)
    eight = find_pattern_with_length(prob_input, 7)

    # a = 7 - 1
    a = seven - one

    # b = 6 times
    b = find_letter_with_count(letter_counts, 6)
    # e = 4 times
    e = find_letter_with_count(letter_counts, 4)
    # f = 9 times
    f = find_letter_with_count(letter_counts, 9)

    # g = 8 - 4 - a - e
    g = eight - four - a - e
    # c = 1 - f
    c = one - f

    # d = 8 - a - b - c - e - f - g
    d = eight - a - b - c - e - f - g

    zero = eight - d
    two = eight - b - f
    three = eight - b - e
    six = eight - c
    five = six - e
    nine = eight - e

    lookup = dict([
        (to_lookup(zero), '0'),
        (to_lookup(one), '1'),
        (to_lookup(two), '2'),
        (to_lookup(three), '3'),
        (to_lookup(four), '4'),
        (to_lookup(five), '5'),
        (to_lookup(six), '6'),
        (to_lookup(seven), '7'),
        (to_lookup(eight), '8'),
        (to_lookup(nine), '9')
    ])

    prob_output = list(map(lambda s: set(list(s)), prob[1]))
    result = int(''.join(map(lambda p: lookup[to_lookup(p)], prob_output)))
    total += result

print(total)
