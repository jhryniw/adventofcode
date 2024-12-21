with open('/Users/james.hryniw/adventofcode2021/day2_input.txt', 'r') as cmd_file:
    cmds = cmd_file.readlines()

# Part 1
x = 0
depth = 0

for cmd in cmds:
    move, amt = cmd.split()
    amt = int(amt)
    if move == 'forward':
        x += amt
    elif move == 'down':
        depth += amt
    elif move == 'up':
        depth -= amt
    else:
        print("unrecognized move: {}".format(move))

print(x * depth)

# Part 2

x = 0
depth = 0
aim = 0

for cmd in cmds:
    move, amt = cmd.split()
    amt = int(amt)
    if move == 'forward':
        x += amt
        depth += aim * amt
    elif move == 'down':
        aim += amt
    elif move == 'up':
        aim -= amt
    else:
        print("unrecognized move: {}".format(move))

print(x * depth)
