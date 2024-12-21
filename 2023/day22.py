from __future__ import annotations

from collections import defaultdict

def overlap(i1, i2) -> bool:
    return (i2[0] <= i1[0] <= i2[1]) or (i2[0] <= i1[1] <= i2[1]) or \
           (i1[0] <= i2[0] <= i1[1]) or (i1[0] <= i2[1] <= i1[1])

assert not overlap((0,0),(1, 1))

class Brick:
    id: int
    start: tuple
    end: tuple

    _axis: int
    _non_axis: list

    def __init__(self, id, start, end) -> None:
        self.id = id

        # Find axis
        self._axis = -1
        self._non_axis = []
        for i in range(3):
            if start[i] != end[i]:
                self._axis = i
            else:
                self._non_axis.append(i)
        if not self._axis >= 0:
            self.axis = 2

        if start[self._axis] <= end[self._axis]:
            self.start = start
            self.end = end
        else:
            self.start = end
            self.end = start

    def above_ground(self) -> bool:
        return self.start[2] > 0 and self.end[2] > 0

    def drop_one(self) -> None:
        self._move_z(-1)

    def add_one(self) -> None:
        self._move_z(1)

    def _move_z(self, amt: int) -> None:
        self.start = (self.start[0], self.start[1], self.start[2]+amt)
        self.end = (self.end[0], self.end[1], self.end[2]+amt)

    def _interval(self, axis) -> tuple:
        sa = self.start[axis]
        ea = self.end[axis]
        if sa <= ea:
            return (sa, ea)
        else:
            return (ea, sa)

    def intersects(self, other: Brick) -> bool:
        for axis in range(3):
            if not overlap(self._interval(axis), other._interval(axis)):
                return False
        return True
    
    def _intersects_pt(self, query_pt):
        first = self._non_axis[0]
        second = self._non_axis[1]
        return self.start[first] == query_pt[first] and self.start[second] == query_pt[second] and \
            (self.start[self._axis] <= query_pt[self._axis] <= self.end[self._axis])

    def lowest(self) -> int:
        return min(self.start[2], self.end[2])
    
    def coords(self) -> list:
        out = []
        cur = list(self.start)
        for v in range(self.start[self._axis], self.end[self._axis]+1):
            cur[self._axis] = v
            out.append(tuple(cur))
        return out

    def copy(self) -> Brick:
        return Brick(
            id=self.id,
            start=self.start,
            end=self.end
        )
    
    def __repr__(self):
        return f"[{self.start},{self.end}]"

assert Brick(0, (0, 0, 1), (2, 0, 1)).intersects(Brick(1, (1, 0, 1),(1, 2, 1)))

bricks = []
with open("day22full.txt", "r") as f:
    for id, line in enumerate(f):
        start, end = line.strip().split("~")
        bricks.append(Brick(
            id,
            tuple([int(n) for n in start.split(",")]),
            tuple([int(n) for n in end.split(",")])
        ))

print(bricks)

def plot(bricks, axis1, axis2, rows, cols):
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    grid[0] = ["-"] * cols
    for b in bricks:
        for c1, c2 in set(map(lambda c: (c[axis1], c[axis2]), b.coords())):
            assert c2 > 0
            empty = grid[c2][c1] == " "
            grid[c2][c1] = str(b.id) if empty else "?"
    
    for row in reversed(grid):
        print(''.join(row))
    print()


# bricks = sorted(bricks, key=lambda b: b.lowest())
# plot(bricks, 0, 2, 10, 3)
# print("#####")
# plot(bricks, 1, 2, 10, 3)
# print("^^^ INITIAL")
left = {b.id: "" for b in sorted(bricks, key=lambda b: b.lowest()) if b.above_ground()}

support = defaultdict(set)
pillar = defaultdict(set)

while len(left) > 0:
    to_be_done = []
    for i in left:
        # print("processing", i)
        b = bricks[i]
        assert b.id == i
        b.drop_one()

        found = False
        for comp in bricks:
            if b.id == comp.id:
                continue
            if b.intersects(comp):
                pillar[b.id].add(comp.id)
                support[comp.id].add(b.id)
                found = True
                # print(b, " intersects ", comp)
        
        if found or not b.above_ground():
            b.add_one()
            print("add", b)
            to_be_done.append(b.id)

    for id in to_be_done:
        del left[id]
    
    # print(len(left))
    # print(bricks)
    print(len(left))
    # plot(bricks, 0, 2, 10, 3)
    # plot(bricks, 1, 2, 10, 3)
    # print("#################")

print(support)
print(pillar)

disintegrable = 0
for b in range(len(bricks)):
    needed = False
    for b2 in support[b]:
        if len(pillar[b2]) == 1:
            needed = True
            break
    if not needed:
        disintegrable += 1

print(disintegrable)

print("PILLAR", pillar)
# single_support = {b for b in range(len(bricks)) if len(pillar[b]) == 1}
# print("SINGLE SUPPORT", single_support)
print("SUPPORT", support)

# part 2
total = 0
for b in range(len(bricks)):
    chain = {b}
    q = [b]
    while q:
        cur = q.pop()
        new_links = set()
        for s in support[cur]:
            if len(pillar[s] - chain) == 0:
                new_links.add(s)
        new_links -= chain
        q.extend(new_links)
        chain |= new_links

    print(b, len(chain) - 1)
    total += len(chain) - 1

print(total)

# for every brick b
#  for every brick b2 b supports
# if b2 has >1 support
# b is not disintegrable
