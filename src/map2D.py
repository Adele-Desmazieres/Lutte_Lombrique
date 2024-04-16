import random as rd
import math

class Map2D:
	
	def __init__(self, width, height, mincoef, maxcoef):
		self.width = width
		self.height = height
		self.mincoef = mincoef
		self.maxcoef = maxcoef
		self.midcoef = (mincoef+maxcoef) / 2
		self.coefs = []
		for i in range(height):
			l = []
			for j in range(width):
				l.append(rd.randrange(mincoef, maxcoef))
			self.coefs.append(l)
			
		for i in range(10):
			self.smoothOneTime()
	
	def smoothOneTime(self):
		c = self.coefs
		for j in range(len(c[0])):
			for i in range(len(c)):
				c1 = self.coefs[i-1][j-1] if self.checkInRange(i-1, j-1) else None
				c2 = self.coefs[i-1][j] if self.checkInRange(i-1, j) else None
				c3 = self.coefs[i-1][j+1] if self.checkInRange(i-1, j+1) else None
				c4 = self.coefs[i][j-1] if self.checkInRange(i, j-1) else None
				c5 = self.coefs[i][j+1] if self.checkInRange(i, j+1) else None
				c6 = self.coefs[i+1][j-1] if self.checkInRange(i+1, j-1) else None
				c7 = self.coefs[i+1][j] if self.checkInRange(i+1, j) else None
				c8 = self.coefs[i+1][j+1] if self.checkInRange(i+1, j+1) else None
				l = [c1, c2, c3, c4, c5, c6, c7, c8]
				nbcoefsup = len([x for x in l if x is not None and x > self.midcoef])
				c[i][j] += (nbcoefsup - 3.6) * 5 # we can play with theses parameters
				
				# truncate between max and min coef
				c[i][j] = max(min(c[i][j], self.maxcoef), self.mincoef)

				c[i][j] += math.sin(j / 3)
				# c[i][j] += math.cos(i * j + 1)
				
				# truncate between max and min coef
				c[i][j] = max(min(c[i][j], self.maxcoef), self.mincoef)

				# more terrain on ground than sky
				nbr_zones = 5
				zonesize = self.height / nbr_zones
				groundseparation = 5
				c[i][j] += ((i//zonesize) * groundseparation / (self.height//zonesize)) - (groundseparation/2)

				# truncate between max and min coef
				c[i][j] = max(min(c[i][j], self.maxcoef), self.mincoef)
				
		self.coefs = c
		# TODO : test this
	
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

