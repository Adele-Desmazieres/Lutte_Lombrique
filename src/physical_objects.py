from game_parameters import *
from enum import Enum

class State(Enum):
	GROUNDED = 0
	AIRBORNE = 1

class Vector:
	
	def __init__(self, vx, vy):
		self.vx = vx
		self.vy = vy
	
	def add(self, v):
		self.vx += v.vx
		self.vy += v.vy
	
	def __str__(self):
		return "(" + str(self.vx) + ", " + str(self.vy) + ")"


class PhysicalSphere:
	
	gravityVector = Vector(0, GameParameters.GRAVITY)
	
	def __init__(self, x, y, radius):
		self.x = x
		self.y = y
		self.radius = radius
		self.deplacementVec = Vector(0, 0)
	
	def moveFree(self):
		self.deplacementVec.add(self.gravityVector)
		self.handleCollision()
		print(self.deplacementVec)
		self.x += self.deplacementVec.vx
		self.y += self.deplacementVec.vy
	
	def handleCollision(self):
		stuckGround = False
		if (self.x + self.radius + self.deplacementVec.vx > GameParameters.XMAX) or (self.x - self.radius + self.deplacementVec.vx < GameParameters.XMIN):
			self.deplacementVec.vx = -self.deplacementVec.vx * GameParameters.BOUNCINGABSORPTION
			self.deplacementVec.vy *= GameParameters.BOUNCINGABSORPTION
			
		if (self.y + self.radius + self.deplacementVec.vy > GameParameters.YMAX) or (self.y - self.radius + self.deplacementVec.vy < GameParameters.YMIN):
			if (self.y + self.radius + self.deplacementVec.vy > GameParameters.YMAX) and (self.deplacementVec.vy < 2):
				stuckGround = True
			self.deplacementVec.vx *= GameParameters.BOUNCINGABSORPTION
			self.deplacementVec.vy = -self.deplacementVec.vy * GameParameters.BOUNCINGABSORPTION
		
		# colle l'objet au sol
		if stuckGround :
			self.deplacementVec.vx = 0
			self.deplacementVec.vy = 0


class Worm(PhysicalSphere):
	slideSpeed = 3
	radius = 10
	
	def __init__(self, x, y):
		PhysicalSphere.__init__(self, x, y, 10)
		self.state = State.GROUNDED
	
	def moveRight(self):
		if self.state == State.GROUNDED:
			self.x += self.slideSpeed
			# TODO : pas de terrain en dessous => state => airborne + vecteur de descente
	
	def moveLeft(self):
		if self.state == State.GROUNDED:
			self.x -= self.slideSpeed
			# TODO : pas de terrain en dessous => state => airborne + vecteur de descente
	
	def moveDown(self):
		if self.state == State.GROUNDED:
			self.y += self.slideSpeed
			# TODO : pas de terrain en dessous => state => airborne + vecteur de descente
	
	def moveUp(self):
		if self.state == State.GROUNDED:
			self.y -= self.slideSpeed
			# TODO : pas de terrain en dessous => state => airborne + vecteur de descente
