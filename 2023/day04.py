matches = []

with open("day04full2.txt") as f:
    for line in f:
        winning_numbers_str, numbers_str = line.split(":")[1].strip().split(" | ")
        
        winning_numbers = [s.strip() for s in winning_numbers_str.split(" ") if len(s)]
        numbers = [s.strip() for s in numbers_str.split(" ") if len(s)]
        winning_numbers = set(map(int, winning_numbers))
        numbers = set(map(int, numbers))

        match = winning_numbers & numbers
        matches.append(len(match))

        # if len(match) >= 1:
        #     sum += 2 ** (len(match) - 1)

copies = [1] * len(matches)
total = len(matches)
for i, match in enumerate(matches):
    card_copies = copies[i]
    for j in range(i+1, min(total, i+match+1)):
        copies[j] += card_copies

print(sum(copies))
