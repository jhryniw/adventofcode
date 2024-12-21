from dataclasses import dataclass
import math
import sys
sys.setrecursionlimit(100000)
with open("day10full.txt") as f:
    map = [l.strip() for l in f.readlines()]

s_pos = None
for i in range(len(map)):
    for j in range(len(map[i])):
        if map[i][j] == 'S':
            s_pos = (j, i)
            break

assert s_pos is not None

map_h = len(map)
map_w = len(map[0])

@dataclass
class PathSegment:
    c: str
    x: int
    y: int
    dir_x: int
    dir_y: int

    
for line in map:
    print(line)
print(s_pos)
print()
cont = False

for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    cur_x = s_pos[0] + dir[0]
    cur_y = s_pos[1] + dir[1]
    cur_dir_x = dir[0]
    cur_dir_y = dir[1]
    steps = 0
    fail = False
    path = [PathSegment(
        c='S', x=cur_x, y=cur_y, dir_x=cur_dir_x, dir_y=cur_dir_y
    )]

    while (cur_x, cur_y) != s_pos:
        if cur_x >= map_w or cur_y >= map_h or cur_x < 0 or cur_y < 0:
            fail = True
            break

        c = map[cur_y][cur_x]

        # print ((cur_x, cur_y), (cur_dir_x, cur_dir_y), c)
        path.append(PathSegment(
            c=c, x=cur_x, y=cur_y, dir_x=cur_dir_x, dir_y=cur_dir_y
        ))

        if c == '.':
            break
        elif c == "|":
            if cur_dir_y == 0:
                fail = True
                break
            cur_y += cur_dir_y
        elif c == "-":
            if cur_dir_x == 0:
                fail = True
                break
            cur_x += cur_dir_x
        elif c == "L":
            if cur_dir_x != -1 and cur_dir_y != 1:
                fail = True
                break
            if cur_dir_y == 1:
                cur_dir_x = 1
                cur_dir_y = 0
                cur_x += 1
            else:
                cur_dir_x = 0
                cur_dir_y = -1
                cur_y -= 1
        elif c == "J":
            if cur_dir_x != 1 and cur_dir_y != 1:
                fail = True
                break
            if cur_dir_y == 1:
                assert cur_dir_x == 0
                cur_dir_x = -1
                cur_dir_y = 0
                cur_x -= 1
            else:
                cur_dir_x = 0
                cur_dir_y = -1
                cur_y -= 1
        elif c == "7":
            if cur_dir_x != 1 and cur_dir_y != -1:
                fail = True
                break
            if cur_dir_y == -1:
                cur_dir_x = -1
                cur_dir_y = 0
                cur_x -= 1
            else:
                cur_dir_x = 0
                cur_dir_y = 1
                cur_y += 1
        elif c == "F":
            if cur_dir_x != -1 and cur_dir_y != -1:
                fail = True
                break
            if cur_dir_y == -1:
                cur_dir_x = 1
                cur_dir_y = 0
                cur_x += 1
            else:
                cur_dir_x = 0
                cur_dir_y = 1
                cur_y += 1
        elif c == "S":
            break

        steps += 1
    print("FAIL", cur_x, cur_y, c)
    print()

    if (cur_x, cur_y) == s_pos and not fail:
        cont = True
        break

if not cont:
    exit(1)

map_copy = [list(l) for l in map]

loop_positions = set([(p.x, p.y) for p in path])
loop_positions.add(s_pos)

for i in range(len(map_copy)):
    for j in range(len(map_copy[i])):
        if (j, i) not in loop_positions:
            map_copy[i][j] = '.'

def flood_fill(m, x, y):
    if x >= map_w or y >= map_h or x < 0 or y < 0:
        return
    if m[y][x] != '.':
        return
    m[y][x] = "I"

    for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        flood_fill(m, x + dir[0], y + dir[1])

for s in path:
    left = (s.x + s.dir_y, s.y - s.dir_x)
    right = (s.x - s.dir_y, s.y + s.dir_x)
    forward = (s.x + s.dir_x, s.y + s.dir_y)
    # flood_fill(map_copy, left[0], left[1])
    turns = []
    if s.c in "|-":
        turns.append(right)
    if s.c in 'L7' and s.dir_y != 0:
        turns.append(right)
        turns.append(forward)
    if s.c in 'JF' and s.dir_x != 0:
        turns.append(right)
        turns.append(forward)
    # if s.c in "JL":
    #     turns.append(right)
    #     turns.append(forward)
    # if s.c in "7F"

    for turn in turns:
        flood_fill(map_copy, turn[0], turn[1])

for l in map_copy:
    print(''.join(l))

i_count = 0
dot_count = 0
for l in map_copy:
    for c in l:
        if c == "I":
            i_count += 1
        if c == ".":
            dot_count += 1

for s in path[:5]:
    print(s)

print(i_count)
print(dot_count)
