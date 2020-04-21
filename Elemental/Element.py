import pygame as pg #For graphics
import random #For random player movements
import numpy as np
import math as m

from Particles import ParticleManager, Particle

class Element(pg.sprite.Sprite):
    def __init__(self, initVelX, initVelY, xLoc, yLoc, speed, image, name, color):
        #Creates image and private fields
        pg.sprite.Sprite.__init__(self)
        self.image = image.convert()
        self.size = self.image.get_size()
        self.name = name
        
        self.super = None #Which player can beat it
        self.sub = None #Which player it can beat
        self.maxSpeed = speed
        self.x = xLoc - self.size[0]/2
        self.y = yLoc - self.size[0]/2
        self.change_x = initVelX
        self.change_y = initVelY
        self.AIchoiceInterval = random.randint(15, 30) #How fast the AI brain can make decisions
        self.color = color
        if self.name == "LAVA":
            self.number = 1
        elif self.name == "POISON":
            self.number = 2
        elif self.name == "ACID":
            self.number = 3
        elif self.name == "WATER":
            self.number = 4
        else:
            print("Wrong Element Error")
            quit()
        self.particleList = ParticleManager((self.x, self.y), (self.change_x/2, self.change_y/2), 20, self.color, self.name, 0.9, 1) #Creates new particle effect for each player
        self.deathNums = [] #List of player numbers that will kill it if run into
    
    def update(self, width, height, SQUARE_WIDTH):
        self.addMovement() #Update position
        self.boundryCheck(width, height) #Make sure player remains on screen
            
        #Align to column if just turned
        if(self.change_y != 0 and self.x % SQUARE_WIDTH != 0): #Going Up or Down and not aligned on X
            self.x = np.round(self.x/SQUARE_WIDTH) * SQUARE_WIDTH
        if(self.change_x != 0 and self.y % SQUARE_WIDTH != 0): #Going Left or Right and not aligned on Y
            self.y = np.round(self.y/SQUARE_WIDTH) * SQUARE_WIDTH   
        self.particleList.update(self.color, self.name, (self.x, self.y), (self.change_x/2, self.change_y/2), 1) #Update particles  
    def setSuper(self, otherGuy):
        self.super = otherGuy
        self.deathNums.append(otherGuy.number)
    def setSub(self, otherPlayer):
        self.sub = otherPlayer

    #Directional Methods
    def goUp(self):
        self.change_x = 0
        self.change_y = -self.maxSpeed
    def goDown(self):
        self.change_x = 0
        self.change_y = self.maxSpeed
    def goRight(self):
        self.change_x = self.maxSpeed
        self.change_y = 0
    def goLeft(self):
        self.change_x = -self.maxSpeed
        self.change_y = 0        
    def turnLeft(self):
        if self.getDir() == "Right": #If going right
            self.goUp()
        elif self.getDir() == "Up": #If going Up
            self.goLeft()
        elif self.getDir() == "Left": #If going left
            self.goDown()
        else: #If going down
            self.goRight()
    def turnRight(self):
        if self.getDir() == "Right": #Right
            self.goDown()
        elif self.getDir() == "Up": #Up
            self.goRight()
        elif self.getDir() == "Left": #Left
            self.goUp()
        else: #Down
            self.goLeft()
    def getDir(self):
        if(self.change_x == self.maxSpeed):
            return "Right"
        elif(self.change_y == -self.maxSpeed):
            return "Up"
        elif(self.change_x == -self.maxSpeed):
            return "Left"
        else:
            return "Down"
    def addMovement(self):
        self.x += self.change_x 
        self.y += self.change_y
    
    #Indexing methoda
    def findMyBox(self, SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT): #Returns given index in Matrix from player position
        x = m.trunc((self.x%SCREEN_WIDTH) / SQUARE_SIZE)
        y = m.trunc((self.y%SCREEN_HEIGHT) / SQUARE_SIZE)
        if(x >= 0 and y >= 0 and x < SCREEN_WIDTH/SQUARE_SIZE and y < SCREEN_HEIGHT/SQUARE_SIZE): 
            return (x, y)
        else:
            print("Player Bad Index Box Error")
            return None
    def findRightBox(self, SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT): #Returns Matrix index of right
        x = m.trunc((self.x%SCREEN_WIDTH) / SQUARE_SIZE) + 1
        y = m.trunc((self.y%SCREEN_HEIGHT) / SQUARE_SIZE)
        if(y >= 0 and y < SCREEN_HEIGHT/SQUARE_SIZE):
            if(x == SCREEN_WIDTH/SQUARE_SIZE):
                x = int(0)
            return (x, y)
        else:
            return None
    def findLeftBox(self, SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT): #Returns Matrix index of left
        x = m.trunc((self.x%SCREEN_WIDTH) / SQUARE_SIZE) - 1
        y = m.trunc((self.y%SCREEN_HEIGHT) / SQUARE_SIZE)
        if(y >= 0 and y < SCREEN_HEIGHT/SQUARE_SIZE):
            if(x == -1):
                x = int(SCREEN_WIDTH/SQUARE_SIZE-1)
            return (x, y)
        else:
            return None
    def findUpBox(self, SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT): #Returns Matrix index of above
        x = m.trunc((self.x%SCREEN_WIDTH) / SQUARE_SIZE)
        y = m.trunc((self.y%SCREEN_HEIGHT) / SQUARE_SIZE) - 1
        if(x >= 0 and x < SCREEN_WIDTH/SQUARE_SIZE):
            if(y == -1):
                y = int(SCREEN_HEIGHT/SQUARE_SIZE-1)
            return (x, y)
        else:
            return None
    def findDownBox(self, SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT): #Returns Matrix index of below
        x = m.trunc((self.x%SCREEN_WIDTH) / SQUARE_SIZE)
        y = m.trunc((self.y%SCREEN_HEIGHT) / SQUARE_SIZE) + 1
        if(x >= 0 and x < SCREEN_WIDTH/SQUARE_SIZE):
            if(y == SCREEN_HEIGHT/SQUARE_SIZE):
                y = int(0)
            return (x, y)
        else:
            return None
    def willDie(self, GRID, SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE):
        num = GRID[self.findMyBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)] #Find who controls current index
        return num in self.deathNums #If that number is in the death list
    def boundryCheck(self, width, height): #Puts the player in bounds if they were not
        if(self.x < 0):
            self.x += width
        if(self.y < 0):
            self.y += height
        self.x = self.x % width
        self.y = self.y % height
        
    #AI methods
    def randomAction(self): #Small chance of a left or right turn
        r = int(random.randrange(0, 100))
        if r == 1:
            self.turnLeft()
        elif r == 2:
            self.turnRight()
    def randomChoice(self): #1 in 3 chance for left, right, or straight
        num = random.randint(0, 2)
        if(num == 1):
            self.turnRight()
        elif(num == 2):
            self.turnLeft()
        else:
            pass
    def randomLeftOrRight(self):
        num = random.randint(1, 2)
        if(num == 1):
            self.turnRight()
        elif(num == 2):
            self.turnLeft()
    def AIAction(self, GRID, SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE):
        if random.randint(0, 3) >= 1: #Makes a smart decision 75% of the time, otherwise random
            if(self.getDir() == "Left" and self.findLeftBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT) != None):
                num = GRID[self.findLeftBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)]
                if(num in self.deathNums or num == self.number):
                    self.randomLeftOrRight() #If going to collide with somthing going left, avoid it
            elif(self.getDir() == "Right" and self.findRightBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT) != None):
                num = GRID[self.findRightBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)]
                if(num in self.deathNums or num == self.number):
                    self.randomLeftOrRight() #If going to collide with somthing going right, avoid it
            elif(self.getDir() == "Up" and self.findUpBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT) != None):
                num = GRID[self.findUpBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)]
                if(num in self.deathNums or num == self.number):
                    self.randomLeftOrRight() #If going to collide with somthing going up, avoid it
            elif(self.getDir() == "Down" and self.findDownBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT) != None):
                num = GRID[self.findDownBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)]
                if(num in self.deathNums or num == self.number):
                    self.randomLeftOrRight() #If going to collide with somthing going down, avoid it
        else:
            self.randomChoice()