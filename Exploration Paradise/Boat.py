import pygame as pg
import collections
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from Terrain import Colors

class Boat(pg.sprite.Sprite):
    
    def __init__(self, image, xLoc, yLoc, max_acceleration = 0.0001, max_steering = 45):
        #Graphics
        pg.sprite.Sprite.__init__(self)
        self.image = image.convert_alpha() #This gets the clear image backgrounds
        
        #Physics
        self.position = Vector2(xLoc, yLoc)
        self.velocity = Vector2(0.0, 0.0)
        self.acceleration = 0.0
        self.angle = 0
        self.steering = 0.0
        
        #Characteristics
        #self.length = 100.0
        #self.width = 50.0
        self.length = self.image.get_size()[0]
        self.width = self.image.get_size()[1]
        self.max_acceleration = max_acceleration #Default is 0.001
        self.max_steering = max_steering #Default is 1
        self.max_velocity = 0.25
        self.brake_deceleration = 5.0
        self.free_deceleration = 0.5

    def update(self, dt, current_terrain):
        self.max_velocity = 0.25
        if collections.Counter(current_terrain) == collections.Counter(Colors.OCEAN):
            self.max_velocity = 0.5
            print("Ocean")
        elif collections.Counter(current_terrain) == collections.Counter(Colors.SAND):
            self.max_velocity = 0.05
            print("SAnd")
        elif collections.Counter(current_terrain) == collections.Counter(Colors.GRASS):
            self.max_velocity = 0.01
            print("GRass")
            
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        angular_velocity = 0
        if self.steering != 0.0:
            angular_velocity = self.velocity.x / (self.length / sin(radians(self.steering)))
        
        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
        
    def getInput(self, pressed, dt):
        if pressed[pg.K_UP]:
                if self.velocity.x < 0:
                    self.acceleration = self.brake_deceleration
                else:
                    self.acceleration += 1 * dt
        elif pressed[pg.K_DOWN]:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= 1 * dt
        elif pressed[pg.K_SPACE]:
            if abs(self.velocity.x) > dt * self.brake_deceleration:
                self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / dt
        else:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

        if pressed[pg.K_RIGHT]:
            self.steering -= 30 * dt
        elif pressed[pg.K_LEFT]:
            self.steering += 30 * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))
        
    def draw(self, screen, middleX, middleY):
        rotated = pg.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, (middleX - rect.width / 2, middleY - rect.height / 2))
        #screen.blit(rotated, (self.position.x - rect.width / 2, self.position.y - rect.height / 2))