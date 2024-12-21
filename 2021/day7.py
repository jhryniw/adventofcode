with open('day7_input.txt', 'r') as f:    
    crabs = list(map(int, next(f).split(',')))

# crabs = [16,1,2,0,4,2,7,1,2,14]

def p1_cost(positions, target):
    return sum(map(lambda p: abs(p - target), positions))

def p2_cost(positions, target):
    return sum(map(lambda p: (abs(p-target) * (abs(p-target)+1)) / 2, positions))

def median(positions):
    sorted_positions = sorted(positions)
    mid = len(sorted_positions) // 2
    if len(sorted_positions) % 2 == 0:
        return round((sorted_positions[mid - 1] + sorted_positions[mid]) / 2)
    else:
        return sorted_positions[mid]

def gradient_method(positions):
    low = 0
    high = max(positions)
    while True:
        mid = (low + high) // 2
        cost_below = p2_cost(positions, mid-1)
        cost_mid = p2_cost(positions, mid)
        cost_above = p2_cost(positions, mid+1)
        if cost_mid < cost_below and cost_mid < cost_above:
            return mid
        elif cost_below < cost_mid:
            high = mid-1
        elif cost_above < cost_mid:
            low = mid+1

# Part 1
# p_median = median(crabs)
# print(p_median)
# print(p1_cost(crabs, p_median))
# print(p1_cost(crabs, p_median + 1))
# print(p1_cost(crabs, p_median - 1))


# Part 2
p_grad = gradient_method(crabs)
print(p_grad)
print(p2_cost(crabs, p_grad))
