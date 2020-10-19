import noise
import numpy as np
from PIL import Image
import math
import pygame as pg

class Colors:
    OCEAN = [0, 128, 255]
    WATER = [0,191,255]
    SAND = [238, 214, 175]
    GRASS = [34,139,34]
    TREES = [0, 100, 0]
    ROCK = [139, 137, 137]
    SNOW = [255, 250, 250]
    SKY =  [135, 206, 235]

class Terrain:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.terrain = np.zeros((self.height, self.width))
        self.topColorTerrain = np.zeros((height, width, 3), dtype=np.uint8)

    def generateTopTerrain(self, scale, octaves, persistence, lacunarity, seed):
        for x in range(0, self.height):
            for y in range(0, self.width):
                self.terrain[x][y] = noise.pnoise2(x/scale, y/scale, octaves, persistence, lacunarity, self.height, self.width, seed)
            print("Generating Terrain:", 100*x/self.height, "%")
    
    def generateTopColor(self, DBLUE, BLUE, YELLOW, GREEN, DARKGREEN, GRAY, WHITE):
        for x in range(0, self.height):
            for y in range(0, self.width):
                if(self.terrain[x, y] < DBLUE):
                    self.topColorTerrain[x, y] = Colors.OCEAN
                elif(self.terrain[x, y] < BLUE):
                    self.topColorTerrain[x, y] = Colors.WATER
                elif(self.terrain[x, y] < YELLOW):
                    self.topColorTerrain[x, y] = Colors.SAND
                elif(self.terrain[x, y] < GREEN):
                    self.topColorTerrain[(x, y)] = Colors.GRASS
                elif(self.terrain[x, y] < DARKGREEN):
                    self.topColorTerrain[(x, y)] = Colors.TREES
                elif(self.terrain[x, y] < GRAY):
                    self.topColorTerrain[x, y] = Colors.ROCK
                else:
                    self.topColorTerrain[x, y] = Colors.SNOW
            print("Coloring Terrain:", 100*x/self.height, "%")
            
    def findMaxHeight(self):
        max = self.terrain[0][0]
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.terrain[y][x] > max:
                    max = self.terrain[y][x]
        return max
    
    def findMinHeight(self):
        min = self.terrain[0][0]
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.terrain[y][x] < min:
                    min = self.terrain[y][x]
        return min
                
    def drawTerrain(self):
        return Image.fromarray(self.topColorTerrain)
    
    def raiseTerrain(self, ammount):
        for y in range(0, len(self.terrain)):
            for x in range(0, len(self.terrain[0])):
                self.terrain[y][x] += ammount
    
    def printTerrain(self, screen):
        for y in range(0, len(self.terrain)):
            for x in range(0, len(self.terrain[0])):
                pg.draw.circle(screen, self.topColorTerrain[(x, y)], [x, y], 0)