import math as ma
from physical_objects import * 
# TODO mettre Vector et Point dans un fichier de geometrie


class Point:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def middle(p, q):
		return Point((p.x + q.x) / 2, (p.y + q.y) / 2)
	

class SurfaceTerrain: # le terrain est sous la ligne définie par le point p à gauche et le point q à droite
	
	def __init__(self, p, q):
		self.p = p
		self.q = q
		self.normal = None
		self.vec = Vector(q[0]-p[0], q[1]-p[1])
	
	# def getEquation(p, q):
	# 	if (q.x == p.x):
	# 		return ()
	# 	a = (q.y - p.y) / (q.x - p.x)
	# 	b = p.y - a * p.x
	# 	return (a, b)
	
	def length(self):
		return ma.sqrt((self.q.y - self.p.y)**2 + (self.q.x - self.p.x)**2)
	
	def normalVector(self):
		v = Vector(-self.vec.vy, self.vec.vx)
		return v
	
	def normalVectorSegmentMiddle(self):
		v = self.normalVector()
		m = middleCoord(self.p, self.q)
		n = (m[0] + v.vx, m[1] + v.vy)
		return (m, n)

class Terrain:
	
	generation_threshold = 0.5 # the threshold above which terrain will be placed
	case_size = 50 # number of pixels in a case
	
	def __init__(self, map):
		terrainSurfaces = set()
		for i in range(len(map)-1):
			for j in range(len(map[i])-1):
				coefs = (map[i][j], map[i][j+1], map[i+1][j+1], map[i+1][j])
				surfaces = self.getLignes(coefs, (i*self.case_size, j*self.case_size))
				terrainSurfaces = terrainSurfaces.union(surfaces)
		self.surfaces = terrainSurfaces
		# print(self.surfaces)
				
	
	# input : les coefs des 4 coins d'un carré, ses coordonées du coin supérieur gauche
	# output : la liste des lignes passant par ce carré
	# algorithme de marching squares : https://jamie-wong.com/2014/08/19/metaballs-and-marching-squares/
	def getLignes(self, cornersCoef, topleftCoord):
		topleftCoef, toprightCoef, bottomrightCoef, bottomleftCoef = cornersCoef
		toprightCoord = (topleftCoord[0], topleftCoord[1]+self.case_size)
		bottomrightCoord = (topleftCoord[0]+self.case_size, topleftCoord[1]+self.case_size)
		bottomleftCoord = (topleftCoord[0]+self.case_size, topleftCoord[1])
		
		# check if each corner is inside or outside terrain
		q = 0 # simulate a 4 bytes integer
		if topleftCoef >= self.generation_threshold: q += 8
		if toprightCoef >= self.generation_threshold: q += 4
		if bottomrightCoef >= self.generation_threshold: q += 2
		if bottomleftCoef >= self.generation_threshold: q += 1
		
		topCoord = middleCoord(topleftCoord, toprightCoord)
		rightCoord = middleCoord(bottomrightCoord, toprightCoord)
		bottomCoord = middleCoord(bottomrightCoord, bottomleftCoord)
		leftCoord = middleCoord(topleftCoord, bottomleftCoord)
		
		match q:
			case 1:
				return {SurfaceTerrain(leftCoord, bottomCoord)}
			case 2:
				return {SurfaceTerrain(bottomCoord, rightCoord)}
			case 3:
				return {SurfaceTerrain(leftCoord, rightCoord)}
			case 4:
				return {SurfaceTerrain(rightCoord, topCoord)}
			case 5:
				return {SurfaceTerrain(leftCoord, topCoord), SurfaceTerrain(rightCoord, bottomCoord)}
			case 6:
				return {SurfaceTerrain(bottomCoord, topCoord)}
			case 7:
				return {SurfaceTerrain(leftCoord, topCoord)}
			case 8:
				return {SurfaceTerrain(topCoord, leftCoord)}
			case 9:
				return {SurfaceTerrain(topCoord, bottomCoord)}
			case 10:
				return {SurfaceTerrain(topCoord, rightCoord), SurfaceTerrain(bottomCoord, leftCoord)}
			case 11:
				return {SurfaceTerrain(topCoord, rightCoord)}
			case 12:
				return {SurfaceTerrain(rightCoord, leftCoord)}
			case 13:
				return {SurfaceTerrain(rightCoord, bottomCoord)}
			case 14:
				return {SurfaceTerrain(bottomCoord, leftCoord)}
			case _:
				return {}



def middleCoord(c1, c2):
	return ((c1[0]+c2[0])/2, (c1[1]+c2[1])/2)


