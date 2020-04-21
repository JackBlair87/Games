import pygame as pg #For graphics
import random #For random sizes
from operator import add

class ParticleManager: #Manages many tiny particles
    def __init__(self, vertPos, playerVector, numParticles, color, element, fade, sizeMultiplyer):
        self.pos = vertPos #Location
        self.fade = fade #How fast the particle shrinks
        self.prtList = [] #A private list of all the individual particles
        for x in range(numParticles):
            self.prtList.append(Particle(self.pos, (-playerVector[0] + random.randint(-3,3), -playerVector[1] + random.randint(-3,3)), self.fade, element, sizeMultiplyer))

    def update(self, color, element, position, playerVector, sizeMultiplyer): #Adds new particles (Like a sparkler)
        self.prtList.append(Particle(position, (-playerVector[0] + random.randint(-3,3), -playerVector[1] + random.randint(-3,3)), self.fade, element, sizeMultiplyer))
        for x in self.prtList: #Updates every particle in the list or removes it if it's too small
            if(x.size[0] > 1):
                x.update()
            else:
                self.prtList.remove(x)
                
    def fadeUpdate(self): #Doesn't add any new particles (Like a Firework)
        for x in self.prtList: #O(n)
            if(x.size[0] > 1):
                x.update()
            else:
                self.prtList.remove(x)
    
    def drawParticles(self, screen):
        for x in self.prtList: #O(n)
            x.render(screen)
        
class Particle:
    def __init__(self, pos, vel, fade, element, sizeMult):
        self.position = (int(pos[0]), int(pos[1]))
        self.velocity = vel
        
        self.image = pg.image.load(element + ".png").convert()
        self.size = self.image.get_size()
        newSize = random.random() * sizeMult #Makes a general random starting size
        self.newImage = pg.transform.scale(self.image, (int(self.size[0]*newSize), int(self.size[1]*newSize)))
        self.fadeMult = fade
        
    def update(self):
        self.position = list(map(add, self.position, self.velocity)) #add current position to velocity for X and Y
        self.newImage = pg.transform.scale(self.image, (int(self.size[0]*self.fadeMult), int(self.size[1]*self.fadeMult))) #Scales to new size
        self.size = self.newImage.get_size() #and updates the private fields

    def render(self, screen):
        screen.blit(self.newImage, self.position)