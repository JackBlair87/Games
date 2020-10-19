import pygame as pg
import numpy as np
from Boat import Boat
from Terrain import Terrain, Colors
 
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 800
WIDTH = 5000
HEIGHT = 5000

BLACK = (0, 0, 0)
YACHT = pg.image.load('Yacht.png')
RAFT = pg.image.load('Raft.png')
CRUISER = pg.image.load('Cruiser.png')
SELECTED_BOAT = YACHT

SCALE = 2000.0
OCTAVES = 5
PERSISTANCE = 0.5
LACUNARITY = 2.0 #Increases fine detail

def quitGame(): #Quits Pygame and Python
    pg.quit()
    quit()
    
def backgroundInputCheck(eventList): #Constantly checks for quits and enters
    for event in eventList:
            if event.type == pg.QUIT:
                quitGame()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quitGame()

def runGame():
    global WIDTH, HEIGHT, SCALE, OCTAVES, PERSISTANCE, LACUNARITY
    playerBoat = Boat(SELECTED_BOAT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    SEED = np.random.randint(0, 100)
    world = Terrain(HEIGHT, WIDTH)
    world.generateTopTerrain(SCALE, OCTAVES, PERSISTANCE, LACUNARITY, SEED)
    world.generateTopColor(-0.2, 0.01, 0.055, 0.25, 0.33, 0.47, 0.55)
    image = pg.surfarray.make_surface(world.topColorTerrain).convert()
    
    while True:
        deltaTime = clock.get_time()
        backgroundInputCheck(pg.event.get())
        
        playerBoat.getInput(pg.key.get_pressed(), deltaTime)
        playerBoat.update(deltaTime, world.topColorTerrain[len(world.topColorTerrain) - int(playerBoat.position.x)][len(world.topColorTerrain[0]) - int(playerBoat.position.y)])
        
        screen.fill(BLACK)
        screen.blit(image, (-playerBoat.position.x, -playerBoat.position.y))
        playerBoat.draw(screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        
        clock.tick(60)
        pg.display.flip()
           
pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("Exploration Paradise")
clock = pg.time.Clock()
runGame()