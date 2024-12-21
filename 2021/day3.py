def b_to_num(b_array):
    return int(''.join(map(str, b_array)), 2)

with open('day3_input.txt', 'r') as num_file:
    nums = num_file.readlines()

# Part 1
nums = list(map(lambda l: l.strip(), nums))
ones = [0] * len(nums[0])

for n in nums:
    for i, c in enumerate(n):
        if c == '1':
            ones[i] += 1

half_total = len(nums) // 2
ones = list(map(lambda x: 1 if x > half_total else 0, ones))
zeros = list(map(lambda x: 1 if x == 0 else 0, ones))

gamma = b_to_num(ones)
epsilon = b_to_num(zeros)

print(gamma)
print(epsilon)

print(gamma * epsilon)

# Part 2

def func(num_array, strat):
    if strat == 'most':
        favored = lambda ones, zeros: '1' if ones >= zeros else '0'
    else:
        favored = lambda ones, zeros: '0' if ones >= zeros else '1'

    pos = 0
    while len(num_array) > 1:
        ones = 0
        for n in num_array:
            if n[pos] == '1':
                ones += 1
        
        zeros = len(num_array) - ones
        favored_bit = favored(ones, zeros)

        num_array = list(filter(lambda n: n[pos] == favored_bit, num_array))
        pos += 1
    
    assert(len(num_array) == 1)
    return num_array[0]

# new_nums = [
#     '00100',
#     '11110',
#     '10110',
#     '10111',
#     '10101',
#     '01111',
#     '00111',
#     '11100',
#     '10000',
#     '11001',
#     '00010',
#     '01010',
# ]

# print(int(func(new_nums, strat='most'), 2))
# print(int(func(new_nums, strat='least'), 2))

oxygen_rating = int(func(nums, strat='most'), 2)
co2_rating = int(func(nums, strat='least'), 2)

print(oxygen_rating)
print(co2_rating)

print(oxygen_rating * co2_rating)
