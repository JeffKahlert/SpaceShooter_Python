import math
import random
import time
import pygame
from pygame.locals import *
from pygame import mixer


#Initialiesierung des Spiels
pygame.init()


#Screen erstellen
screen = pygame.display.set_mode((500,700))

#Spieler 
spaceshipImg = pygame.image.load('Spaceshiptest1.bmp')
spaceshipX = 250
spaceshipY = 600
spaceshipX_change = 0
spaceshipY_change = 0 
spaceship_life = 5

screenLife = pygame.font.Font(pygame.font.get_default_font(),20)
def life_text():
	printLife = screenLife.render("Leben: "+str(spaceship_life), True, (255, 255, 255))
	screen.blit(printLife, (20,20))
	

#Gegner 
asteroidsImg = []
asteroidsX = []
asteroidsY = []

asteroidsX_pos = []
asteroidsY_pos = []
asteroids_num = 4 


for i in range(asteroids_num):
	asteroidsImg.append(pygame.image.load('Asteroid.bmp'))
	asteroidsX.append(random.randint(0, 450))
	asteroidsY.append(random.randint(20, 100))
	asteroidsX_pos.append(1)
	asteroidsY_pos.append(-60)
	

#Laser
laserImg =  pygame.image.load('laser.bmp')
laserX = 0 
laserY = 0
laserX_pos = 0
laserY_pos = 0.3
bullet_state = "ready"

#Game Over
over = pygame.font.Font(pygame.font.get_default_font(),36)
 
def game_over_text():
		text = over.render("GAME OVER", True, (255, 255, 255))
		screen.blit(text, (140, 280))
	
	
def spaceship(x, y):
	screen.blit(spaceshipImg, (x,y))
	
def asteroid(x, y, i): 
	screen.blit(asteroidsImg[i], (x,y))
	
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(laserImg, (x + 0.01, y + 0.01))
	
def isCollision(asteroidsX, asteroidsY, laserX, laserY):
	distance = math.sqrt(math.pow(asteroidsX - laserX, 2) + (math.pow(asteroidsY - laserY, 2)))
	if distance < 10:
		return True
	else: 
		return False
		
def spaceshipCollision(asteroidsX, asteroidsY, spaceshipX, spaceshipY):
	distance = math.sqrt(math.pow(asteroidsX - spaceshipX, 2) + (math.pow(asteroidsY - spaceshipY, 2)))
	if distance < 30 :
		return True
	else: 
		return False
		

#GameState Rendering 
running = True
while running:
	#Hintergrund
	screen.fill((3.1,3.9,25.9))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
		#Spielereingaben 		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				spaceshipX_change= -0.3
			if event.key == pygame.K_RIGHT:
				spaceshipX_change = 0.3
			if event.key == pygame.K_UP:
				spaceshipY_change = -0.3
			if event.key == pygame.K_DOWN:
				spaceshipY_change = 0.3
			if event.key == pygame.K_SPACE:
				laserX = spaceshipX
				laserY = spaceshipY
				fire_bullet(laserX, laserY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				spaceshipX_change = 0	
				spaceshipY_change = 0 
	#Spaceship Movement		
	spaceshipY += spaceshipY_change	
	if spaceshipY <= 0:
		spaceshipY = 0
	elif spaceshipY >= 650:
		spaceshipY = 650
			
	spaceshipX += spaceshipX_change
	if spaceshipX <= 0:
		spaceshipX = 0 
	elif spaceshipX >= 450:
		spaceshipX = 450
		
			
	#Asteroids Movement					
	for i in range(asteroids_num):
		asteroidsY[i] += asteroidsY_pos[i]
		
		if asteroidsY[i] <= 0:
			asteroidsY_pos[i] = 0.1
		elif asteroidsY[i] >= 700:
			asteroidsX[i] = random.randint(0, 450)
			asteroidsY[i] = random.randint(20, 100)
			asteroidsX_pos.append(1)
			asteroidsY_pos.append(-60)
			

		#Collision
		collision = isCollision(asteroidsX[i], asteroidsY[i], laserX, laserY)
		spaceCollision = spaceshipCollision(asteroidsX[i], asteroidsY[i], spaceshipX, spaceshipY)
		
		if spaceCollision:
			spaceship_life -= 1
			asteroidsX[i] = random.randint(0, 450)
			asteroidsY[i] = random.randint(20, 100) 
			
		if spaceship_life == 0:
			game_over_text()
			break
				
		if collision:
			laserY = 400
			bullet_state = "ready"
			asteroidsX[i] = random.randint(0, 450)
			asteroidsY[i] = random.randint(20, 100)
			
		asteroid(asteroidsX[i], asteroidsY[i], i)
			
	if laserY <= 0:
		laserY = 480
		bullet_state = "ready"
	
	if bullet_state is "fire":
		fire_bullet(laserX, laserY)
		laserY -= laserY_pos
		
	spaceship(spaceshipX, spaceshipY)
	life_text()
	pygame.display.update()
