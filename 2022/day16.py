from collections import deque, defaultdict
from dataclasses import dataclass
from typing import List, Set

@dataclass
class Valve:
    name: str
    index: int
    rate: int
    neighbors: List[str]

def parse() -> List[Valve]:
    data = []
    with open("day16_input.txt", 'r') as f:
        for line in f:
            data.append(line.strip().replace("Valve ", "")
                .replace(" has flow rate=", ", ")
                .replace("; tunnels lead to valves ", ", ")
                .replace("; tunnel leads to valve ", ", ")
                .split(', '))
    
    def to_valve(args):
        i, d = args
        return Valve(name=d[0], rate=int(d[1]), neighbors=d[2:], index=i)

    return list(map(to_valve, enumerate(data)))

def potential(v: Valve, t):
    return v.rate * (30 - t)

def distance_grid(valves):
    num_valves = len(valves)
    grid = defaultdict(dict)

    valve_lookup = dict(zip(map(valve_name, valves), valves))
    
    for v1 in valves:
        seen_set = set()
        q = deque([(v1.name, 0)])
        while len(q) > 0:
            current, d = q.popleft()
            if current in seen_set:
                continue

            seen_set.add(current)
            grid[v1.name][current] = d

            current_valve = valve_lookup[current]
            for n in current_valve.neighbors:
                q.append((n, d + 1))

    return grid


def distance(dgrid, v1, v2):
    return 1

def valve_name(v):
    return v.name

@dataclass
class State:
    current: str
    score: int
    time_left: int
    valves_left: Set[str]


if __name__ == "__main__":
    valves = parse()
    valves = sorted(valves, key=valve_name)
    valve_lookup = dict(zip(map(valve_name, valves), valves))

    d_grid = distance_grid(valves)

    max_seen = 0

    all_valves = list(map(valve_name, filter(lambda v: v.rate > 0, valves)))
    q = deque([State(current='AA', score=0, time_left=30, valves_left=all_valves)])

    while q:
        state = q.popleft()
        cur_valve_index = valve_lookup[state.current].index

        for v in state.valves_left:
            if v == state.current:
                continue
            
            other_valve_index = valve_lookup[v].index
            distance = d_grid[state.current][v]
            new_time_left = state.time_left - distance - 1

            if new_time_left < 0:
                continue

            new_score = state.score + new_time_left * valve_lookup[v].rate

            if new_score > max_seen:
                max_seen = new_score
            
            new_valves_left = state.valves_left.copy()
            new_valves_left.remove(v)
            q.append(State(current=v, score=new_score, time_left=new_time_left, valves_left=new_valves_left))

    print(max_seen)

    # TIMESTEPS = 30

    # dp = []
    # for t in range(TIMESTEPS):
    #     dp.append([])
    #     for i in range(len(valves)):
    #         dp[t].append(DpEntry(val=-1, active=[], debug=[]))
    # dp[0][valves_indexes['AA']].val = 0

    # for t in range(1, TIMESTEPS):
    #     for i, v in enumerate(valves):
    #         max_from_travel = -1
    #         travel_node = None
    #         for other in v.neighbors:
    #             move_val = dp[t-1][valves_indexes[other]].val
    #             if move_val > max_from_travel:
    #                 max_from_travel = move_val
    #                 travel_node = other
            
    #         if not v.name in dp[t-1][i].active and dp[t-1][i].val != -1 and v.rate > 0:
    #             valve_on_val = dp[t-1][i].val + potential(v, t)
    #         else:
    #             valve_on_val = -1

    #         if valve_on_val > max_from_travel:
    #             new_active_list = dp[t-1][i].active.copy()
    #             new_active_list.append(v.name)

    #             debug_copy = dp[t-1][i].debug.copy()
    #             debug_copy.append((v.name, t))
                
    #             dp[t][i].val = valve_on_val
    #             dp[t][i].active = new_active_list
    #             dp[t][i].debug = debug_copy
    #         else:
    #             dp[t][i].val = max_from_travel
    #             dp[t][i].active = dp[t-1][valves_indexes[travel_node]].active.copy() if travel_node is not None else []
    #             dp[t][i].debug = dp[t-1][valves_indexes[travel_node]].debug.copy() if travel_node is not None else []

    # answer = max(list(map(lambda entry: entry.val, dp[-1])))
    # entry = next(filter(lambda entry: entry.val == answer, dp[-1]))

    # print(answer, entry.debug)
    # for node in entry.active:
    #     print(valves[valves_indexes[node]])
