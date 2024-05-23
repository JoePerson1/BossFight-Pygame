import pygame.time

from sprites import *

class Character(NotSquare):
  def __init__(self, picture, pos, speed, scale):
    NotSquare.__init__(self, picture, pos, speed, scale)
    
    self.lastKey = None
  
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
  def dash(self, keyPresses):
    sumKeys = 0
    for i, key in enumerate(list(keyPresses.values())[:3]):
      sumKeys += key
      if i == 3 and sumKeys == 1:
        self.lastKey = key
    
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
    
    