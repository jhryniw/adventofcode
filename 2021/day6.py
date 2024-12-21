with open('day6_input.txt', 'r') as f:    
    lamprays = list(map(int, next(f).split(',')))

# lamprays = [3,4,3,1,2]

lampray_counts = [0] * 9
for lifespan in lamprays:
    lampray_counts[lifespan] += 1

for i in range(256):
    new_lampray_counts = [0] * 9
    new_lamprays = lampray_counts[0]
    new_lampray_counts[0] = lampray_counts[1]
    new_lampray_counts[1] = lampray_counts[2]
    new_lampray_counts[2] = lampray_counts[3]
    new_lampray_counts[3] = lampray_counts[4]
    new_lampray_counts[4] = lampray_counts[5]
    new_lampray_counts[5] = lampray_counts[6]
    new_lampray_counts[6] = lampray_counts[7] + new_lamprays
    new_lampray_counts[7] = lampray_counts[8]
    new_lampray_counts[8] = new_lamprays
    lampray_counts = new_lampray_counts

print(lampray_counts)
print(sum(lampray_counts))
