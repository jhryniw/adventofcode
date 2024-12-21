from dataclasses import dataclass
import numpy as np

with open("day24test.txt", "r") as f:
    hail = []
    for line in f:
        pos, vel = line.strip().replace(" ", "").split("@")
        pos = tuple([int(e) for e in pos.split(",")])
        vel = tuple([int(e) for e in vel.split(",")])
        hail.append((pos, vel))

# print(hail)

@dataclass
class IntersectionResult:
    t1: float = 0.0
    t2: float = 0.0
    success: bool = False
    intersection_pt: tuple = (0.0, 0.0)


# def intersect_p1(h1, h2) -> IntersectionResult:
#     # print(h1, h2)
#     pos1, vel1 = h1
#     pos2, vel2 = h2

#     v = np.array([
#         [vel1[0], -vel2[0]], # x
#         [vel1[1], -vel2[1]], # y
#     ])

#     p0 = np.array([
#         [pos2[0] - pos1[0]],
#         [pos2[1] - pos1[1]]
#     ])

#     try:
#         t = np.matmul(np.linalg.inv(v), p0)
#     except np.linalg.LinAlgError:
#         return IntersectionResult(success=False)
    
#     t = t.squeeze(-1)
#     return IntersectionResult(
#         success=True,
#         t1=t[0],
#         t2=t[1],
#         intersection_pt=(pos1[0] + (vel1[0] * t[0]), pos1[1] + (vel1[1] * t[0]))
#     )

# total = 0
# for i in range(len(hail)):
#     for j in range(i+1,len(hail)):
#         h1 = hail[i]
#         h2 = hail[j]
#         result = intersect_p1(h1, h2)
#         if result.success and result.t1 >= 0 and result.t2 >= 0 \
#             and 200000000000000 <= result.intersection_pt[0] <= 400000000000000 \
#             and 200000000000000 <= result.intersection_pt[1] <= 400000000000000:
#             total += 1

# print(total)
    
def cross_matrix(v: np.array):
    return np.array([
        [0, -v[2], v[1]],
        [v[2], 0 , -v[0]],
        [-v[1], v[0], 0]
    ])

m = np.block([
    [-cross_matrix(hail[0][1]) + cross_matrix(hail[1][1]), -cross_matrix(hail[0][0])+cross_matrix(hail[1][0])],
    [-cross_matrix(hail[0][1]) + cross_matrix(hail[2][1]), -cross_matrix(hail[0][0])+cross_matrix(hail[2][0])],
])

print(m.shape)

rhs = np.block([
    -np.cross(hail[0][0], hail[0][1]) + np.cross(hail[1][0], hail[1][1]),
    -np.cross(hail[0][0], hail[0][1]) + np.cross(hail[2][0], hail[2][1]),
])

print(rhs.shape)

result = np.matmul(np.linalg.inv(m), rhs)
print(result)
print(sum(result[:3]))
