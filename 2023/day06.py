times = []
distances = []
# with open("day06test.txt") as f:

#     lines = f.readlines()
#     times = [int(e.strip()) for e in lines[0].strip().split(' ')[1:] if len(e)]
#     distances = [int(e.strip()) for e in lines[1].strip().split(' ')[1:] if len(e)]

# prod = 1
# for time, win_thresh in zip(times, distances):
#     poss = 0
#     for hold in range(time):
#         dist = hold * (time - hold)
#         if dist > win_thresh:
#             poss += 1
#     prod *= poss

# print(prod)

with open("day06test.txt") as f:

    lines = f.readlines()
    time = int(lines[0].split(":")[1].replace(" ", "").strip())
    dist = int(lines[1].split(":")[1].replace(" ", "").strip())

poss = 0
for hold in range(time):
    d = hold * (time - hold)
    if d > dist:
        poss += 1

print(poss)
