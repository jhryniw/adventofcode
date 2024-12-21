from dataclasses import dataclass
import re

@dataclass
class Node:
    name: str
    left: str
    right: str

    def __hash__(self) -> int:
        return hash(self.name)

nodes = {}

with open("day08full.txt") as f:
    lines = [l.strip() for l in f.readlines()]
    dirs = list(lines[0])

    for l in lines[2:]:
        words = [re.sub(r'\W+', '', w) for w in l.split(" ")]
        words = [w for w in words if len(w)]
        assert len(words) == 3, words
        name, left, right = tuple(words)
        node = Node(name=name, left=left, right=right)
        nodes[node.name] = node

# n = nodes['AAA']
# i = 0
# step = 0
# while n.name != "ZZZ":
#     d = dirs[i]
#     if d == "L":
#         n = nodes[n.left]
#     else:
#         n = nodes[n.right]

#     i = (i + 1) % len(dirs)
#     step += 1

# print(step)

class Pointer:
    sunk: bool
    cur: str
    path: list
    visited: set
    loop: list
    good: list

    def __init__(self, cur) -> None:
        self.cur = cur
        self.sunk = False
        self.path = []
        self.visited = set((cur, 0))
        self.sunk_node = None
        self.loop = None

    def compute_loop(self):
        loop = []
        self.path.pop()
        i = len(self.path) - 1
        while self.path[i][0] != self.cur:
            loop.append(self.path[i][0])
            i -= 1
        loop.append(self.cur)

        self.loop = list(reversed(loop))
        self.good = [i for i, n in enumerate(self.loop) if n[-1] == 'Z']

    def __repr__(self) -> str:
        return repr([len(self.path), len(self.loop), self.good])
        # return repr((self.cur, self.sunk, self.path, self.loop, self.good))


pointers = [Pointer(n.name) for n in nodes.values() if n.name[-1] == "A"]
step = 0

for p in pointers:
    i = 0
    while p.cur[-1] != 'Z':
        d = dirs[i]
        if d == "L":
            p.cur = nodes[p.cur].left
        else:
            p.cur = nodes[p.cur].right
        p.path.append(p.cur)
        i = (i + 1) % len(dirs)

print([p.path for p in pointers])
steps = [len(p.path) for p in pointers]

from functools import reduce
from math import lcm
# print(pointers)
print(steps)
print(lcm(*steps))

# while any([not p.sunk for p in pointers]):
#     d = dirs[i]
#     i = (i + 1) % len(dirs)
#     for p in pointers:
#         if not p.sunk:
#             if d == "L":
#                 p.cur = nodes[p.cur].left
#             else:
#                 p.cur = nodes[p.cur].right
            
#             key = (p.cur, i)
#             p.path.append(key)
#             if key in p.visited:
#                 p.sunk = True
#                 p.sunk_node = p.cur
#             else:
#                 p.visited.add(key)

#     step += 1

# @dataclass
# class PathIter:
#     first: int = 0
#     cur: int = 0
#     loop_len: int = 0

# iters = []

# for p in pointers:
#     p.compute_loop()
#     assert len(p.good) == 1
#     path_len = len(p.path)
#     loop_len = len(p.loop)
#     good = p.good[0]
#     iters.append(PathIter(
#         first = path_len - loop_len + good,
#         cur = path_len - loop_len + good,
#         loop_len=loop_len
#     ))

# import copy


# s = sorted(iters, key=lambda it: it.cur)

# def combine_naive(it1o: PathIter, it2o: PathIter) -> PathIter:
#     it1 = copy.copy(it1o)
#     it2 = copy.copy(it2o)
#     i = 0
#     while it1.cur != it2.cur:
#         small = min(it1, it2, key=lambda i: i.cur)
#         large = max(it1, it2, key=lambda i: i.cur)
#         small.cur += math.ceil((large.cur - small.cur) / small.loop_len) * small.loop_len
#         # i += 1
#         # if i > 100000:
#         #     print(small, large)
#         #     i = 0
    
#     return PathIter(
#         first=it1.cur,
#         cur=it1.cur,
#         loop_len=lcm(it1.loop_len, it2.loop_len)
#     )

# print(combine_naive(s[0], s[1]))
# assert (combine_naive(
#     PathIter(cur=2, loop_len=2),
#     PathIter(cur=7, loop_len=3)
# ).cur == 10)

# at = s[0]
# cur = 0
# for it in s[1:]:
#     new_at = combine_naive(at, it)
#     print(f"{at} + {it} = {new_at}")
#     at = new_at

# print(at)
# print(s)
# at = s[0]
# cur = 0
# for it in s[1:]:
#     meet = max(it.cur, at.cur)
    
#     it_cur = meet - ((meet - it.cur) % it.loop_len)
#     at_curr = meet - ((meet - at.cur) % at.loop_len)

#     # diff = max(it.cur, at.cur) % min(it.loop_len, at.loop_len)

#     # diff = abs(it_cur - at_curr)
#     # # loop_diff = 
#     # jump = lcm(diff, at.loop_len)
#     # jump = lcm(jump, it.loop_len)

#     # loop_diff = max(it.loop_len, at.loop_len) % min(it.loop_len, at.loop_len)
#     # jump = lcm(diff, loop_diff)
#     new_loop_len = lcm(at.loop_len, it.loop_len)
#     # print(at.loop_len, it.loop_len, new_loop_len)
#     # print(at, it, diff, loop_diff, jump)
#     at = PathIter(
#         cur=at.cur + jump,
#         loop_len=new_loop_len
#     )
#     print(at)

# print("---")
print(at)

for it in s:
    print(it, (at.cur - it.first) % it.loop_len)
    assert (at.cur - it.cur) % it.loop_len == 0

# jump = iters[0].loop_len
# for it in iters[1:]:

#     print(jump)
#     jump = lcm(jump, it.loop_len)
# print(jump)


# while any([it.cur != iters[0].cur for it in iters]):
#     low = min([it.cur for it in iters])
#     for it in iters:
#         if it.cur == low:
#             it.cur += it.loop_len
#     # print(iters)

# print(iters)


