#Created by Jack Blair - April, 2020
import pygame as pg #For graphics
import random #For random player movements
import numpy as np
import math as m

from Particles import ParticleManager, Particle
from Element import Element

#Graphics and Images
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (202, 105, 46) #LAVA
BLUE = (50, 50, 200) #WATER
GREEN = (50, 200, 50) #ACID
PURPLE = (100, 32, 117) #POISON
RED = (200, 50, 50)
GRAY = (50, 50, 50)
LAVA = pg.image.load('Lava.png')
WATER = pg.image.load('Water.png')
ACID = pg.image.load('Acid.png')
POISON = pg.image.load('Poison.png')

#Main Settings
SCREEN_WIDTH = 1440 #Must be divisible by SQUARE_SIZE
SCREEN_HEIGHT = 800 #Must be divisible by SQUARE_SIZE
SQUARE_SIZE = 32
MODE = "BINARY" #BINARY OR QUAD
CONTROL = "ARROW" #ARROW or LETTER
PLAYER_SPEED = 5 #How fast gameplay is
PLAYER_CONTROLLED = "LAVA" #Which Element is controlled by the player (LAVA, ACID, WATER, POISON, RANDOM)
PLAYER = "" #What the actual player will be (After random assignment)
FPS = 60 #Standard Smooth FPS

GRID = np.zeros([int(SCREEN_WIDTH/SQUARE_SIZE), int(SCREEN_HEIGHT/SQUARE_SIZE)], dtype=int)
#print("Grid Size:", int(SCREEN_WIDTH/SQUARE_SIZE), "by", int(SCREEN_HEIGHT/SQUARE_SIZE))
print("GAME ", SCREEN_WIDTH, "x", SCREEN_HEIGHT, " at ", FPS, " FPS", ", Controlled with ", MODE, " ", CONTROL, " at speed ", PLAYER_SPEED, " with player ", PLAYER_CONTROLLED, sep = '')

def clearGrid(num): #Wipes the grid to whatever number given (0 is reset)
    global GRID 
    for x in range(0, len(GRID)):
        for y in range(0, len(GRID[0])):
            GRID[x, y] = num
            
def quitGame(): #Quits Pygame and Python
    pg.quit()
    quit()

def randomPlayer(): #Determines the player if the choice was random
    num = random.randint(1, 4)
    if num == 1:
        return "LAVA"
    elif num == 2:
        return "POISON"
    elif num == 3:
        return "ACID"
    elif num == 4:
        return "WATER"

def backgroundInputCheck(eventList): #Constantly checks for quits and enters
    for event in eventList:
            if event.type == pg.QUIT:
                quitGame()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return False
                elif event.key == pg.K_RETURN:
                    return False
                elif event.key == pg.K_ESCAPE:
                    quitGame()
    return True
 
def drawTrails(screen, color1, color2, color3, color4): #Draws back trails
    global GRID, SQUARE_SIZE
    for x in range(0, len(GRID)):
        for y in range(0, len(GRID[0])):
            if(GRID[(x, y)] != 0):
                if(GRID[(x, y)] == 1):
                    pg.draw.rect(screen, color1, [SQUARE_SIZE*x, SQUARE_SIZE*y, SQUARE_SIZE, SQUARE_SIZE])
                elif(GRID[(x, y)] == 2):
                    pg.draw.rect(screen, color2, [SQUARE_SIZE*x, SQUARE_SIZE*y, SQUARE_SIZE, SQUARE_SIZE])
                elif(GRID[(x, y)] == 3):
                    pg.draw.rect(screen, color3, [SQUARE_SIZE*x, SQUARE_SIZE*y, SQUARE_SIZE, SQUARE_SIZE])
                elif(GRID[(x, y)] == 4):
                    pg.draw.rect(screen, color4, [SQUARE_SIZE*x, SQUARE_SIZE*y, SQUARE_SIZE, SQUARE_SIZE])  

def drawPlayers(screen, playerList): #Draws all the living players
    for player in playerList: #Draw Players
            player.particleList.drawParticles(screen)
            screen.blit(player.image, [player.x, player.y])
 
def addTrail(player): #Adds the trail of the player depending on which direction they are going
    if(player.getDir() == "Left"):
        point = player.findRightBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
    elif player.getDir() == "Right":
        point = player.findMyBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
    elif player.getDir() == "Up":
        point = player.findDownBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
    elif player.getDir() == "Down":
        point = player.findMyBox(SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
         
    if point != None:
        GRID[point] = player.number

def writeText(screen, font, size, text, x, y, color):
    smallText = pg.font.SysFont(font, size)
    textSurf = smallText.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    screen.blit(textSurf, textRect)

def getColor(elementName):
    if elementName == "LAVA":
        return ORANGE
    elif elementName == "POISON":
        return PURPLE
    elif elementName == "ACID":
        return GREEN
    elif elementName == "WATER":
        return BLUE
    else:
        return GRAY

def getImage(elementName):
    global LAVA, POISON, ACID, WATER
    if elementName == "LAVA":
        return LAVA
    elif elementName == "POISON":
        return POISON
    elif elementName == "ACID":
        return ACID
    elif elementName == "WATER":
        return WATER
    
def drawEyes(screen, waitTime, interval1, interval2, upOffset): #Draws animated eyes realtive to center of screen
    pg.draw.rect(screen, (255, 255, 255), (670, 340-upOffset, 40, 60))
    pg.draw.rect(screen, (255, 255, 255), (750, 340-upOffset, 40, 60))
    if(waitTime < interval1 or waitTime > interval2):
        pg.draw.rect(screen, (0, 0, 0), (690, 360-upOffset, 20, 40))
        pg.draw.rect(screen, (0, 0, 0), (770, 360-upOffset, 20, 40))
    else:
        pg.draw.rect(screen, (0, 0, 0), (670, 360-upOffset, 20, 40))
        pg.draw.rect(screen, (0, 0, 0), (750, 360-upOffset, 20, 40))
        
def switchButton(msg, x, y, w, h, ic, ac): #Button that loops through options, like in settings
    global PLAYER, PLAYER_CONTROLLED
    writeText(screen, "arial", 50, msg, (x+(w/2)), (y+(h/2)), WHITE)
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1:
            return True
    else:
        pg.draw.rect(screen, ic,(x,y,w,h))
    writeText(screen, "arial", 50, msg, (x+(w/2)), (y+(h/2)), WHITE)
    return False
    
def createButton(text, x, y, w, h, ic, ac, action = None): #Normal button that preforms an action
    global PLAYER, PLAYER_CONTROLLED
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pg.draw.rect(screen, ic,(x,y,w,h))
    writeText(screen, "arial", 50, text, (x+(w/2)), (y+(h/2)), WHITE)
    
def makeOrder(players): #Sets the subs and supers given a list
    if(len(players) == 4):
        players[0].setSuper(players[1])
        players[1].setSuper(players[2])
        players[2].setSuper(players[3])
        players[3].setSuper(players[0])
        players[0].setSub(players[3])
        players[1].setSub(players[0])
        players[2].setSub(players[1])
        players[3].setSub(players[2])
    else:
        return None

def assignPlayer():
    global PLAYER_CONTROLLED, PLAYER    
    if(PLAYER_CONTROLLED == "RANDOM"):
        PLAYER = randomPlayer()
    else:
        PLAYER = PLAYER_CONTROLLED
        
def setFPS(): #Cycles through FPS options
    global FPS
    if(FPS == 25):
        FPS = 30
    elif(FPS == 30):
        FPS = 60
    elif(FPS == 60):
        FPS = 120
    elif(FPS == 120):
        FPS = 25
    
def setSpeed():
    global PLAYER_SPEED
    if(PLAYER_SPEED == 5):
        PLAYER_SPEED = 10
    elif(PLAYER_SPEED == 10):
        PLAYER_SPEED = 3
    elif(PLAYER_SPEED == 3):
        PLAYER_SPEED = 5
       
def setElement():
    global PLAYER_CONTROLLED
    if(PLAYER_CONTROLLED == "RANDOM"):
        PLAYER_CONTROLLED = "LAVA"
    elif(PLAYER_CONTROLLED == "LAVA"):
        PLAYER_CONTROLLED = "POISON"
    elif(PLAYER_CONTROLLED == "POISON"):
        PLAYER_CONTROLLED = "ACID"
    elif(PLAYER_CONTROLLED == "ACID"):
        PLAYER_CONTROLLED = "WATER"
    elif(PLAYER_CONTROLLED == "WATER"):
        PLAYER_CONTROLLED = "RANDOM"

def setArrows():
    global CONTROL
    if(CONTROL == "LETTER"):
        CONTROL = "ARROW"
    elif(CONTROL == "ARROW"):
        CONTROL = "LETTER" 
        
def setMode():
    global MODE
    if(MODE == "BINARY"):
        MODE = "QUAD"
    elif(MODE == "QUAD"):
        MODE = "BINARY"      
       
#Screens   
def mainScreen():
    onMain = True
    p1 = Element(PLAYER_SPEED, 0, SCREEN_WIDTH/8, SCREEN_HEIGHT/4, PLAYER_SPEED, LAVA, "LAVA", ORANGE) #LAVA
    p2 = Element(0, -PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT/2, PLAYER_SPEED, POISON, "POISON", PURPLE) #POISON
    p3 = Element(-PLAYER_SPEED, 0, SCREEN_WIDTH/2 - SQUARE_SIZE, SCREEN_HEIGHT/2, PLAYER_SPEED, ACID, "ACID", GREEN) #ACID
    p4 = Element(0, PLAYER_SPEED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + SQUARE_SIZE, PLAYER_SPEED, WATER, "WATER", BLUE) #WATER
    playerList = [p1, p2, p3, p4]
    
    while onMain:
        if not backgroundInputCheck(pg.event.get()): #If SPACE or ENTER then play game
            gameScreen()
                    
        for player in playerList:
            player.randomAction()
            player.update(SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE) #Update location
            addTrail(player)
        
        #Draw on Screen
        screen.fill(BLACK) #Paint the whole screen black
        drawTrails(screen, ORANGE, PURPLE, GREEN, BLUE)
        drawPlayers(screen, playerList)
        
        writeText(screen, "arial", 350, "ELEMENTAL", (SCREEN_WIDTH/2), (SCREEN_HEIGHT/3), WHITE)
        createButton("START",350,450,740,250,GRAY,GREEN,gameScreen)
        createButton("QUIT",50,450,250,100,GRAY,RED,quitGame)
        createButton("SETTINGS",50,600,250,100,GRAY,PURPLE,settingsScreen)
        createButton("INSTRUCTIONS",1140,450,250,100,GRAY,BLUE,instructionsScreen)
        createButton("CREDITS",1140,600,250,100,GRAY,ORANGE,creditsScreen)

        pg.display.update()
        clock.tick(60)
    
def introScreen(elementName):
    global SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER, FPS, MODE, CONTROL, LAVA, WATER, POISON, ACID, GRID, PLAYER_CONTROLLED
    waitTime = 0
    
    player = Element(0, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0, getImage(elementName), elementName, getColor(elementName))
    bigTrail = ParticleManager((4.5*SCREEN_WIDTH/10, SCREEN_HEIGHT/2 + 40), (20, 0), 30, player.color, player.name, 0.999, 100)
    longTrail = ParticleManager((4.5*SCREEN_WIDTH/10, SCREEN_HEIGHT/2), (15, 0), 30, player.color, player.name, 0.9999, 100)
    newImage = pg.transform.scale(player.image, (160, 160))
    
    while waitTime < 120:
        backgroundInputCheck(pg.event.get())
                    
        bigTrail.update(player.color, player.name, (4.5*SCREEN_WIDTH/10, SCREEN_HEIGHT/2 + 40), (15, 0), 100)
        longTrail.update(player.color, player.name, (4.5*SCREEN_WIDTH/10, SCREEN_HEIGHT/2), (20, 0), 100)
                    
        screen.fill(BLACK) #Paint the whole screen black
        bigTrail.drawParticles(screen)
        longTrail.drawParticles(screen)
        screen.blit(newImage, [SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 - 80])
        drawEyes(screen, waitTime, 60, 90, 0)
        
        waitTime += 1
        clock.tick(60)
        pg.display.flip()
    
def gameScreen():
    global GRID, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER, CONTROL, MODE, FPS
    hasWinner = False
    explosionList = []
    currentInterval = 1
    clearGrid(0)
    assignPlayer()
    
    lava = Element(PLAYER_SPEED, 0, SCREEN_WIDTH/2 + SQUARE_SIZE, SCREEN_HEIGHT/2, PLAYER_SPEED, LAVA, "LAVA", ORANGE) #LAVA
    poison = Element(0, -PLAYER_SPEED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - SQUARE_SIZE, PLAYER_SPEED, POISON, "POISON", PURPLE) #POISON
    acid = Element(-PLAYER_SPEED, 0, SCREEN_WIDTH/2 - SQUARE_SIZE, SCREEN_HEIGHT/2, PLAYER_SPEED, ACID, "ACID", GREEN) #ACID
    water = Element(0, PLAYER_SPEED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + SQUARE_SIZE, PLAYER_SPEED, WATER, "WATER", BLUE) #WATER
    playerList = [lava, poison, acid, water]
    makeOrder(playerList)
    
    for element in playerList:
        if element.name == PLAYER:
            p1 = element
       
    introScreen(p1.name)
    while not hasWinner:
        #Handle input control
        if(MODE == "BINARY" and CONTROL == "ARROW"): #Left-Right arrow movement system
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print(GRID)
                    quitGame()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        p1.turnLeft()
                    elif event.key == pg.K_RIGHT:
                        p1.turnRight()
                    elif event.key == pg.K_ESCAPE:
                        quitGame()
        elif(MODE == "BINARY" and CONTROL == "LETTER"): #A-D movement system
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print(GRID)
                    quitGame()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        p1.turnLeft()
                    elif event.key == pg.K_d:
                        p1.turnRight()
                    elif event.key == pg.K_ESCAPE:
                        quitGame()    
        elif(MODE == "QUAD" and CONTROL == "ARROW"): #UP-DOWN-LEFT-RIGHT movement System
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print(GRID)
                    quitGame()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        if(p1.change_y != p1.maxSpeed):
                            p1.goUp()
                    elif event.key == pg.K_LEFT:
                        if(p1.change_x != p1.maxSpeed):
                            p1.goLeft()
                    elif event.key == pg.K_DOWN:
                        if(p1.change_y != -p1.maxSpeed):
                            p1.goDown()
                    elif event.key == pg.K_RIGHT:
                        if(p1.change_x != -p1.maxSpeed):
                            p1.goRight()
                    elif event.key == pg.K_ESCAPE:
                        quitGame()
        elif(MODE == "QUAD" and CONTROL == "LETTER"): #WASD movement System
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print(GRID)
                    quitGame()
                elif event.type == pg.KEYDOWN:             
                    if event.key == pg.K_w:
                        if(p1.change_y != p1.maxSpeed):
                            p1.goUp()
                    elif event.key == pg.K_a:
                        if(p1.change_x != p1.maxSpeed):
                            p1.goLeft()
                    elif event.key == pg.K_s:
                        if(p1.change_y != -p1.maxSpeed):
                            p1.goDown()
                    elif event.key == pg.K_d:
                        if(p1.change_x != -p1.maxSpeed):
                            p1.goRight()
                     
        #Handle Logic
        for player in playerList:
            if(player != p1 and currentInterval % player.AIchoiceInterval == 0): #AI for other players
                player.AIAction(GRID, SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE)
            player.update(SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE) #Update location
            if(player.willDie(GRID, SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE)): #If the player dies
                print("Player", player.name, "was killed")
                player.sub.setSuper(player.super)
                player.super.setSub(player.sub)
                explosionList.append(ParticleManager((player.x, player.y), (0, 0), 40, player.color, player.name, 0.9, 1))
                playerList.remove(player)
                #print(player.sub.name, "-", player.name, "-", player.super.name, "-->", player.sub.name, "-", player.super.name)
            
            addTrail(player)
        
        if(len(playerList) == 1): #If only one player is still alive
            hasWinner = True
            
        for e in explosionList:
            e.fadeUpdate()
       
        #Draw on Screen
        screen.fill(BLACK) #Paint the whole screen black
        drawTrails(screen, ORANGE, PURPLE, GREEN, BLUE)
        drawPlayers(screen, playerList)
        pg.draw.rect(screen, GRAY, [SCREEN_WIDTH//2 - SQUARE_SIZE*1.5, SCREEN_HEIGHT//2 - SQUARE_SIZE*1.5, SQUARE_SIZE*3, SQUARE_SIZE*3])
        
        for e in explosionList:
            e.drawParticles(screen)
            
        currentInterval += 1
        clock.tick(FPS)
        pg.display.flip()
        
    winnerScreen(playerList[0], explosionList, p1)
    clearGrid(0)

def winnerScreen(playerWinner, particleList, controlledPlayer):
    global GRID, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER, CONTROL, MODE, FPS
    print(playerWinner.name, "won!")
    GRID[22][12] = playerWinner.number
    restTime = 0
    
    while restTime < FPS*2:
        backgroundInputCheck(pg.event.get())
        
        playerWinner.update(SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE) #Update location
        addTrail((playerWinner))
        
        for e in particleList:
            e.fadeUpdate()
                
        particleList.append(ParticleManager((random.random()*SCREEN_WIDTH, random.random()*SCREEN_HEIGHT), (0, 0), 10, playerWinner.color, playerWinner.name, 0.999, 1))
        
        screen.fill(BLACK) #Paint the whole screen black
        drawTrails(screen, playerWinner.color, playerWinner.color, playerWinner.color, playerWinner.color)
        drawPlayers(screen, [playerWinner])
        
        if(playerWinner == controlledPlayer):
            writeText(screen, "arial", 250, "VICTORY", (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2), WHITE)
        
        for e in particleList:
            e.drawParticles(screen)
              
        restTime += 1
        clock.tick(FPS)
        pg.display.flip()

def instructionsScreen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER, FPS, MODE, CONTROL, LAVA, WATER, POISON, ACID, GRID, PLAYER_CONTROLLED

    offset = 125
    newLava = pg.transform.scale(LAVA, (160, 160))
    newPosion = pg.transform.scale(POISON, (160, 160))
    newAcid = pg.transform.scale(ACID, (160, 160))
    newWater = pg.transform.scale(WATER, (160, 160))
    
    onInstructions = True
    restTime = 0
    clearGrid(0)  
      
    while onInstructions:
        onInstructions = backgroundInputCheck(pg.event.get())
        
        screen.fill(BLACK) #Paint the whole screen black
        screen.blit(newLava, [SCREEN_WIDTH/2 -80 + offset, SCREEN_HEIGHT/3.5 - 80 - offset])
        screen.blit(newPosion, [SCREEN_WIDTH/2 -80 - offset, SCREEN_HEIGHT/3.5 - 80 - offset])
        screen.blit(newAcid, [SCREEN_WIDTH/2 -80 - offset, SCREEN_HEIGHT/3.5 - 80 + offset])
        screen.blit(newWater, [SCREEN_WIDTH/2 -80 + offset, SCREEN_HEIGHT/3.5 - 80 + offset])
        writeText(screen, "arial", 50, "LAVA", SCREEN_WIDTH/2 + offset, SCREEN_HEIGHT/3.5 - offset + 120, ORANGE)
        writeText(screen, "arial", 50, "POISON", SCREEN_WIDTH/2 - offset, SCREEN_HEIGHT/3.5 - offset + 120, PURPLE)
        writeText(screen, "arial", 50, "ACID", SCREEN_WIDTH/2 - offset, SCREEN_HEIGHT/3.5 + offset + 120, GREEN)
        writeText(screen, "arial", 50, "WATER", SCREEN_WIDTH/2 + offset, SCREEN_HEIGHT/3.5 + offset + 120, BLUE)
        writeText(screen, "arial", 50, "Elemental is like Rock-Paper-Scissors, every element can beat one other.", (SCREEN_WIDTH/2), (2*SCREEN_HEIGHT/3), WHITE)
        writeText(screen, "arial", 45, "LAVA beats WATER, WATER beats ACID, ACID beats POISON, and POISON beats LAVA.", (SCREEN_WIDTH/2), (2*SCREEN_HEIGHT/3 + 50), WHITE)
        writeText(screen, "arial", 50, "If the element that beats you dies, the one that beat it is now trying to beat you.", (SCREEN_WIDTH/2), (2*SCREEN_HEIGHT/3 + 100), WHITE)
        writeText(screen, "arial", 50, "Make sure not to cross over the tracks of any old elements that could still beat you!", (SCREEN_WIDTH/2), (2*SCREEN_HEIGHT/3 + 150), WHITE)
        
        if(restTime > 180):
            writeText(screen, "arial", 25, "-SPACEBAR to return to MAIN-", (SCREEN_WIDTH/2), (SCREEN_HEIGHT-50), WHITE)

        restTime += 1
        clock.tick(60)
        pg.display.flip()
    
def settingsScreen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER, FPS, MODE, CONTROL, LAVA, WATER, POISON, ACID, GRID, PLAYER_CONTROLLED
    player = Element(0, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0, LAVA, "LAVA", ORANGE)
    newImage = pg.transform.scale(player.image, (160, 160))
    clearGrid(0)
    restTime = 0      
    onSettings = True  
    
    while onSettings:
        onSettings = backgroundInputCheck(pg.event.get())
        
        screen.fill(BLACK) #Paint the whole screen black
        screen.blit(newImage, [SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 - 230])
        drawEyes(screen, restTime, 60, 140, 150)

        if switchButton("SPEED " + str(PLAYER_SPEED),50,450,250,100,GRAY,RED) and restTime > 15:
            setSpeed()
            restTime = 0
        if switchButton(str(PLAYER_CONTROLLED),350,450,740,250,GRAY, getColor(PLAYER_CONTROLLED)) and restTime > 15:
            setElement()
            restTime = 0
        if switchButton(str(FPS) + " FPS",50,600,250,100,GRAY,GREEN) and restTime > 15:
            setFPS()
            restTime = 0
        if switchButton(str(CONTROL),1140,450,250,100,GRAY,BLUE) and restTime > 15:
            setArrows()
            restTime = 0
        if switchButton(str(MODE),1140,600,250,100,GRAY,ORANGE) and restTime > 15:
            setMode()
            restTime = 0
        
        if(restTime > 180):
            writeText(screen, "arial", 25, "-SPACEBAR to return to MAIN-", (SCREEN_WIDTH/2), (SCREEN_HEIGHT-50), WHITE)

        restTime += 1
        clock.tick(60)
        pg.display.flip()

def creditsScreen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER, FPS, MODE, CONTROL, LAVA, WATER, POISON, ACID, GRID, PLAYER_CONTROLLED

    player = Element(0, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0, LAVA, "LAVA", ORANGE)
    newImage = pg.transform.scale(player.image, (160, 160))
    
    onCredits = True
    clearGrid(0)
    restTime = 0      
      
    while restTime < 300 and onCredits:
        onCredits = backgroundInputCheck(pg.event.get())
        
        screen.fill(BLACK) #Paint the whole screen black
        writeText(screen, "arial", 100, "Created by Jack Blair", (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2), WHITE)
        writeText(screen, "arial", 50, "Released April 2020", (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2)+70, WHITE)
        screen.blit(newImage, [SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 - 230])
        drawEyes(screen, restTime, 60, 140, 150)
        
        restTime += 1
        clock.tick(60)
        pg.display.flip()
    
pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("Elemental")
clock = pg.time.Clock()
mainScreen()