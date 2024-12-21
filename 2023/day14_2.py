from typing import List
from dataclasses import dataclass
from functools import lru_cache

with open("day14full.txt", "r") as f:
    grid = [list(line.strip()) for line in f.readlines()]

cache = dict()

def move_north(grid):
    for j in range(len(grid[0])):
        base_index = 0
        for i in range(len(grid)):
            val = grid[i][j]
            if val == "O":
                grid[i][j] = "."
                grid[base_index][j] = "O"
                base_index += 1
            elif val == "#":
                base_index = i + 1


def move_west(grid):
    for i in range(len(grid)):
        base_index = 0
        for j in range(len(grid[0])):
            val = grid[i][j]
            if val == "O":
                grid[i][j] = "."
                grid[i][base_index] = "O"
                base_index += 1
            elif val == "#":
                base_index = j + 1


def move_south(grid):
    for j in range(len(grid[0])):
        base_index = len(grid) - 1
        for i in reversed(range(len(grid))):
            val = grid[i][j]
            if val == "O":
                grid[i][j] = "."
                grid[base_index][j] = "O"
                base_index -= 1
            elif val == "#":
                base_index = i - 1


def move_east(grid):
    for i in range(len(grid)):
        base_index = len(grid[0]) - 1
        for j in reversed(range(len(grid[0]))):
            val = grid[i][j]
            if val == "O":
                grid[i][j] = "."
                grid[i][base_index] = "O"
                base_index -= 1
            elif val == "#":
                base_index = j - 1

@dataclass
class Grid:
    as_str: str

def compute_str(grid):
    return '\n'.join([''.join(row) for row in grid])

cache = {}
global cache_hit, cache_miss
cache_hit = 0
cache_miss = 0

def extract_grid(s: str):
    return [list(line) for line in s.split("\n")]

@lru_cache(maxsize=256)
def cycle(grid_str: str):
    # global cache_hit, cache_miss
    # if grid_str in cache:
    #     cache_hit += 1
    #     return cache[grid_str]
    
    main_grid = extract_grid(grid_str)
    
    move_north(main_grid)
    move_west(main_grid)
    move_south(main_grid)
    move_east(main_grid)

    new_str = compute_str(main_grid)
    # cache[grid_str] = new_str
    # cache_miss += 1
    return new_str


def total_load(grid):
    total = 0
    total_rows = len(grid)
    for i, row in enumerate(grid):
        for e in row:
            if e == "O":
                total += (total_rows - i)
    return total

def print_grid(grid: Grid):
    print(grid.as_str)
    print()

grid_str = compute_str(grid)

print(grid_str)
for i in range(1000000000):
    grid_str = cycle(grid_str)
    if i % 100000 == 0:
        # print(total_load(extract_grid(grid_str)))
        print(i, cycle.cache_info())

print(grid_str)
# print_grid(full_grid)
print(cache_hit, cache_miss)

print(total_load(extract_grid(grid_str)))
