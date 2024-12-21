from dataclasses import dataclass
import math
from typing import Tuple
import sys
sys.setrecursionlimit(100000)

RIGHT = 0
LEFT = 2
UP = 3
DOWN = 1

d_map = {
    "U": UP,
    "L": LEFT,
    "D": DOWN,
    "R": RIGHT
}

def move_dir(i, j, dir, dist=1):
    if dir == RIGHT:
        return (i, j+dist)
    elif dir == UP:
        return (i-dist, j)
    elif dir == LEFT:
        return (i, j-dist)
    else: # DOWN
        return (i+dist, j)

@dataclass
class PathSegment:
    pos: Tuple[int, int]
    dir: int
    dist: int
    color: str

hex_map = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
}

def get_hex(h: str) -> int:
    total = 0
    for i, d in enumerate(reversed(h)):
        total += hex_map[d] * (16 ** i)
    return total

with open("day18full.txt") as f:
    path = []
    cur_pos = (0, 0)
    for line in f:
        line = line.strip()
        dir_str, dist_str, color = line.split(" ")
        # dir = d_map[dir_str]
        # dist = int(dist_str)

        dist_hex = color[2:7]
        dir_hex = color[7]
        dir = int(dir_hex)
        dist = get_hex(dist_hex)

        path.append(PathSegment(
            pos=cur_pos,
            dir=dir,
            dist=dist,
            color=color
        ))
        cur_pos = move_dir(cur_pos[0], cur_pos[1], dir, dist)

print(path)

assert cur_pos == (0, 0)
print(path)

min_i = min([p.pos[0] for p in path])
min_j = min([p.pos[1] for p in path])

for p in path:
    p.pos = (p.pos[0] - min_i, p.pos[1] - min_j)

cols = max([p.pos[1] for p in path]) + 1
rows = max([p.pos[0] for p in path]) + 1

area = 0
for p in path:
    if p.dir == RIGHT:
        area -= (p.dist * p.pos[0]) 
    elif p.dir == LEFT:
        area += p.dist * (p.pos[0] + 1)
    elif p.dir == UP:
        area += p.dist
    # This will double count
    # elif p.dir == DOWN:
    #     print("DOWN", p.dist)
    #     area += p.dist

# Need to count the original square
print(area + 1)
# grid = [['.' for _ in range(cols)] for _ in range(rows)]

# for row in grid:
#     print(''.join(row))
# print()

# for p in path:
#     print(p.pos)
#     grid[p.pos[0]][p.pos[1]] = "#"

# def flood_fill(m, i, j):
#     if i >= rows or j >= cols or i < 0 or j < 0:
#         return
#     if m[i][j] != '.':
#         return
#     m[i][j] = "#"

#     for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#         flood_fill(m, i + dir[0], j + dir[1])

# def right_dir(dir: int) -> int:
#     if dir == UP:
#         return RIGHT
#     elif dir == RIGHT:
#         return DOWN
#     elif dir == DOWN:
#         return LEFT
#     else: # LEFT
#         return UP

# for p in path:
#     right_pos = move_dir(p.pos[0], p.pos[1], right_dir(p.dir))
#     flood_fill(grid, right_pos[0], right_pos[1])

# total = 0
# for row in grid:
#     total += sum([e == "#" for e in row])

# for row in grid:
#     print(''.join(row))

# print(total)
