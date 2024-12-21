grid = []
with open('day11_input.txt', 'r') as f:
    for line in f:
        grid.append(list(map(int, line.strip())))

# grid_s = """
# 5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526
# """.strip().split('\n')

# grid_s = """
# 11111
# 19991
# 19191
# 19991
# 11111
# """.strip().split('\n')

# for line in grid_s:
#         grid.append(list(map(int, line.strip())))

rows = len(grid)
cols = len(grid[0])

def flash(fmap, i, j):
    if i < 0 or i >= rows or j < 0 or j >= cols:
        return

    if fmap[i][j]:
        return

    # flash
    grid[i][j] += 1
    if grid[i][j] > 9:
        fmap[i][j] = True
        flash(fmap, i-1, j)
        flash(fmap, i+1, j)
        flash(fmap, i, j-1)
        flash(fmap, i, j+1)
        flash(fmap, i-1, j-1)
        flash(fmap, i+1, j+1)
        flash(fmap, i+1, j-1)
        flash(fmap, i-1, j+1)


# num_flashes = 0
# for _ in range(100):
step = 0
while True:
    step += 1
    fmap = [[False] * cols for _ in range(rows)]

    # Add one to every element
    for i in range(rows):
        for j in range(cols):
            grid[i][j] += 1

    # Traverse flashes
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] > 9:
                fmap[i][j] == True
                flash(fmap, i, j)

    # Flash down
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] > 9:
                grid[i][j] = 0
    
    num_flashes = 0
    for i in range(rows):
        for j in range(cols):
            if fmap[i][j]:
                num_flashes += 1
    
    if num_flashes == rows * cols:
        break

for i in range(rows):
    print(''.join(map(str, grid[i])))

print('')
# print(num_flashes)
print(step)
