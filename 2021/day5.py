class Pt:
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]

    def __hash__(self):
        return hash(tuple(self.x, self.y))

    def __str__(self):
        return ','.join([str(self.x), str(self.y)])

class Line:
    def __init__(self, pt1, pt2):
        self.start = pt1
        self.end = pt2
        if (self.is_vertical() and self.start.y > self.end.y) or \
           self.start.x > self.end.x:
            self.start, self.end = self.end, self.start

    def is_horizontal(self):
        return self.start.y == self.end.y
    
    def is_vertical(self):
        return self.start.x == self.end.x

    def is_main_diagonal(self):
        return self.start.x < self.end.x and self.start.y < self.end.y
    
    def is_off_diagonal(self):
        return self.start.x < self.end.x and self.start.y > self.end.y

    def __len__(self):
        if self.is_horizontal():
            return self.end.x - self.start.x
        elif self.is_vertical():
            return self.end.y - self.start.y
        else:
            return self.end.x - self.start.x

    def all_coords(self):
        coords = []
        if self.is_horizontal():
            for i in range(self.start.x, self.end.x + 1):
                coords.append((i, self.start.y))
        elif self.is_vertical():
            for i in range(self.start.y, self.end.y + 1):
                coords.append((self.start.x, i))
        elif self.is_main_diagonal():
            for i in range(len(self) + 1):
                coords.append((self.start.x + i, self.start.y + i))
        elif self.is_off_diagonal():
            for i in range(len(self) + 1):
                coords.append((self.start.x + i, self.start.y - i))

        return coords

    def __str__(self):
        return "{} -> {}".format(str(self.start), str(self.end))


def coord_to_pt(coord):
    return Pt(tuple(map(int, coord.split(','))))

lines = []

with open('day5_input.txt', 'r') as f:    
    for l in f:
        pts = l.split(' -> ')
        line = Line(coord_to_pt(pts[0]), coord_to_pt(pts[1]))
        lines.append(line)

grid = [0] * 1000000

for line in lines:
    for coord in line.all_coords():
        grid[coord[0] * 1000 + coord[1]] += 1

count = 0
for i in range(1000000):
    if grid[i] >= 2:
        count += 1

print(count)
