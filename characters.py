import pygame.time

from sprites import *

class Character(NotSquare):
  def __init__(self, picture, pos, speed, scale):
    NotSquare.__init__(self, picture, pos, speed, scale)
    
    self.lastKey = None
    self.isDash = False
    self.dashKey = None
  
  def movement(self, keys, arena):
    horizontalMovement = keys[pygame.K_d] - keys[pygame.K_a]
    verticalMovement = keys[pygame.K_s] - keys[pygame.K_w]
    
    vector = pygame.math.Vector2(horizontalMovement, verticalMovement)
    if vector[0] != 0 or vector[1] != 0:
      vector = pygame.math.Vector2.normalize(vector)
    
    self.decimal += vector * self.speed
    self.rect.center = self.decimal
    
    if self.rect.left < arena.rect.left:
      self.rect.left = arena.rect.left
      self.decimal = self.rect.center
    if self.rect.right > arena.rect.right:
      self.rect.right = arena.rect.right
      self.decimal = self.rect.center
    if self.rect.top < arena.rect.top:
      self.rect.top = arena.rect.top
      self.decimal = self.rect.center
    if self.rect.bottom > arena.rect.bottom:
      self.rect.bottom = arena.rect.bottom
      self.decimal = self.rect.center
      
      # TODO make dash double press and not just hold
      # TODO make dash shorter time
  def dash(self, key):
    if key is not None:
     self.lastKey = key
    
    if not self.isDash:
      self.ticks1 = pygame.time.get_ticks()
      if self.lastKey == key:
        print(pygame.time.get_ticks())
        print(self.ticks1)
        print(pygame.time.get_ticks() - self.ticks1)
        ticks2 = pygame.time.get_ticks()
        if ticks2 - self.ticks1 < 10000:
          print('In Interval')
          self.isDash = True
          self.dashKey = self.lastKey
          self.dashSpeed = 100
    
    elif self.isDash:
      if self.dashKey == pygame.K_w:
        self.decimal[1] -= self.dashSpeed
      elif self.dashKey == pygame.K_s:
        self.decimal[1] += self.dashSpeed
      elif self.dashKey == pygame.K_a:
        self.decimal[0] -= self.dashSpeed
      elif self.dashKey == pygame.K_d:
        self.decimal[0] += self.dashSpeed
        
      self.dashSpeed -= self.dashSpeed*.1
      print('dashSpeed: '+str(self.dashSpeed))
        
      print(pygame.time.get_ticks(), self.ticks1, self.isDash)
      if pygame.time.get_ticks() - self.ticks1 > 10000:
       self.isDash = False
  
    print(self.lastKey, key)
  
class Boss(NotSquare):
  def __init__(self, picture, pos, speed, scale):
    NotSquare.__init__(self, picture, pos, speed, scale)
    
  def movement(self, arena):
    if self.rect.left < arena.rect.left:
      self.rect.left = arena.rect.left
      self.decimal = self.rect.center
    if self.rect.right > arena.rect.right:
      self.rect.right = arena.rect.right
      self.decimal = self.rect.center
    if self.rect.top < arena.rect.top:
      self.rect.top = arena.rect.top
      self.decimal = self.rect.center
    if self.rect.bottom > arena.rect.bottom:
      self.rect.bottom = arena.rect.bottom
      self.decimal = self.rect.center
    
    