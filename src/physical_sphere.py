from settings import *
from geometry import *
import math


class PhysicalSphere:
    gravityVector = Vector(0, Settings.GRAVITY)
    bouncingAbsorption = 0.6

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.deplacementVec = Vector(0, 0)
        self.stuckGround = False

    def updatePos(self, terrain):
        if not self.stuckGround:
            self.deplacementVec.add(self.gravityVector)
            self.handleCollision(terrain)
            self.x += self.deplacementVec.vx
            self.y += self.deplacementVec.vy
    
    def borderCollision(self):
        if (self.x + self.radius + self.deplacementVec.vx > Settings.XMAX) or (
                self.x - self.radius + self.deplacementVec.vx < Settings.XMIN):
            self.deplacementVec.vx = -self.deplacementVec.vx * self.bouncingAbsorption
            self.deplacementVec.vy *= self.bouncingAbsorption

        if (self.y + self.radius + self.deplacementVec.vy > Settings.YMAX) or (
                self.y - self.radius + self.deplacementVec.vy < Settings.YMIN):
            self.deplacementVec.vx *= self.bouncingAbsorption
            self.deplacementVec.vy = -self.deplacementVec.vy * self.bouncingAbsorption
    
    def handleCollision(self, terrain):
        for surface in terrain.surfaces:
            if self.intersects(surface):
                self.terrainCollision(surface)
                break
        
        if self.stuckGround:
            self.deplacementVec.vx = 0
            self.deplacementVec.vy = 0

    def distanceToSurface(self, surface):
        """ Calcule la distance du centre de la sphère jusqu'à la surface la plus proche. """
        x1, y1 = surface.p
        x2, y2 = surface.q

        num = abs((y2 - y1) * self.x - (x2 - x1) * self.y + x2 * y1 - y2 * x1)
        den = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return num / den

    def terrainCollision(self, surface):
        angle_surface = math.atan2(surface.vec.vy, surface.vec.vx)
        angle_normal = angle_surface + math.pi / 2

        angle_incidence = math.atan2(-self.deplacementVec.vy, -self.deplacementVec.vx)
        angle_reflected = angle_normal + (angle_normal - angle_incidence)

        speed = math.hypot(self.deplacementVec.vx, self.deplacementVec.vy)
        self.deplacementVec.vx = speed * math.cos(angle_reflected) * self.bouncingAbsorption
        self.deplacementVec.vy = speed * math.sin(angle_reflected) * self.bouncingAbsorption

        # Calcul du déplacement nécessaire pour éloigner la sphère du point de collision
        dist = self.distanceToSurface(surface)
        overlap = self.radius - dist + 0.1
        
        if overlap > 0:  # Ajuster s'il y a chevauchement
            self.x += math.cos(angle_normal) * overlap
            self.y += math.sin(angle_normal) * overlap
        else:
            # Réduire la vitesse pour éviter que les corrections répétées ne causent des tremblements
            self.deplacementVec.vx *= 0.5
            self.deplacementVec.vy *= 0.5
            
        if (speed < 1 and dist < self.radius + 2):
            self.stuckGround = True

    # renvoie True s'il y a collision
    def intersects(self, surface):
        # Distance à la surface (redondant mais on a besoin des éléments du calcul)
        x1, y1 = surface.p
        x2, y2 = surface.q

        num = abs((y2 - y1) * self.x - (x2 - x1) * self.y + x2 * y1 - y2 * x1)
        den = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        distance = num / den

        if distance > self.radius + 0.1:
            return False

        t = ((self.x - x1) * (x2 - x1) + (self.y - y1) * (y2 - y1)) / den ** 2
        nearest_x = x1 + t * (x2 - x1)
        nearest_y = y1 + t * (y2 - y1)

        within_segment = (min(x1, x2) <= nearest_x <= max(x1, x2)) and (min(y1, y2) <= nearest_y <= max(y1, y2))

        return within_segment

    def line_intersect(self, vect, surface):
        vectVx = vect.vx
        vectVy = vect.vy
        surfaceVx = surface.vec.vx
        surfaceVy = surface.vec.vy
        pX, pY = surface.p

        denom = vectVx * surfaceVy - surfaceVx * vectVy
        if denom == 0:
            return False

        denomPos = denom > 0
        totalVx = self.x - pX
        totalVy = self.y - pY
        sNumer = vectVx * totalVy - vectVy * totalVx
        if (sNumer < 0) == denomPos:
            return False

        tNumer = surfaceVx * totalVy - surfaceVy * totalVx
        if (tNumer < 0) == denomPos:
            return False

        if ((sNumer > denom) == denomPos) or ((tNumer > denom) == denomPos):
            return False

        return True
