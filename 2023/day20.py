from dataclasses import dataclass
from collections import deque, defaultdict
from typing import List, Dict

@dataclass
class Pulse:
    src: str
    dest: str
    ptype: str

    def __repr__(self):
        return f"{self.src} -{self.ptype}-> {self.dest}"

class Module:
    name: str
    children: List[str]

    def __init__(self, name: str, children: List[str]) -> None:
        self.name = name
        self.children = children

    def handle(self, p: Pulse) -> List[Pulse]:
        raise NotImplementedError("Not implemented")
    
    def pulses(self, ptype: str) -> List[Pulse]:
        return [Pulse(src=self.name, dest=c, ptype=ptype) for c in self.children]


class Broadcaster(Module):

    def handle(self, p: Pulse) -> List[Pulse]:
        assert p.dest == self.name
        return self.pulses(p.ptype)

        
class FlipFlop(Module):
    OFF = False
    ON = True

    state: int = OFF
    
    def handle(self, p: Pulse) -> List[Pulse]:
        assert p.dest == self.name
        if p.ptype == "high":
            return []
        elif self.state:
            self.state = False
            return self.pulses("low")
        else:
            self.state = True
            return self.pulses("high")


class Conjunction(Module):
    state: Dict[str, bool] = {}

    def handle(self, p: Pulse) -> List[Pulse]:
        assert p.dest == self.name
        self.state[p.src] = p.ptype == "high"

        if all(self.state.values()):
            out = self.pulses("low")
        else:
            out = self.pulses("high")

        return out

    def setup(self, inputs: List[str]):
        self.state = dict([(i, False) for i in inputs])
        self.num_high = 0

    def peek_state(self) -> str:
        if all(self.state.values()):
            return "low"
        else:
            return "high"

class Rx(Module):
    done: bool = False
    
    def handle(self, p: Pulse) -> List[Pulse]:
        self.done = p.ptype == "low"
        return []


with open("day20full.txt", "r") as f:
    modules: Dict[str, Module] = {}
    conjs = []
    for line in f:
        name, children_str = line.strip().split(" -> ")
        children = children_str.split(", ")
        if name == "broadcaster":
            modules[name] = Broadcaster("broadcaster", children)
        elif name.startswith("%"):
            modules[name[1:]] = FlipFlop(name[1:], children)
        elif name.startswith("&"):
            modules[name[1:]] = Conjunction(name[1:], children)
            conjs.append(name[1:])

modules['rx'] = Rx("rx", [])

input_map = defaultdict(list)

for m in modules.values():
    for c in m.children:
        input_map[c].append(m.name)

for c in conjs:
    modules[c].setup(input_map[c])

print(input_map['mf'])
rx_ins = {i:0 for i in input_map['mf']}

total_low_pulses = 0
total_high_pulses = 0
button_presses = 0

def prod(nums):
    out = 1
    for n in nums:
        out *= n
    return out

while True:
    button_presses += 1
    q = deque()
    q.append(Pulse(src="button", dest="broadcaster", ptype="low"))
    low_pulses = 0
    high_pulses = 0
    while q:
        pulse = q.popleft()
        # print(pulse)
        if pulse.ptype == "low":
            low_pulses += 1
        else:
            high_pulses += 1

        if pulse.dest in modules:
            out_pulses = modules[pulse.dest].handle(pulse)
            q.extend(out_pulses)

        if pulse.dest in rx_ins and modules[pulse.dest].peek_state() == "high":
            if rx_ins[pulse.dest] == 0:
                rx_ins[pulse.dest] = button_presses
                print(rx_ins)

            # for p in out_pulses:
            #     if p.dest == "rx":
            #         print(p)
    
    if all(rx_ins.values()):
        print(rx_ins)
        print(prod(rx_ins.values()))
        break

    if button_presses < 1000:
    # print(low_pulses, high_pulses)
        total_low_pulses += low_pulses
        total_high_pulses += high_pulses
    # print("----")

# print([(n, input_map[n]) for n in conjs])
print(total_low_pulses, total_high_pulses)
print(total_low_pulses * total_high_pulses)
