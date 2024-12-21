with open("day14full.txt", "r") as f:
    lines = f.readlines()
    cols = [[] for _ in range(len(lines))]
    for line in lines:
        for j, c in enumerate(line.strip()):
            cols[j].append(c)

print(cols)
num_rows = len(cols[0])

def compute_load(start_index: int, total_rows: int, stack_size: int) -> int:
    result = 0
    top_load = total_rows - start_index
    for load in range(top_load, top_load-stack_size, -1):
        result += load
    return result

totals = []
for col in cols:
    total = 0
    i = 0
    cur_range = 0
    start_index = 0
    while i < len(col):
        if col[i] == "O":
            cur_range += 1
        elif col[i] == "#":
            total += compute_load(start_index, num_rows, cur_range)
            cur_range = 0
            start_index = i + 1
        i += 1
    
    total += compute_load(start_index, num_rows, cur_range)
    totals.append(total)

print(totals)
print(sum(totals))
