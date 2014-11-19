import sys, pygame;
from pygame.locals import *;

import game;

screenW = 800;
screenH = 600;

pygame.init();

clock = pygame.time.Clock();

eventList = [];
keyboardState = [];
keyboardOldState = [];

gameRunning = True;

def updateEvents():
	global eventList, gameRunning;
	pygame.event.pump();
	eventList = pygame.event.get();

	for event in eventList:
		if event.type == QUIT:
			gameRunning = False;

	updateKeyboard();

def updateKeyboard():
	global keyboardState, keyboardOldState;

	keyboardOldState = keyboardState;
	keyboardState = pygame.key.get_pressed();

def isKeyDown(key):
	return keyboardState[key];
def isKeyPressed(key):
	return keyboardState[key] and (not keyboardOldState[key]);
def isKeyReleased(key):
	return (not keyboardState[key]) and keyboardOldState[key];


windowSurface = pygame.display.set_mode( (screenW, screenH) );
font = pygame.font.Font('freesansbold.ttf', 20);

game.startGame();

gameRunning = True;
while gameRunning == True:

	updateEvents();

	game.updateGame();
	game.drawGame();
	pygame.display.update();

	clock.tick(60);	

pygame.quit();
sys.exit();
