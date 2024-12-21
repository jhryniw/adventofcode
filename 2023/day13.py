patterns = []
with open("day13full.txt", "r") as f:
    lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        pat = []
        while i < len(lines):
            line = lines[i].strip()
            if line == "":
                break
            pat.append(line)
            i += 1
            
        patterns.append(pat)
        i += 1

col_patterns = []
for pat in patterns:
    cols = len(pat[0])
    col_pat = []
    for j in range(cols):
        col_line = ''
        for line in pat:
            col_line += line[j]
        col_pat.append(col_line)
    col_patterns.append(col_pat)

from typing import List

def is_mirror(pat: List[str], index: int) -> bool:
    left = index
    right = index + 1
    if right >= len(pat):
        return False
    
    while left >= 0 and right < len(pat):
        if pat[left] != pat[right]:
            return False
        left -= 1
        right += 1
    return True


def can_smudge(s1: str, s2: str) -> int:
    diff = 0
    first = -1
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            diff += 1
            if first == -1:
                first = i
    return first if diff <= 1 else -1

def replace_at_index(s, i, c):
    return s[:i] + c + s[i+1:]

def is_mirror_p2(pat: List[str], index: int) -> bool:
    left = index
    right = index + 1
    if right >= len(pat):
        return False
    
    smudge_allowance = 1
    fixed = None
    
    while left >= 0 and right < len(pat):
        if pat[left] != pat[right]:
            if smudge_allowance == 0:
                return False
            
            smudge_index = can_smudge(pat[left], pat[right])
            if smudge_index > -1:
                smudge_allowance -= 1
                fixed = (left, smudge_index)
            else:
                return False
        left -= 1
        right += 1

    return fixed is not None
    #     print("FIXED", fixed)
    #     rep = "." if pat[fixed[0]][fixed[1]] == "#" else "#"
    #     pat[fixed[0]] = replace_at_index(pat[fixed[0]], fixed[1], rep)

    # return True, fixed


def part1():
    print("part1")
    total = []
    for row_pat, col_pat in zip(patterns, col_patterns):

        for i in range(len(row_pat)):
            if is_mirror(row_pat, i):
                print("MIRROR ROW", i)
                total.append((i + 1) * 100)

        for j in range(len(col_pat)):
            if is_mirror(col_pat, j):
                print("MIRROR COL", j)
                total.append(j + 1)

    assert len(total) == len(patterns)
    print(sum(total))
    print()

def part2():
    print("part2")
    total = []
    for row_pat, col_pat in zip(patterns, col_patterns):
        
        found = False
        for i in range(len(row_pat)):
            if is_mirror_p2(row_pat, i):
                print("MIRROR ROW", i)
                total.append((i + 1) * 100)
                found = True
                break
            
        if found:
            continue


        for j in range(len(col_pat)):
            if is_mirror_p2(col_pat, j):
                print("MIRROR COL", j)
                total.append(j + 1)
                break

    assert len(total) == len(patterns)
    print(sum(total))
    print()

    # assert reflection_found

part1()
part2()

# total = 0
# for row_pat, col_pat in zip(patterns, col_patterns):

#     print()
#     print("\n".join(row_pat))

#     reflected_original = set()
#     reflected_smudge = set()
#     can_fix = True

#     for i in range(len(row_pat)):
#         m, fixed = is_mirror_p2(row_pat, i, can_fix)
#         if m:
#             print("MIRROR ROW", i)
#             if fixed is not None:
#                 can_fix = False
#                 col_pat[fixed[1]] = replace_at_index()
            
#             total += (i + 1) * 100

#         # if is_mirror(row_pat, i):
#         #     print("MIRROR ROW ORIG", i)
#         #     reflected_original.add(("r", i))

#         if is_mirror_p2(row_pat, i):
#             print("MIRROR ROW", i)
#             # total += (i + 1) * 100
#             reflected_smudge.add(("r", i))
#             # break
    
#     # if reflection_found:
#         # continue
#     print()
#     print("\n".join(col_pat))

#     for j in range(len(col_pat)):
#         if is_mirror(col_pat, j):
#             print("MIRROR COL ORIG", j)
#             reflected_original.add(("c", i))

#         if is_mirror_p2(col_pat, j):
#             print("MIRROR COL", j)
#             reflected_smudge.add(("c", j))
#     print()

#     new_line = list(reflected_smudge - reflected_original)
#     print(reflected_smudge, reflected_original)
#     assert len(new_line) == 1
#     if new_line[0] == "r":
#         total += ((new_line[1] + 1) * 100)
#     else:
#         total += (new_line[0] + 1)

    # assert reflection_found

# print(total)

# for pat in patterns:
#     print("\n".join(pat))
#     print()

# for pat in col_patterns:
#     print("\n".join(pat))
#     print()
