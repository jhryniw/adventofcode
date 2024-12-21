with open("day09full.txt", "r") as f:
    lines = f.readlines()
    seqs = [[int(n) for n in line.strip().split(" ")] for line in lines]

print(seqs)

def compute_diffs(l):
    d = []
    for a, b in zip(l, l[1:]):
        d.append(b-a)
    return d

preds = []
pred_firsts = []
for seq in seqs:
    diffs = seq
    last = [seq[-1]]
    first = [seq[0]]
    while any([d != 0 for d in diffs]):
        diffs = compute_diffs(diffs)
        last.append(diffs[-1])
        first.append(diffs[0])
    preds.append(sum(last))

    # print(first)
    pred_first = 0
    for f in reversed(first):
        pred_first = f - pred_first
    pred_firsts.append(pred_first)
    # print(pred_first)

# print(preds)
# print(sum(preds))

print(pred_firsts)
print(sum(pred_firsts))
