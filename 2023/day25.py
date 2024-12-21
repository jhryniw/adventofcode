from collections import defaultdict, deque
from typing import List, Tuple

connections = defaultdict(set)

with open("day25full.txt", "r") as f:
    for line in f:
        n, cons = line.strip().split(":")
        cons = [c for c in cons.strip().split(" ")]
        for c in cons:
            connections[n].add(c)
            connections[c].add(n)

nodes = list(connections.keys())

edges = {}
for u in nodes:
    for v in connections[u]:
        edges[(u, v)] = 0

def bfs(flows: dict, source: str, target: str, parent: dict) -> Tuple[bool, list]:
    parent.clear()

    q = deque([source])
    while len(q) > 0 and target not in parent:
        cur = q.popleft()
        for n in connections[cur]:
            assert (cur, n) in flows
            if n not in parent and flows[(cur, n)] > 0:
                q.append(n)
                parent[n] = cur

    return target in parent


def max_flows(nodes, edges, source, target) -> int:
    # num_nodes = len(nodes)
    flows = {e: 1 for e in edges.keys()}
    # capacities = {e: 1 for e in edges}
    source = nodes[0]
    target = nodes[-1]
    parent = {}

    while bfs(flows, source, target, parent):
        path_flow = float("Inf")
        s = target
        while s != source:
            path_flow = min(path_flow, flows[(parent[s], s)])
            s = parent[s]

        v = target
        while v != source:
            u = parent[v]
            flows[(u, v)] -= path_flow
            flows[(v, u)] += path_flow
            v = parent[v]

    return flows

flows = max_flows(nodes, edges, nodes[0], nodes[-1])
# print(flows)

def extract_flow_group(flows: dict, conns: dict, start: str):
    group = set()
    q = [start]
    while q:
        cur = q.pop()
        group.add(cur)
        for c in conns[cur]:
            if c not in group and flows[(cur, c)] > 0:
                q.append(c)
    return group

print(nodes[0], nodes[-1])

group1 = extract_flow_group(flows, connections, nodes[0])
print(group1)
print(len(group1))
print(len(nodes) - len(group1))
print("ANSWER: ", len(group1) * (len(nodes) - len(group1)))


# for _ in range(3):
#     links = ranked_links(nodes, connections)
#     _, _, to_cut = links[0]
#     n1, n2 = to_cut
#     print(links[0])
#     connections[n2].remove(n1)
#     connections[n1].remove(n2)

# def get_group_1(nodes, conns) -> set:
#     group1 = set()
#     q = [nodes[0]]
#     while q:
#         cur = q.pop()
#         group1.add(cur)
#         for c in conns[cur]:
#             if c not in group1:
#                 q.append(c)
#     return group1

# group1 = get_group_1(nodes, connections)

# print(len(group1), group1)
# print(len(nodes) - len(group1), set(nodes) - group1)



# print()

# for n, s in connections.items():
#     print(n, len(s))
