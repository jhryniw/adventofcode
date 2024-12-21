from typing import List, Tuple
from functools import lru_cache

class Arrangement:
    s: str = ""
    groups: list

    def __init__(self, s: str):
        self.s = s
        self.groups = []
        prev = "."
        for i in range(len(s)):
            if s[i] == "#":
                if prev == ".":
                    self.groups.append(1)
                else:
                    self.groups[-1] += 1
            prev = s[i]

    def add_damaged(self):
        return Arrangement(self.s + "#")
    
    def add_operational(self):
        return Arrangement(self.s + ".")
    
    def compatible(self, groups: list):
        if len(self.groups) > len(groups):
            return False
        
        if len(self.groups) == 0:
            return True
        
        for i in range(len(self.groups) - 1):
            if self.groups[i] != groups[i]:
                return False
        
        if self.groups[-1] > groups[len(self.groups) - 1]:
            return False
        
        return True
    
    def equal(self, groups: list):
        return self.groups == groups
    
    def __repr__(self) -> str:
        return self.s


def arrangements(s: str, groups: List[int]) -> int:
    arrangements = [Arrangement("")]

    for c in s:
        new_arr = []
        for arr in arrangements:
            if not arr.compatible(groups):
                continue

            if c == "#" or c == "?":
                new_arr.append(arr.add_damaged())
            if c == "." or c == "?":
                new_arr.append(arr.add_operational())

        # print(new_arr)
        arrangements = new_arr
    return arrangements

ANY = 0
DAMAGE_ONLY = 1
OP_ONLY = 2

@lru_cache
def arrangements_p2(s: str, groups: Tuple[int], open: int) -> int:
    if len(s) == 0 and len(groups) == 0:
        # print(s, groups, 1, open)
        return 1
    elif len(groups) == 0:
        # print(s, groups, open, 1 if all([c in "?." for c in s]) else 0)
        return 1 if all([c in "?." for c in s]) else 0
    if len(s) < sum(groups):
        # print(s, groups, open, 0)
        return 0
    
    c = s[0]
    result = 0
    
    if (c == "#" or c == "?") and open != OP_ONLY:
        if groups[0]-1 <= 0:
            new_groups = groups[1:]
            result += arrangements_p2(s[1:], new_groups, open=OP_ONLY)
        else:
            new_groups = tuple([groups[0]-1] + list(groups[1:]))
            result += arrangements_p2(s[1:], new_groups, open=DAMAGE_ONLY)
    
    if (c == "." or c == "?") and open != DAMAGE_ONLY:
        result += arrangements_p2(s[1:], groups, open=ANY)

    # print(s, groups, open, result)
    return result

def count(arrs: list, groups: list):
    # print(arrs)
    return sum([arr.equal(groups) for arr in arrs])


with open("day12full.txt", "r") as f:
    lines = f.readlines()
    # lines = lines[2:3]
    total = 0
    for line in lines:
        s, g = line.strip().split(" ")
        groups = tuple(map(int, g.split(",")))
        groups = groups * 5
        s = '?'.join([s] * 5)
        # print(s, groups)
        line_total = arrangements_p2(s, groups, open=ANY)
        total += line_total
        print(line_total, " ---- ", s, groups)
    print(total)

# print(arrangements_p2("#?#?", (3,), open=True))

# print(count(arrangements("???.###", [1, 1, 3]), [1, 1, 3]))
# print(count(arrangements(".??..??...?##.", [1, 1, 3]), [1, 1, 3]))

# assert arrangements("???.###", [1, 1, 3]) == 1
# assert arrangements(".??..??...?##.", [1, 1, 3]) == 4
