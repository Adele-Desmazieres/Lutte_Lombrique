import math
from physical_sphere import * 


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
		return math.sqrt((self.q.y - self.p.y)**2 + (self.q.x - self.p.x)**2)
	
	def normalVector(self):
		v = Vector(-self.vec.vy, self.vec.vx)
		return v
	
	def normalVectorSegmentMiddle(self):
		v = self.normalVector()
		m = middleCoord(self.p, self.q)
		n = (m[0] + v.vx, m[1] + v.vy)
		return (m, n)

class Terrain:
	
	def __init__(self, map, square_size, generation_threshold):
		self.generation_threshold = generation_threshold # the threshold above which terrain will be placed
		self.square_size = square_size # number of pixels in a square side
		terrainSurfaces = set()
		
		# ajoute des 0 autour de la map
		mapframed = [[0] + map[i] + [0] for i in range(len(map))]
		mapframed = [[0] * len(mapframed[0])] + mapframed + [[0] * len(mapframed[0])]
		map = mapframed

		for i in range(len(map)-1):
			for j in range(len(map[i])-1):
				coefs = (map[i][j], map[i][j+1], map[i+1][j+1], map[i+1][j])
				surfaces = self.getLignes(coefs, (i*self.square_size, j*self.square_size))
				terrainSurfaces = terrainSurfaces.union(surfaces)
		self.surfaces = terrainSurfaces
		
		polygons = self.init_points_lists() # a list of lists of (int, int)
		self.polygons = polygons
		# print(self.surfaces)		
	
	# input : les coefs des 4 coins d'un carré, ses coordonées du coin supérieur gauche
	# output : la liste des lignes passant par ce carré
	# algorithme de marching squares : https://jamie-wong.com/2014/08/19/metaballs-and-marching-squares/
	def getLignes(self, cornersCoef, topleftCoord):
		y = topleftCoord[0]
		x = topleftCoord[1]
		size = self.square_size
		thr = self.generation_threshold
		tl, tr, br, bl = cornersCoef
		
		# check if each corner is inside or outside terrain
		q = 0 # simulate a 4 bytes integer, each bit is flipped if the corner is inside terrain
		if tl >= thr: q += 8
		if tr >= thr: q += 4
		if br >= thr: q += 2
		if bl >= thr: q += 1
		
		# simplest method : gives only straight and 45 degres slopes
		#toprightCoord = (x, y+size)
		#bottomrightCoord = (x+size, y+size)
		#bottomleftCoord = (x+size, y)
		#topCoord = middleCoord(topleftCoord, toprightCoord)
		#rightCoord = middleCoord(bottomrightCoord, toprightCoord)
		#bottomCoord = middleCoord(bottomrightCoord, bottomleftCoord)
		#leftCoord = middleCoord(topleftCoord, bottomleftCoord)
		
		# linear interpolation to smooth the slopes
		if q != 0 and q != 15:
			topCoord = (y, x + size - size * ((thr-tr)/(tl-tr))) if (tl-tr) else (0, 0)
			rightCoord = (y + size * ((thr-tr)/(br-tr)), x + size) if (br-tr) else (0, 0)
			bottomCoord = (y + size, x + size - size * ((thr-br)/(bl-br))) if (bl-br) else (0, 0)
			leftCoord = (y + size - size * ((thr-bl)/(tl-bl)), x) if (tl-bl) else (0, 0)
		
		# create the slopes of this square
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
			case _: # cases 0 and 15 : no terrain limitation (air square or full terrain square)
				return {}
	
	def init_points_lists(self):
		points_lists = []
		current_list = []
		surfaces = self.surfaces.copy()
		
		while (surfaces):
			s = surfaces.pop()
			current_list.append(s.p)
			current_list.append(s.q)
			p = s.q
			
			while (len({s for s in surfaces if coords_almost_equals(s.p, p)}) >= 1): # tant que s a un vecteur partant du point précédent
				s = {s for s in surfaces if coords_almost_equals(s.p, p)}.pop() # dans surfaces et son p est égal à p
				surfaces.remove(s)
				current_list.append(s.q)
				p = s.q
			
			points_lists.append(current_list)
			current_list = []
		
		return points_lists
	


def coords_almost_equals(c, d):
	epsilon = 0.001
	return (abs(c[0]-d[0]) < epsilon and abs(c[1]-d[1]) < epsilon)
	# return c == d

def middleCoord(c1, c2):
	return ((c1[0]+c2[0])/2, (c1[1]+c2[1])/2)


