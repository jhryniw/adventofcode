from collections import defaultdict

with open("day23full.txt", "r") as f:
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

# assert set([c[2] for c in compute_reach_coord(grid, 19, 19)]) == set([UP, LEFT, DOWN]), [c[2] for c in compute_reach_coord(grid, 19, 19)] 

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

def all_in_dirs_fn(i, adj):
    out = [opposite_dir[a[2]] for a in adj]
    if i == 0:
        out.append(DOWN)
    elif i == rows - 1:
        out.append(UP)
    if j == cols - 1:
        out.append(LEFT)
    elif j == 0:
        out.append(RIGHT)
    return out

for n in nodes:
    adj = compute_reach_coord(grid, n[0], n[1])
    all_in_dirs = set(all_in_dirs_fn(n[0], adj))
    # print("DIRS", adj, all_in_dirs)
    for a in adj:
        count = 1
        cur = a
        cur_pt = (cur[0], cur[1])
        while cur_pt not in nodes:
            nexts = compute_reach(grid, cur)
            assert len(nexts) == 1
            cur = nexts[0]
            cur_pt = (cur[0], cur[1])
            count += 1

        for dir in all_in_dirs - {opposite_dir[a[2]]}:
            # print((n[0], n[1], dir), cur, count)
            edges[(n[0], n[1], dir)][cur] = count

print(nodes)
print(edges)

print(edges[(0, 1, DOWN)])

# path_map = {
#     start: ({(start[0], start[1]): 0}, 0)
# }

# from collections import deque
# import heapq

max_dist_to_end = 0
longest_path = None
paths_tried = 0

q = [(0, start, {})]
while len(q) > 0:
    dist, cur, path = q.pop() # dfs
    # path, dist = path_map[cur]
    for next_cur, edge_cost in edges[cur].items():
        next_pt = (next_cur[0], next_cur[1])
        if next_pt not in path:
            new_d = dist + edge_cost
            new_path = path.copy()
            new_path[next_pt] = new_d
            q.append((new_d, next_cur, new_path))
            if next_pt == (end[0], end[1]):
                paths_tried += 1
                if new_d > max_dist_to_end:
                    max_dist_to_end = new_d
                    longest_path = new_path
                    print("NEW MAX", max_dist_to_end)

    if paths_tried > 0 and paths_tried % 10000 == 0:
        print(paths_tried)
            # _, d = path_map.get(next_cur, (set(), 0))
            # new_d = dist + edge_cost
            # if new_d > d:
            #     new_path = path.copy()
            #     new_path[next_pt] = new_d
            #     path_map[next_cur] = (new_path, new_d)
            #     heapq.heappush(q, (-new_d, next_cur))

# longest_path, dist = path_map[(rows-1, cols-2, DOWN)]

for i in range(rows):
    row = []
    for j in range(cols):
        if (i, j) in longest_path:
            # _, d = path_map[]
            row.append(str(longest_path[(i, j)]))
        else:
            row.append(grid[i][j])
    print(''.join(row))
print()

print(longest_path)
print(dist)

# print(len(path_map[(rows-1, cols-2, DOWN)]) - 1)
