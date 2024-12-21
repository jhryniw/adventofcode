import heapq
from typing import List

with open("day17full.txt", "r") as f:
    heatmap = [list(map(int, l.strip())) for l in f.readlines()]

# for row in heatmap:
#     print(row)

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

rows = len(heatmap)
cols = len(heatmap[0])

def heuristic(i, j) -> int:
    # naive
    return (rows - i - 1) + (cols - j - 1)

def turn_dirs(dir: int) -> List[int]:
    if dir in (LEFT, RIGHT):
        return [UP, DOWN]
    else:
        return [LEFT, RIGHT]

def dir_ch(dir: int) -> List[int]:
    if dir == RIGHT:
        return ">"
    elif dir == UP:
        return "^"
    elif dir == LEFT:
        return "<"
    else: # DOWN
        return "v"

def move_dir(i, j, dir):
    if dir == RIGHT:
        return (i, j+1)
    elif dir == UP:
        return (i-1, j)
    elif dir == LEFT:
        return (i, j-1)
    else: # DOWN
        return (i+1, j)

def in_bounds(i, j):
    return 0 <= i < rows and 0 <= j < cols    

# costmap = [[0 for _ in range(cols)] for _ in range(rows)]
seen = dict()
q = [(0, 0, 0, RIGHT, (0, 0))]

result = 0

while len(q) > 0:
    e = heapq.heappop(q)
    # print(e)
    o_cost, cost, consecutive_straights, dir, pos = e
    prev_key = (consecutive_straights, dir, pos)
    cur_i, cur_j = pos

    if pos == (rows-1, cols-1):
        # Found!
        result = cost
        break
    
    options = []
    if consecutive_straights < 10:
        new_pos = move_dir(cur_i, cur_j, dir)
        if in_bounds(new_pos[0], new_pos[1]):
            new_cost = cost + heatmap[new_pos[0]][new_pos[1]]
            new_ocost = new_cost + heuristic(new_pos[0], new_pos[1])
            options.append((new_ocost, new_cost, consecutive_straights + 1, dir, new_pos))
    
    if consecutive_straights >= 4:
        for new_dir in turn_dirs(dir):
            new_pos = move_dir(cur_i, cur_j, new_dir)
            if in_bounds(new_pos[0], new_pos[1]):
                new_cost = cost + heatmap[new_pos[0]][new_pos[1]]
                new_ocost = new_cost + heuristic(new_pos[0], new_pos[1])
                options.append((new_ocost, new_cost, 1, new_dir, new_pos))
    
    for option in options:
        # (consecutive_straights, dir, pos)
        option_key = (option[2], option[3], option[4])
        min_cost = seen.get(option_key, (1e9, None))[0]
        if option[0] < min_cost:
            seen[option_key] = (option[1], prev_key)
            heapq.heappush(q, option)

    # print(len(q))
            
for key in seen:
    if key[2] == (rows-1, cols-1):
        start_key = key
        break

cur_key = start_key
while cur_key[2] != (0, 0):
    cur_pos = cur_key[2]
    heatmap[cur_pos[0]][cur_pos[1]] = dir_ch(cur_key[1])
    cur_key = seen[cur_key][1]

for row in heatmap:
    print(''.join(map(str, row)))

print(result)
