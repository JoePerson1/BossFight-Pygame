import pygame

from sprites import *
from functions import *

class Character(NotSquare):
  def __init__(self, picture, pos, scale):
    NotSquare.__init__(self, picture, pos, scale)
    self.speed = 5
    self.lastKey = None
    self.isDash = False
    self.defaultDashDuration = 5
    self.dashDuration = self.defaultDashDuration
    self.dashSpeed = 20  # TODO add lerp to dash (and basically like half the moves)
    
    self.invincible = True
  
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
  def dash(self, display, keyPresses):
    if not self.isDash:
      trueKey = None
      sumKeys = 0
      for key, value in list(keyPresses.items())[:4]:
        if value:
          sumKeys += value
          trueKey = key
        if key == pygame.K_d and sumKeys == 1:
          if self.lastKey == trueKey:
            self.isDash = True
            self.dashDuration = self.defaultDashDuration
          self.lastKey = trueKey
    
    if self.isDash:
      # display.blit(self.image, self.rect)  # TODO make it a dif class so it blits
      self.dashDuration -= 1
      try:
        if self.lastKey == pygame.K_w:
          self.decimal[1] -= self.dashSpeed
        elif self.lastKey == pygame.K_a:
          self.decimal[0] -= self.dashSpeed
        elif self.lastKey == pygame.K_s:
          self.decimal[1] += self.dashSpeed
        elif self.lastKey == pygame.K_d:
          self.decimal[0] += self.dashSpeed
      except TypeError:
        pass
      if self.dashDuration == 0:
        self.isDash = False
        self.lastKey = None
    
class Enemy(NotSquare):
  def __init__(self, picture, pos, scale):
    self.hitbox = None
  def hitbox(self, pos, size):
    Square.__init__(self.hitbox, pos, size)
  
class Boss(NotSquare):  # TODO make class for general (toPlayerVector and collide death) and speed
  def __init__(self, picture, pos, scale):
    NotSquare.__init__(self, picture, pos, scale)
    self.startMove = 0
    
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
    
  def follow(self, character, speed):
    self.decimal += toCharacterVector(character.rect.center, self.rect.center) * speed
    self.rect.center = self.decimal
  
  def cleave(self, character, reelTime, reelDistance, reelLerp, attackTime, attackDistance, attackLerp):
    if self.startMove == 0:
      self.totalMoveTime = reelTime + attackTime
    self.startMove += 1
    if self.startMove % self.totalMoveTime < reelTime:
      self.decimal -=\
        toCharacterVector(character.rect.center, self.rect.center) * reelDistance * reelLerp  # TODO make reelLerp work
    elif self.startMove % self.totalMoveTime == reelTime:
      self.stillCharacterVector = targetPos(character.rect.center, self.rect.center, attackDistance)
    elif self.startMove % self.totalMoveTime > reelTime:
      self.decimal += \
        (self.stillCharacterVector - self.rect.center) * attackLerp
    self.rect.center = self.decimal
  