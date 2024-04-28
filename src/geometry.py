import math

class Vector:

    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy
        self.angle = self.getAngleRadians()

    def add(self, v):
        self.vx += v.vx
        self.vy += v.vy
    
    def length(self):
        return math.sqrt(self.vx**2 + self.vy**2)
    
    def getAngleRadians(self):
        return math.atan2(self.vy, self.vx)

    def __str__(self):
        return "(" + str(self.vx) + ", " + str(self.vy) + ")"


def closest_point_on_line(surface, point):
    
    line_vec_x = surface.q[0] - surface.p[0]
    line_vec_y = surface.q[1] - surface.p[1]
    sphere_vec_x = point[0] - surface.p[0]
    sphere_vec_y = point[1] - surface.p[1]
    t = ((sphere_vec_x * line_vec_x) + (sphere_vec_y * line_vec_y)) / ((line_vec_x * line_vec_x) + (line_vec_y * line_vec_y))
    t = max(0, min(1, t))  # Clip to ensure closest point lies on the line segment
    closest_point_x = surface.p[0] + t * line_vec_x
    closest_point_y = surface.p[1] + t * line_vec_y
    return (closest_point_x, closest_point_y)

def distance(p, q):
    return math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)