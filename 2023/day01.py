# Part 1

# lines = []
# digits = {'0','1','2','3','4','5','6','7','8','9'}
# with open('day1.txt', 'r') as f:
#     for line in f:
#         lines.append(list(filter(lambda c: c in digits, line)))

# numbers = map(lambda l: int(f"{l[0]}{l[-1]}"), lines)
# print(sum(numbers))

# Part 2

digits = []
digits = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
}

def extract_digit(s: str, index: int) -> int:
    for length in [1, 3, 4, 5]:
        substr = s[index:index+length]
        if substr in digits:
            return digits[substr]
    return -1

line_digits = []
with open('day1_2.txt', 'r') as f:
    for line in f:
        digit_arr = []
        for i in range(len(line)):
            d = extract_digit(line, i)
            if d >= 0:
                digit_arr.append(d)
        line_digits.append(digit_arr)

numbers = map(lambda l: int(f"{l[0]}{l[-1]}"), line_digits)
print(sum(numbers))
