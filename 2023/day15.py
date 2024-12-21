from dataclasses import dataclass

with open("day15full.txt", "r") as f:
    steps = f.readlines()[0].strip().split(",")

def hash(s: str) -> int:
    current_val = 0
    for c in s:
        current_val += ord(c)
        current_val *= 17
        current_val %= 256
    return current_val

hashes = [hash(s) for s in steps]
print(sum(hashes))

lookup = {}
boxes = [[] for _ in range(256)]

for step in steps:
    if step[-1] == "-":
        label = step[:-1]
        if label in lookup:
            box_index, focal_len = lookup[label]
            boxes[box_index].remove((label, focal_len))
            del lookup[label]
    else:
        label, focal_len = step.split("=")
        focal_len = int(focal_len)
        box_index = hash(label)
        if label in lookup:
            lookup[label] = (box_index, focal_len)
            # Update
            found = False
            for i in range(len(boxes[box_index])):
                lens = boxes[box_index][i]
                if lens[0] == label:
                    boxes[box_index][i] = (label, focal_len)
                    found = True

            if not found:
                print(label, focal_len, box_index, boxes[box_index], lookup)
                assert False
        else:
            lookup[label] = (box_index, focal_len)
            boxes[box_index].append((label, focal_len))
            lookup[label] = (box_index, focal_len)
        
total = 0
for box_num, box in enumerate(boxes):
    for i, lens in enumerate(box):
        label, focal_len = lens
        focus_power = (box_num + 1) * (i + 1) * focal_len
        total += focus_power

print(total)
