import math

with open("day10full.txt") as f:
    map = [l.strip() for l in f.readlines()]

s_pos = None
for i in range(len(map)):
    for j in range(len(map[i])):
        if map[i][j] == 'S':
            s_pos = (j, i)
            break

assert s_pos is not None

map_w = len(map)
map_h = len(map[0])

# @dataclass
# class Pipe:
#     c: str
    
for line in map:
    print(line)
print(s_pos)
print()

for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    cur_x = s_pos[0] + dir[0]
    cur_y = s_pos[1] + dir[1]
    cur_dir_x = dir[0]
    cur_dir_y = dir[1]
    steps = 0
    fail = False
    while (cur_x, cur_y) != s_pos:
        if cur_x >= map_w or cur_y >= map_h or cur_x < 0 or cur_y < 0:
            fail = True
            break

        c = map[cur_y][cur_x]

        print ((cur_x, cur_y), (cur_dir_x, cur_dir_y), c)

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
    print()

    if (cur_x, cur_y) == s_pos:
        print(steps, math.ceil(steps / 2))
        break

