from dataclasses import dataclass

digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

seeds = []
seed_ranges = []
conversions = []

@dataclass
class Range:
    dest_start: int
    src_start: int
    range_len: int

    def in_range(self, val: int) -> bool:
        return val >= self.src_start and val < (self.src_start + self.range_len)
    
    def convert(self, val: int) -> int:
        return self.dest_start + val - self.src_start
    
    def partial_range(self, range: tuple) -> tuple:
        r_start = max(range[0], self.src_start)
        r_end = min(range[0] + range[1], self.src_start + self.range_len)
        if r_end > r_start:
            return (r_start, r_end - r_start)
        else:
            return None
    
    def convert_range(self, range: tuple) -> tuple:
        return (range[0] + self.dest_start - self.src_start, range[1])


def subtract_range(r1: tuple, r2: tuple) -> list[tuple]:
    result = []
    over = (max(r2[0] + r2[1], r1[0]), r1[0] + r1[1])
    under = (r1[0], min(r1[0]+r1[1], r2[0]))
    if over[0] < over[1]:
        result.append((over[0], over[1] - over[0]))
    if under[0] < under[1]:
        result.append((under[0], under[1] - under[0]))
    return result

class Conversion:
    src: str
    dest: str
    ranges: list = []

    def __init__(self, src, dest, ranges):
        self.src = src
        self.dest = dest
        self.ranges = ranges

    def convert(self, val: int) -> int:
        for r in self.ranges:
            if r.in_range(val):
                return r.convert(val)
        return val
    
    def convert_range(self, range: tuple) -> list[tuple]:
        result = []
        used_ranges = []
        for r in self.ranges:
            partial = r.partial_range(range)
            # print(partial)
            if partial is not None:
                used_ranges.append(partial)
                result.append(r.convert_range(partial))
        
        # print(used_ranges)
        # print("----")
        # fill range
        unused_ranges = [range]
        for used_range in used_ranges:
            new_unused_ranges = []
            for unused_range in unused_ranges:
                new_ranges = subtract_range(unused_range, used_range)
                # print(unused_range, used_range, new_ranges)
                new_unused_ranges.extend(new_ranges)
            # print(new_unused_ranges)
            unused_ranges = new_unused_ranges
        # print(unused_ranges)
        # Same as the val case
        result.extend(unused_ranges)

        return result
    
with open("day05full2.txt") as f:
    conv = None
    for line in f:
        if len(seeds) == 0:
            seeds = list(map(int, line.split(":")[1].strip().split(" ")))
            seed_ranges = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
            print(seeds, seed_ranges)
            continue

        line = line.strip()
        if len(line) == 0:
            continue

        if line[0] in digits:
            dest_start, src_start, range_len = tuple(map(int, line.split(" ")))
            conv.ranges.append(Range(dest_start=dest_start, src_start=src_start, range_len=range_len))
        else:
            src, _, dst = line.split(" ")[0].split("-")
            if conv is not None:
                conversions.append(conv)
            conv = Conversion(src=src, dest=dst, ranges=[])

    if conv is not None:
        conversions.append(conv)


# Find shortest path

# part1
# locations = []
# for seed in seeds:
#     val = seed
#     for c in conversions:
#         val = c.convert(val)
#     locations.append(val)

# part2
# print(conversions[0].convert_range(seed_ranges[0]))

assert subtract_range((100,4), (98, 2)) == [(100, 4)]
assert subtract_range((100,4), (96, 2)) == [(100, 4)]

loc_ranges = []
for srange in seed_ranges:
    total_range = srange[1]
    ranges = [srange]
    for c in conversions:
        new_ranges = []
        # print(ranges)
        for range in ranges:
            new_ranges.extend(c.convert_range(range))
        ranges = new_ranges
        if sum([r[1] for r in ranges]) != total_range:
            print()
            print(srange, total_range, sum([r[1] for r in ranges]))
            print(ranges)
            assert sum([r[1] for r in ranges]) == total_range
    loc_ranges.extend(ranges)

print(loc_ranges)
print(min([l[0] for l in loc_ranges]))


# print(loc_ranges)
