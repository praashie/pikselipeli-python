import pygame
import pygame.gfxdraw
from pygame.locals import *;
 
import __main__
import random
import math

objList = [];

newObjList = [];
delObjList = [];

playerKeyList = [];

started = False;

class GameObject:
	x = 0.0;
	y = 0.0;

	xVel = 0.0;
	yVel = 0.0;
	
	def __init__(self, x, y):
		newObjList.append(self);
		self.x, self.y	= x, y;
		self.xVel 	= 0;
		self.yVel	= 0;
	def delete(self):
		if not self in delObjList:
			delObjList.append(self);
	def draw(self):
		pass;
	def update(self):
		pass;
class Bullet(GameObject):
	parent = None;

	bouncy = False;
	xOld = 0.0;
	yOld = 0.0;

	def __init__(self, x, y, angle, vel, parent):
		newObjList.append(self);
		self.parent = parent;

		self.x = x + math.cos(angle) * (parent.radius + 5.);
		self.y = y - math.sin(angle) * (parent.radius + 5.);

		self.xOld = self.x;
		self.yOld = self.y;

		self.xVel = math.cos(angle) * vel;
		self.yVel = -math.sin(angle) * vel;

	def update(self):
		global objList;

		self.xOld = self.x;
		self.yOld = self.y;

		self.x += self.xVel;
		self.y += self.yVel;

		if self.bouncy == True:
			if (self.x < 50):
				self.x = 50;
				self.xVel *= -1;
			if (self.x > (__main__.screenW - 50)):
				self.x = __main__.screenW - 50;
				self.xVel *= -1;
			if (self.y < 50):
				self.y = 50;
				self.yVel *= -1;
			if (self.y > (__main__.screenH - 50)):
				self.y = __main__.screenH - 50;
				self.yVel *= -1;



		if (self.x < 0) or (self.x > __main__.screenW) or (self.y < 0) or (self.y > __main__.screenH):
			self.delete();

		for o in objList:
			if o.__class__ == Player:
				if o.isAlive == True and ( (self.x - o.x) * (self.x - o.x) +  (self.y - o.y) * (self.y - o.y)) < (o.radius*o.radius):
					o.xVel += self.xVel * 0.3;
					o.yVel += self.yVel * 0.3;

					o.hurt(10.);
					self.parent.hurt(-3./(self.parent.health/100.));
					self.delete();
	def draw(self):
		#pygame.draw.line(__main__.windowSurface, (0,0,0), (self.xOld, self.yOld), (self.x, self.y));
		pygame.gfxdraw.line(__main__.windowSurface, int(self.xOld), int(self.yOld), int(self.x), int(self.y), (0,0,0));
class Player(GameObject):
	controllerKey = 0;
	friction = 0.9;
	#friction = 1.0;
	turnDirection = 1;

	angle = 0.0;
	angleVel = 0.0;

	angleFriction = 0.8;
	#angleFriction = 1.0;

	shootTimer = 0;
	respawnTimer = 0;

	health = 100.;
	radius = 10.;

	isAlive = False;
	def update(self):
		if self.isAlive == True:
			self.x = self.x + self.xVel;
			self.y = self.y + self.yVel;

			self.xVel *= self.friction;
			self.yVel *= self.friction;

			self.angle += self.angleVel;
			self.angleVel *= self.angleFriction;

			if (self.x < 50):
				self.x = 50;
				self.xVel *= -1;
			if (self.x > (__main__.screenW - 50)):
				self.x = __main__.screenW - 50;
				self.xVel *= -1;
			if (self.y < 50):
				self.y = 50;
				self.yVel *= -1;
			if (self.y > (__main__.screenH - 50)):
				self.y = __main__.screenH - 50;
				self.yVel *= -1;

			if __main__.isKeyPressed(self.controllerKey):
				self.shootTimer = 0;
			if __main__.isKeyDown(self.controllerKey):
				self.xVel += math.cos(self.angle) * 0.6;
				self.yVel -= math.sin(self.angle) * 0.6;
				
				self.angleVel += 0.02 * self.turnDirection;

				self.shootTimer += 1;

			if __main__.isKeyReleased(self.controllerKey):
				self.turnDirection *= -1;

				if self.shootTimer < 10:
					Bullet(self.x, self.y, self.angle, 10., self);

			self.radius = 15. + (self.health*self.health/600.);
		else:
			if self.respawnTimer < 1:
				self.spawn();
			else:
				self.respawnTimer -= 1;
	def hurt(self, x):
		self.health -= x;
		if self.health <= 0.0:
			self.die();
	def die(self):
		self.isAlive = False;
		self.respawnTimer += 300;
	def spawn(self):
		self.x = random.randint(100, __main__.screenW - 100);
		self.y = random.randint(100, __main__.screenH - 100);

		self.health = 100;

		self.isAlive = True;
	def draw(self):
		if self.isAlive == True:
			#pygame.draw.circle(__main__.windowSurface, (0, 0, 0), (int(self.x), int(self.y)), self.radius, 1);
			pygame.gfxdraw.aacircle(__main__.windowSurface, int(self.x), int(self.y), int(self.radius), (0,0,0));
			lineStart = (int(self.x + math.cos(self.angle) * self.radius), int(self.y - math.sin(self.angle) * self.radius));
			lineEnd = (int(self.x + math.cos(self.angle) * (self.radius + 5.)), int(self.y - math.sin(self.angle) * (self.radius + 5.)));
			pygame.draw.line(__main__.windowSurface, (0, 0, 0), lineStart, lineEnd);

def startGame():
	#Player(32, 32);
	started = True;

	return True;

def updateGame():
	
	for k in range(K_a, K_z + 1):
		if __main__.isKeyPressed(k) and not k in playerKeyList:
			p = Player(0, 0);
			p.controllerKey = k;
			playerKeyList.append(k);
			p.spawn();

	global objList, newObjList, delObjList;
	for o in objList:
		o.update();
	for n in newObjList:
		objList.append(n);
	for d in delObjList:
		objList.remove(d);
		del d;

	newObjList = [];
	delObjList = [];

	return True;

def drawGame():
	__main__.windowSurface.fill( (255, 255, 255) );

	for o in objList:
		o.draw();

	return True;
