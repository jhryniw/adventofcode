from dataclasses import dataclass, field

@dataclass
class Rule:
    var: str
    op: str
    thresh: int
    ans: str

    def execute(self, vars: dict) -> str:
        v = vars[self.var]
        if self.op == ">":
            if v > self.thresh:
                return self.ans
        elif self.op == "<":
            if v < self.thresh:
                return self.ans
        return None
    
    def execute_range(self, range: dict) -> list:
        v_range = range[self.var]
        if self.op == ">":
            if self.thresh >= v_range[1]:
                return None, range
            elif self.thresh < v_range[0]:
                return range, None
            else:
                range_copy_new = range.copy()
                range_copy_new[self.var] = (self.thresh+1, v_range[1])
                range_copy_remain = range.copy()
                range_copy_remain[self.var] = (v_range[0], self.thresh)
                return range_copy_new, range_copy_remain
        else: # self.op == "<":
            if self.thresh > v_range[1]:
                return range, None
            elif self.thresh <= v_range[0]:
                return None, range
            else:
                range_copy_remain = range.copy()
                range_copy_remain[self.var] = (self.thresh, v_range[1])
                range_copy_new= range.copy()
                range_copy_new[self.var] = (v_range[0], self.thresh-1)
                return range_copy_new, range_copy_remain

test_rule_less = Rule(var='a', op='<', thresh=2006, ans='qkq')
assert test_rule_less.execute_range({'a': (0, 4000)}) == ({'a': (0, 2005)}, {'a': (2006, 4000)})
assert test_rule_less.execute_range({'a': (0, 2006)}) == ({'a': (0, 2005)}, {'a': (2006, 2006)})
assert test_rule_less.execute_range({'a': (0, 2005)}) == ({'a': (0, 2005)}, None)
assert test_rule_less.execute_range({'a': (2005, 4000)}) == ({'a': (2005, 2005)}, {'a': (2006, 4000)})
assert test_rule_less.execute_range({'a': (2006, 4000)}) == (None, {'a': (2006, 4000)})

test_rule_greater = Rule(var='a', op='>', thresh=2005, ans='qkq')
assert test_rule_greater.execute_range({'a': (0, 4000)}) == ({'a': (2006, 4000)}, {'a': (0, 2005)})
assert test_rule_greater.execute_range({'a': (0, 2006)}) == ({'a': (2006, 2006)}, {'a': (0, 2005)})
assert test_rule_greater.execute_range({'a': (0, 2005)}) == (None, {'a': (0, 2005)})
assert test_rule_greater.execute_range({'a': (2005, 4000)}) == ({'a': (2006, 4000)}, {'a': (2005, 2005)})
assert test_rule_greater.execute_range({'a': (2006, 4000)}) == ({'a': (2006, 4000)}, None)

@dataclass 
class Workflow:
    rules: list
    end_ans: str

    def execute(self, vars: dict) -> str:
        for rule in self.rules:
            a = rule.execute(vars)
            if a is not None:
                return a
        return self.end_ans
    
    def execute_range(self, range: dict) -> list:
        out = []
        remain = range
        for rule in self.rules:
            if remain is None:
                break
            new, remain = rule.execute_range(remain)
            if new is not None:
                out.append((rule.ans, new))

        if remain is not None:
            out.append((self.end_ans, remain))
        
        return out


with open("day19full.txt", "r") as f:
    workflows = {}
    f_iter = iter(f)
    for line in f_iter:
        line = line.strip()
        if line == "":
            break
        
        workflow_name, rules_str = line.split("{")
        rules_str = rules_str.strip("}").split(",")
        rules = []
        end_ans = None
        for rule_str in rules_str:
            if ":" not in rule_str:
                end_ans = rule_str
                continue

            r, ans = rule_str.split(":")
            if ">" in r:
                v, thresh = r.split(">")
                op = ">"
            else:
                v, thresh = r.split("<")
                op = "<"
            rules.append(Rule(var=v, op=op, thresh=int(thresh), ans=ans))
        
        assert end_ans is not None
        workflows[workflow_name] = Workflow(
            rules=rules,
            end_ans=end_ans,
        )

    all_vars = []
    for line in f_iter:
        line = line.strip().strip("}{")
        parts = line.split(",")
        vars = {}
        for part in parts:
            k, v = part.split("=")
            vars[k] = int(v)
        all_vars.append(vars)

# total = 0

# for vars in all_vars:
#     w = 'in'
#     while w in workflows:
#         w = workflows[w].execute(vars)

#     if w == "A":
#         total += vars['x'] + vars['m'] + vars['a'] + vars['s']

# print(total)


start = {   
    'x': (1, 4000),
    'm': (1, 4000),
    'a': (1, 4000),
    's': (1, 4000),
}
q = [('in', start)]

print(workflows['px'])
result = workflows['px'].execute_range(start)
for row in result:
    print(row)

print()

resolved = []
while len(q) > 0:
    w, range = q.pop()
    processed = workflows[w].execute_range(range)
    for p in processed:
        if p[0] == 'A' or p[0] == 'R':
            resolved.append(p)
        else:
            q.append(p)

total = 0

for r in resolved:
    print(r)
print(r)

def range_len(v_range):
    return v_range[1] - v_range[0] + 1

for result, range in resolved:
    if result == "A":
        poss = range_len(range['x']) * range_len(range['m']) * range_len(range['a']) * range_len(range['s'])
        total += poss

print(total)
