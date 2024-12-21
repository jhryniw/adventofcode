with open("day23full.txt", "r") as f:
    grid = [line.strip() for line in f.readlines()]

RIGHT = 0
LEFT = 2
UP = 3
DOWN = 1

rows = len(grid)
cols = len(grid[0])
start = (0, 1, DOWN)

opposite_dir = {
    RIGHT: LEFT,
    LEFT: RIGHT,
    UP: DOWN,
    DOWN: UP
}

acceptable_dirs = {
    ".": {DOWN, UP, LEFT, RIGHT},
    "<": {LEFT},
    ">": {RIGHT},
    "^": {UP},
    "v": {DOWN},
}

def compute_reach(g, pos):
    i, j, dir = pos
    out = []
    o_dir = opposite_dir[dir]

    for i2, j2, dir2 in [(i+1, j, DOWN), (i-1, j, UP), (i, j+1, RIGHT), (i, j-1, LEFT)]:
        if dir2 != o_dir and 0 <= i2 < rows and 0 <= j2 < cols and g[i2][j2] in ".<>^v":
            out.append((i2,j2,dir2))
    return out

assert compute_reach(grid, start) == [(1,1,DOWN)]

path_map = {
    start: set([(start[0], start[1])])
}

from collections import deque

q = deque([start])
while len(q) > 0:
    cur = q.popleft()
    path = path_map[cur]
    dist = len(path)
    reach = compute_reach(grid, cur)
    for r in reach:
        r_coord = (r[0], r[1])
        if r_coord not in path:
            d = len(path_map.get(r, []))
            if dist + 1 > d:
                path_map[r] = path | {(r[0], r[1])}
                q.append(r)

longest_path = path_map[(rows-1, cols-2, DOWN)]

for i in range(rows):
    row = []
    for j in range(cols):
        if (i, j) in longest_path:
            row.append("O")
        else:
            row.append(grid[i][j])
    print(''.join(row))
print()

print(len(path_map[(rows-1, cols-2, DOWN)]) - 1)

from collections import defaultdict

with open("day23test.txt", "r") as f:
    grid = [line.strip() for line in f.readlines()]

RIGHT = 0
LEFT = 2
UP = 3
DOWN = 1

rows = len(grid)
cols = len(grid[0])
start = (0, 1, DOWN)
end = (rows-1, cols-2, DOWN)

nodes = {(start[0], start[1]), (end[0], end[1])}
edges = defaultdict(dict)

def compute_reach_coord(g, i, j):
    out = []
    for i2, j2, dir2 in [(i+1, j, DOWN), (i-1, j, UP), (i, j+1, RIGHT), (i, j-1, LEFT)]:
        if 0 <= i2 < rows and 0 <= j2 < cols and g[i2][j2] in ".<>^v":
            out.append((i2,j2,dir2))
    return out

assert [c[2] for c in compute_reach_coord(grid, 19, 19)] == [UP, LEFT, RIGHT]

for i in range(rows):
    for j in range(cols):
        if grid[i][j] in ".<>^v":
            available_outs = compute_reach_coord(grid, i, j)
            if len(available_outs) > 2:
                nodes.add((i,j)) 

opposite_dir = {
    RIGHT: LEFT,
    LEFT: RIGHT,
    UP: DOWN,
    DOWN: UP
}

def compute_reach(g, pos):
    i, j, dir = pos
    out = []
    o_dir = opposite_dir[dir]

    for i2, j2, dir2 in [(i+1, j, DOWN), (i-1, j, UP), (i, j+1, RIGHT), (i, j-1, LEFT)]:
        if dir2 != o_dir and 0 <= i2 < rows and 0 <= j2 < cols and g[i2][j2] in ".<>^v":
            out.append((i2,j2,dir2))
    return out

assert compute_reach(grid, start) == [(1,1,DOWN)]

for n in nodes:
    adj = compute_reach_coord(grid, n[0], n[1])
    if n[0] == 19 and n[1] == 19:
        print("hi")
        print(adj)
    for a in adj:
        count = 0
        cur = a
        cur_pt = (cur[0], cur[1])
        while cur_pt not in nodes:
            nexts = compute_reach(grid, cur)
            assert len(nexts) == 1
            cur = nexts[0]
            cur_pt = (cur[0], cur[1])
            count += 1
        edges[(n[0], n[1], a[2])][cur] = count

print(nodes)
print(edges)

assert edges[(19, 19, 1)] == (22, 21, 1): 4

path_map = {
    start: (set([(start[0], start[1])]), 0)
}

from collections import deque

q = deque([start])
while len(q) > 0:
    cur = q.popleft()
    print(cur)
    path, dist = path_map[cur]
    for next_cur, edge_cost in edges[cur].items():
        next_pt = (next_cur[0], next_cur[1])
        if next_pt not in path:
            _, d = path_map.get(next_cur, (set(), 0))
            if dist + edge_cost > d:
                path_map[next_cur] = (path | {next_pt}, dist + edge_cost)
                q.append(next_cur)

longest_path = path_map[(rows-1, cols-2, DOWN)]

for i in range(rows):
    row = []
    for j in range(cols):
        if (i, j) in longest_path:
            row.append("O")
        else:
            row.append(grid[i][j])
    print(''.join(row))
print()

print(len(path_map[(rows-1, cols-2, DOWN)]) - 1)
