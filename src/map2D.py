import random as rd
import math

class Map2D:
	
	def __init__(self, width, height, mincoef, maxcoef):
		self.width = width
		self.height = height
		
		self.mincoef = mincoef
		self.maxcoef = maxcoef
		self.currmincoef = mincoef
		self.currmaxcoef = maxcoef
		self.midcoef = (mincoef+maxcoef) / 2
		
		self.coefs = []
		for i in range(height):
			l = []
			for j in range(width):
				l.append(rd.randrange(mincoef, maxcoef))
			self.coefs.append(l)
		
		self.addLowerTerrainAndCliffs()
		self.normalizeTerrain()
		for i in range(6):
			self.smoothOneTime()
			self.normalizeTerrain()
	
	def smoothOneTime(self):
		c = self.coefs
		
		for j in range(len(c[0])):
			for i in range(len(c)):
				
				# smooth each square according to its neighbours
				c1 = self.coefs[i-1][j-1] if self.checkInRange(i-1, j-1) else None
				c2 = self.coefs[i-1][j] if self.checkInRange(i-1, j) else None
				c3 = self.coefs[i-1][j+1] if self.checkInRange(i-1, j+1) else None
				c4 = self.coefs[i][j-1] if self.checkInRange(i, j-1) else None
				c5 = self.coefs[i][j+1] if self.checkInRange(i, j+1) else None
				c6 = self.coefs[i+1][j-1] if self.checkInRange(i+1, j-1) else None
				c7 = self.coefs[i+1][j] if self.checkInRange(i+1, j) else None
				c8 = self.coefs[i+1][j+1] if self.checkInRange(i+1, j+1) else None
				l = [c1, c2, c3, c4, c5, c6, c7, c8]
				
				nbcoefsup = len([x for x in l if x is not None and x >= self.midcoef])
				c[i][j] += (nbcoefsup - 3.6) * 3 # we can play with theses parameters
				

		self.coefs = c
	
	def addLowerTerrainAndCliffs(self):
		c = self.coefs
		
		for j in range(len(c[0])):
			for i in range(len(c)):
								
				# add a few mountains and cliffs
				c[i][j] += math.sin(j / 3) * 0.7
				
				# add more terrain on ground and remove some terrain from the sky
				nbr_zones = 5
				zonesize = self.height / nbr_zones
				groundseparation = 5
				c[i][j] += ((i//zonesize) * groundseparation / (self.height//zonesize)) - (groundseparation/2)
				
				# add noise
				# self.coefs[i][j] += rd.randrange(-1, 1)
				
		self.coefs = c
		
	def normalizeTerrain(self):
		# normalize terrain between mincoef and maxcoef
		a = (self.mincoef-self.maxcoef) / (self.currmincoef-self.currmaxcoef)
		b = self.maxcoef - a * self.currmaxcoef
		
		c = self.coefs
		
		for j in range(len(c[0])):
			for i in range(len(c)):
				c[i][j] = a * c[i][j] + b
		
		self.coefs = c
	
	def checkInRange(self, i, j):
		return 0 <= i < len(self.coefs) and 0 <= j < len(self.coefs[i])
	
	def getCoefsFormatted(self):
		coefs = self.coefs
		# inverse la map
		coefs = [[coefs[i][j] for i in range(len(coefs))] for j in range(len(coefs[0]))]
		# ajoute des 0 autour de la map
		coefs = [[0] + coefs[i] + [0] for i in range(len(coefs))]
		coefs = [[0] * len(coefs[0])] + coefs + [[0] * len(coefs[0])]

		return coefs
	
	def __str__(self):
		return self.coefs.__str__()

