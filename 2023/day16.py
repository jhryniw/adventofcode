from collections import deque
from typing import List

with open("day16full.txt", "r") as f:
    grid = [line.strip() for line in f.readlines()]

rows = len(grid)
cols = len(grid[0])

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

def pipe_dirs(dir: int) -> List[int]:
    if dir in (UP, DOWN):
        return [dir]
    else:
        return [UP, DOWN]

def dash_dirs(dir: int) -> List[int]:
    if dir in (LEFT, RIGHT):
        return [dir]
    else:
        return [LEFT, RIGHT]

def fslash_dir(dir: int) -> int:
    # /
    if dir == RIGHT:
        return UP
    elif dir == UP:
        return RIGHT
    elif dir == LEFT:
        return DOWN
    else: # DOWN
        return LEFT

def bslash_dir(dir: int) -> int:
    # \
    if dir == RIGHT:
        return DOWN
    elif dir == UP:
        return LEFT
    elif dir == LEFT:
        return UP
    else: # DOWN
        return RIGHT

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

def show_energized(energized):
    g = [['.' for _ in range(cols)] for _ in range(rows)]
    for e in energized:
        g[e[0]][e[1]] = "#"
    
    for row in g:
        print(''.join(row))
    print()

def compute_energized(start):
    q = deque([start])
    seen = set([start])

    while len(q) > 0:
        cur, dir = q.popleft()
        cur_i, cur_j = cur

        if not in_bounds(cur_i, cur_j):
            continue

        ch = grid[cur_i][cur_j]
        if ch == ".":
            new_dirs = [dir]
        elif ch == "/":
            new_dirs = [fslash_dir(dir)]
        elif ch == "\\":
            new_dirs = [bslash_dir(dir)]
        elif ch == "|":
            new_dirs = pipe_dirs(dir)
        elif ch == "-":
            new_dirs = dash_dirs(dir)

        for d in new_dirs:
            new = (move_dir(cur_i, cur_j, d), d)
            if new not in seen:
                q.append(new)
                seen.add(new)
    
    unique_pos = set([i[0] for i in seen if in_bounds(i[0][0], i[0][1])])
    # show_energized(unique_pos)
    return len(unique_pos)

# part 1
print(compute_energized(((0, 0), RIGHT)))
print("--------")
# part 2
max_e = 0
for i in range(rows):
    start = ((i, 0), RIGHT)
    max_e = max(max_e, compute_energized(start))

    start = ((i, cols-1), LEFT)
    max_e = max(max_e, compute_energized(start))

for j in range(cols):
    start = ((0, j), DOWN)
    max_e = max(max_e, compute_energized(start))

    start = ((rows-1, j), UP)
    max_e = max(max_e, compute_energized(start))

print(max_e)
