hmap = []
bmap = []

with open('day9_input.txt', 'r') as f:
    for line in f:
        row = [int(h) for h in line.strip()]
        hmap.append(row)
        bmap.append([h == 9 for h in row])

# test_map = """
# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# """

# for line in test_map.strip().split('\n'):
#     row = [int(h) for h in line.strip()]
#     hmap.append(row)
#     bmap.append([h == 9 for h in row])

def is_lowpoint(heights, i, j, rows, cols):
    val = heights[i][j]
    # up
    if i > 0 and heights[i-1][j] <= val:
        return False
    #down
    if i < rows - 1 and heights[i+1][j] <= val:
        return False

    # left    
    if j > 0 and heights[i][j-1] <= val:
        return False

    # right
    if j < cols - 1 and heights[i][j+1] <= val:
        return False

    return True

def mark_basins(basins, si, sj, rows, cols):

    def mark(i, j):
        if i < 0 or j < 0 or i >= rows or j >= cols or basins[i][j]:
            return 0
        basins[i][j] = True

        return 1 + mark(i+1, j) + mark(i-1, j) + mark(i, j+1) + mark(i, j-1)

    return mark(si, sj)

total = 0
map_rows = len(hmap)
map_cols = len(hmap[0])
basin_sizes = []

for i in range(map_rows):
    for j in range(map_cols):
        if is_lowpoint(hmap, i, j, map_rows, map_cols):
            basin_size = mark_basins(bmap, i, j, map_rows, map_cols)
            basin_sizes.append(basin_size)
            total += 1 + hmap[i][j]

# Part 1
print(total)

# Part 2
biggest_3 = sorted(basin_sizes, reverse=True)[:3]
print(biggest_3[0] * biggest_3[1] * biggest_3[2])
