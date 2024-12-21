start = None

with open("day21full.txt", "r") as f:
    grid = [line.strip() for line in f.readlines()]
    for i, l in enumerate(grid):
        if "S" in l:
            for j, c in enumerate(l):
                if c == "S":
                    start = (i, j)
                    break
            grid[i] = l.replace("S", ".")

assert start is not None

rows = len(grid)
cols = len(grid[0])

def reachable_p1(g, i, j):
    out = []
    for i2, j2 in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
        if 0 <= i2 < rows and 0 <= j2 < cols and g[i2][j2] == ".":
            out.append((i2,j2))
    return out

reach_setp1 = {}
for i, row in enumerate(grid):
    for j, c in enumerate(row):
        if c == ".":
            reach_setp1[(i, j)] = set(reachable_p1(grid, i, j))

def run_steps_p1(start, num_steps: int):
    cur = {start}
    for _ in range(num_steps):
        new = set()
        for pos in cur:
            new |= reach_setp1[pos]
        cur = new
    return len(cur) 

def reachable_p2(g, i, j):
    out = []
    for i2, j2 in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
        tile_diff_i = 0
        tile_diff_j = 0
        if i2 >= rows:
            tile_diff_i = 1
            i2 = 0
        elif i2 < 0:
            tile_diff_i = -1
            i2 = rows - 1

        if j2 >= cols:
            tile_diff_j = 1
            j2 = 0
        elif j2 < 0:
            tile_diff_j = -1
            j2 = cols - 1
        
        if g[i2][j2] == ".":
            out.append((i2, j2, tile_diff_i, tile_diff_j))

    return out

reach_set = {}
for i, row in enumerate(grid):
    for j, c in enumerate(row):
        if c == ".":
            reach_set[(i, j)] = reachable_p2(grid, i, j)

def run_steps(s: tuple, num_steps: int) -> int:
    cur = {(s[0], s[1], 0, 0)}
    for _ in range(num_steps):
        new = set()
        for pos in cur:
            reach = set([(r[0], r[1], pos[2] + r[2], pos[3] + r[3]) for r in reach_set[(pos[0], pos[1])]])
            new |= reach
        cur = new
    return len(cur)

# print(6, run_steps(start, 6))
# print(10, run_steps(start, 10))
# print(50, run_steps(start, 50))
# print(100, run_steps(start, 100))
# print(len(cur))

dist_map = {
    start: 0
}
cur = {start}
step = 1
while cur:
    new = set()
    for pos in cur:
        reach = [(r[0], r[1]) for r in reach_set[(pos[0], pos[1])]]
        for r in reach:
            if r not in dist_map:
                dist_map[r] = step
                new.add(r)
    cur = new
    step += 1

def poly_method(num_steps: int) -> int:
    half_dist = (rows-1)/2
    assert half_dist == int(half_dist)
    half_dist = int(half_dist)

    # Precondition
    # assert num_steps % 2 == 1

    n = (num_steps - half_dist) / rows
    print("N", n, half_dist, rows)
    assert n == int(n)

    n = int(n)

    full_even = sum([d % 2 == 0 for d in dist_map.values()])
    full_odd = sum([d % 2 == 1 for d in dist_map.values()])

    odd_corners = full_odd - run_steps_p1(start, half_dist)
    # even_corners = run_steps_p1(start, half_dist - 1)
    
    # odd_corners = sum([d % 2 == 1 for d in filter(lambda d: d > half_dist, dist_map.values())])
    even_corners = sum([d % 2 == 0 for d in filter(lambda d: d > half_dist, dist_map.values())]) - 1
    # print(full_even, full_odd, odd_corners, even_corners)

    # print(32781 - full_even - (4 * full_odd) + 2 * odd_corners)

    # 26501365
    return ((n + 1) * (n + 1) * full_odd) + (n * n * full_even) - ((n + 1) * odd_corners) + (n * even_corners)

def full_odd():
    return sum([d % 2 == 1 for d in dist_map.values()])

def odd_corners():
    half_dist = (rows-1)/2
    return sum([d % 2 == 1 for d in filter(lambda d: d > half_dist - 1, dist_map.values())])


# assert odd_corners() == 3648, odd_corners()
# print(run_steps_p1(start, 65))
# print(run_steps(start, 196))
# print(run_steps_p1())
assert poly_method(65) == run_steps_p1(start, 65), poly_method(65)
assert poly_method(196) == 32781, poly_method(196)
assert poly_method(327) == 90972, poly_method(327)

print(poly_method(26501365))
# for test in (196 + 131,):

    # print(test, run_steps(start, test))
    # print(poly_method(test))

# print(step)

# count_grid = [[-1 for _ in range(cols)] for _ in range(rows)]
# for pos, d in dist_map.items():
#     count_grid[pos[0]][pos[1]] = d
# for row in count_grid:
#     print(row)
# print()


# full_even = sum([d % 2 == 0 for d in dist_map.values()])
# full_odd = sum([d % 2 == 1 for d in dist_map.values()])
# print(full_even, full_odd)


# odd_corners = sum([d % 2 == 0 for d in filter(lambda d: d > (rows-1)/2, dist_map.values())])
# even_corners = sum([d % 2 == 0 for d in filter(lambda d: d > (rows-1)/2, dist_map.values())])

# # 26501365
# n = int((65 - (rows - 1) / 2) / rows)
# print("N", n, rows)
# print((26501365 - (rows - 1) / 2) / rows)
# total = (n + 1) * (n + 1) * full_odd + (n * n) * full_even - (n - 1) * odd_corners + n * even_corners
# print(total)

# def reachable_p2(g, i, j):
#     out = []
#     for i2, j2 in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
#         i2 = (i2 + rows) % rows
#         j2 = (j2 + cols) % rows
#         if g[i2][j2] == ".":
#             out.append((i2,j2))
#     return out

# reach_set = {}
# for i, row in enumerate(grid):
#     for j, c in enumerate(row):
#         if c == ".":
#             reach_set[(i, j)] = reachable_p2(grid, i, j)

# count_grid = [[0 for _ in range(cols)] for _ in range(rows)]
# count_grid[start[0]][start[1]] = 1

# next_grid = [[0 for _ in range(cols)] for _ in range(rows)]

# for step in range(26501365):
#     # for i in range(rows):
#     #     for j in range(cols):
#     for pos, reach in reach_set.items():
#         next_grid[pos[0]][pos[1]] = len(reach)
#         # sum([count_grid[r[0]][r[1]] for r in reach])
    
#     count_grid, next_grid = next_grid, count_grid
        
#     if step % 100000 == 0:
#         for count_row in count_grid:
#             print(count_row)
#         print(step)
#         print()

# total = 0
# for row in count_grid:
#     print(row)
#     total += sum(row)

# print(total)

# print(reach_set[start])
