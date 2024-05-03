import math
from physical_sphere import * 

# Segment séparant l'air du terrain. 
# Le terrain est sous la ligne définie par le point p à gauche et le point q à droite.
class SurfaceTerrain: 
	
	def __init__(self, p, q):
		self.p = p
		self.q = q
		self.vec = Vector(q[0]-p[0], q[1]-p[1])
		self.angle = self.getAngleRadians()
	
	def getAngleRadians(self):
		return self.vec.getAngleRadians()
	
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

# Ensemble des points formant un polygone de terrain.
# Ou un polygone d'air au sein d'un polygone de terrain.
class Polygon:
	
	def __init__(self, points, is_terrain):
		self.points = points # list of points, ordered to draw a simple polygon
		self.is_terrain = is_terrain # true if the terrain is inside this
		self.length = len(self.points)

class Terrain:
	
	def __init__(self, map, square_size, generation_threshold):
		self.generation_threshold = generation_threshold # the threshold above which terrain will be placed
		self.square_size = square_size # number of pixels in a square side
		
		self.surfaces = self.init_surfaces(map) # a set of TerrainSurface
		
		polygons = self.init_polygons() # a unordered list of Polygon objects
		self.polygons = polygons
	
	# output : l'ensemble des SurfaceTerrain correspondant à la map d'input
	def init_surfaces(self, map):
		terrainSurfaces = set()
		for i in range(len(map)-1):
			for j in range(len(map[i])-1):
				coefs = (map[i][j], map[i][j+1], map[i+1][j+1], map[i+1][j])
				surfaces = self.getLignes(coefs, (i*self.square_size, j*self.square_size))
				terrainSurfaces = terrainSurfaces.union(surfaces)
		return terrainSurfaces
	
	# input : les coefs des 4 coins d'un carré, ses coordonées du coin supérieur gauche
	# output : l'ensemble des lignes passant par ce carré
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
	
	def init_polygons(self):
		polygons = []
		current_list = []
		surfaces = self.surfaces.copy()
		kept_surfaces = set()
		
		while (surfaces):
			s = surfaces.pop()
			curr_kept_surfaces = {s}
			current_list.append(s.p)
			current_list.append(s.q)
			p = s.q
			clockwiseangle = 0
			
			while (len({s for s in surfaces if coords_almost_equals(s.p, p)}) >= 1): # tant que s a un vecteur partant du point précédent
				s2 = {s for s in surfaces if coords_almost_equals(s.p, p)}.pop() # dans surfaces et son p est égal à p
				clockwiseangle += math.pi - angle(s.p, s.q, s2.q)
				s = s2
				surfaces.remove(s)
				curr_kept_surfaces.add(s)
				current_list.append(s.q)
				p = s.q
			
			# keeps only polygons with more than 10 points
			if len(current_list) >= 10:
				kept_surfaces.update(curr_kept_surfaces)
				# print(math.degrees(clockwiseangle))
				polygon = Polygon(current_list, (clockwiseangle >= 0))
				polygons.append(polygon)
				
			current_list = []
		
		self.surfaces = kept_surfaces
		
		return polygons
	


def coords_almost_equals(c, d):
	epsilon = 0.001
	return (abs(c[0]-d[0]) < epsilon and abs(c[1]-d[1]) < epsilon)

def middleCoord(c1, c2):
	return ((c1[0]+c2[0])/2, (c1[1]+c2[1])/2)

def angle(a, b, c):
	ang = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
	return ang + math.pi*2 if ang < 0 else ang
