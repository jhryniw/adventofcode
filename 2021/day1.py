from collections import deque

with open('/Users/james.hryniw/adventofcode2021/day_1_input.txt', 'r') as depth_file:
    depths = map(int, depth_file.readlines())

# Part A
inc = 0
for i in range(1, len(depths)):
    if depths[i] > depths[i-1]:
        inc += 1

print(inc)    

# Part B
q = deque(depths[:3])
rolling_depth = sum(depths[:3])

inc = 0
for i in range(1, len(depths)-2):
    new_rolling = rolling_depth + depths[i+2] - q[0]
    q.popleft()
    q.append(depths[i+2])
    if new_rolling > rolling_depth:
        inc += 1
    rolling_depth = new_rolling

print(inc)
