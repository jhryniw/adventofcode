galaxies = []
exp_rows = []
exp_cols = []
with open("day11full.txt", "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if all([c == "." for c in line]):
            exp_rows.append(i)
            continue

        for j, c in enumerate(line):
            if c == "#":
                galaxies.append((i, j))
    
    cols = len(lines[0])
    for j in range(cols):
        if all([l[j] == "." for l in lines]):
            exp_cols.append(j)

print(galaxies, exp_rows, exp_cols)

def dist(g1, g2) -> int:
    raw_dist = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])

    lower_row = min(g1[0], g2[0])
    upper_row = max(g1[0], g2[0])
    num_extra_rows = sum([(lower_row <= r <= upper_row) for r in exp_rows])

    lower_cols = min(g1[1], g2[1])
    upper_cols = max(g1[1], g2[1])
    num_extra_cols = sum([(lower_cols <= r <= upper_cols) for r in exp_cols])

    return raw_dist + ((num_extra_rows + num_extra_cols) * 999999)

my_sum = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        my_sum += dist(galaxies[i], galaxies[j])
        # print(i + 1, j + 1, galaxies[i], galaxies[j], dist(galaxies[i], galaxies[j]))
print(my_sum)
