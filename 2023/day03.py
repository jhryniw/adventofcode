from dataclasses import dataclass, field

@dataclass
class Number:
    pos: list = field(default_factory=list)
    val_str: str = ""
    adj: bool = False


symbol_positions = set()
gears = {}
numbers = []
digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
# symbols = {'*', '#', '+', '$', '/', ''}

with open("day03.txt") as f:
    for line_num, line in enumerate(f):
        number = None
        for c_num, c in enumerate(line):
            was_digit = False
            if c in digits:
                was_digit = True
                if number is None:
                    number = Number()
                number.pos.append((line_num, c_num))
                number.val_str += c
            elif c != '.' and c != '\n':
                symbol_positions.add((line_num, c_num))
            
            if c == "*":
                gears[(line_num, c_num)] = []
            
            if not was_digit and number is not None:
                numbers.append(number)
                number = None
        
        if number is not None:
            numbers.append(number)

def adjacency(x: int, y: int) -> list:
    return [
        (x+1, y), (x+1, y+1), (x+1, y-1),
        (x, y+1), (x, y-1),
        (x-1, y), (x-1, y+1), (x-1, y-1),
    ]

for number in numbers:
    for pos in number.pos:
        adj = adjacency(pos[0], pos[1])
        should_break = False
        for p in adj:
            if p in gears:
                gears[p].append(number)

            if p in symbol_positions:
                number.adj = True
                should_break = True
                break
        if should_break:
            break

sum = 0
for g, nums in gears.items():
    if len(nums) == 2:
        sum += int(nums[0].val_str) * int(nums[1].val_str)
        nums[0].adj = False
        nums[1].adj = False

# for n in numbers:
#     if n.adj:
#         sum += int(n.val_str)

# print(gears)
# print([n for n in numbers if n.adj])
# print(sorted(symbol_positions))
print(sum)
