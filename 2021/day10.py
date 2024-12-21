lines = []

with open('day10_input.txt', 'r') as f:
    lines = [line.strip() for line in f]

# lines = """
# [({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]
# """.strip().split('\n')

def back(stack):
    return stack[-1] if len(stack) > 0 else ''

score_map = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

class Result:
    def __init__(self, line):
        stack = []
        self.violation = None
        for c in line:
            if c == '(' or c == '{' or c == '[' or c == '<':
                stack.append(c)
            else:
                if c == ')':
                    if back(stack) == '(':
                        stack.pop()
                    else:
                        self.violation = c
                        break
                elif c == '}':
                    if back(stack) == '{':
                        stack.pop()
                    else:
                        self.violation = c
                        break
                elif c == ']':
                    if back(stack) == '[':
                        stack.pop()
                    else:
                        self.violation = c
                        break
                else:
                    if back(stack) == '<':
                        stack.pop()
                    else:
                        self.violation = c
                        break

        self.stack = stack
        self.is_incomplete = len(stack) > 0 and self.violation is None
        self.is_corrupted = self.violation is not None
        self.corrupt_score = score_map[self.violation] if self.violation is not None else 0

results = [Result(line) for line in lines]

# Part 1
print(sum([result.corrupt_score for result in results]))

# Part 2
incomplete_results = list(filter(lambda r: r.is_incomplete, results))

inc_score_map = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

def incomplete_score(result):
    score = 0
    for c in reversed(result.stack):
        score *= 5
        score += inc_score_map[c]
    return score

def median(positions):
    sorted_positions = sorted(positions)
    mid = len(sorted_positions) // 2
    if len(sorted_positions) % 2 == 0:
        return round((sorted_positions[mid - 1] + sorted_positions[mid]) / 2)
    else:
        return sorted_positions[mid]

scores = [incomplete_score(result) for result in incomplete_results]
print(median(scores))
