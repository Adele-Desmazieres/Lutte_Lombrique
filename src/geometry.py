import math

class Vector:

    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def add(self, v):
        self.vx += v.vx
        self.vy += v.vy

    def __str__(self):
        return "(" + str(self.vx) + ", " + str(self.vy) + ")"
