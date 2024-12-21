from collections import defaultdict

edge_lookup = defaultdict(list)

with open('day12_input.txt', 'r') as f:    
    for l in f:
        edge = tuple(l.strip().split('-'))
        edge_lookup[edge[0]].append(edge[1])
        edge_lookup[edge[1]].append(edge[0])

# prob_s = """
# start-A
# start-b
# A-c
# A-b
# b-d
# A-end
# b-end
# """.strip()

# prob_s = """
# dc-end
# HN-start
# start-kj
# dc-start
# dc-HN
# LN-dc
# HN-end
# kj-sa
# kj-HN
# kj-dc
# """.strip()

# prob_s = """
# fs-end
# he-DX
# fs-he
# start-DX
# pj-DX
# end-zg
# zg-sl
# zg-pj
# pj-he
# RW-he
# fs-DX
# pj-RW
# zg-RW
# start-pj
# he-WI
# zg-he
# pj-fs
# start-RW
# """.strip()

# for l in prob_s.split('\n'):
#     edge = tuple(l.strip().split('-'))
#     edge_lookup[edge[0]].append(edge[1])
#     edge_lookup[edge[1]].append(edge[0])

print(edge_lookup)
paths = set()

def is_small(node):
    return node.islower()

def is_big(node):
    return node.isupper()

def count(node, path):
    return sum(map(lambda n: 1 if n == node else 0, path))

def dfs(current, path):
    if current == 'end':
        paths.add(','.join(path))
        return
    
    adjacent_nodes = edge_lookup[current]

    # Part 1
    # adjacent_nodes = list(filter(lambda node: is_big(node) or node not in path, adjacent_nodes))

    # Part 2
    small_on_path = list(filter(lambda node: is_small(node), path))
    has_visited_twice = len(set(small_on_path)) < len(small_on_path)

    if has_visited_twice:
        adjacent_nodes = list(filter(lambda node: is_big(node) or node not in path, adjacent_nodes))
    else:
        adjacent_nodes = list(filter(lambda node: is_big(node) or (node != 'start'), adjacent_nodes))

    for node in adjacent_nodes:
        dfs(node, path + [node])

dfs('start', ['start'])
print(len(paths))
