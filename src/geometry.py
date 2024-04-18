

class Point:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def middle(p, q):
		return Point((p.x + q.x) / 2, (p.y + q.y) / 2)


class Vector:

    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def add(self, v):
        self.vx += v.vx
        self.vy += v.vy

    def __str__(self):
        return "(" + str(self.vx) + ", " + str(self.vy) + ")"
