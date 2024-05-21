import pygame

from characters import *

# TODO another Game-state-manager managing the modes and kits
# TODO make buttons work with sprites
# TODO add blits for the borders to prevent overlap

class Mode:
  def __init__(self, display, gameStateManager):
    self.display = display
    self.gameStateManager = gameStateManager
    
    self.easy = EasyMode(self.display, self.gameStateManager)
    self.normal = NormalMode(self.display, self.gameStateManager)
    self.hard = HardMode(self.display, self.gameStateManager)
    
    self.modeStates = {'easy': self.easy, 'normal': self.normal, 'hard': self.hard}
    
    self.start = True
    
  def run(self, gameSquare, reRender, key):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      ratio = 7 / 8
      
      self.arena = Square(((gameSquare.image.get_width() / 2) + gameSquare.rect.left,
                          (gameSquare.image.get_height() * (ratio / 2)) + gameSquare.rect.top),
                          (gameSquare.image.get_width(), gameSquare.image.get_height() * ratio),
                          'black')
      self.ui = Square(((gameSquare.image.get_width() / 2) + gameSquare.rect.left,
                       (gameSquare.image.get_height() * ((1 - ratio) / 2)) + gameSquare.rect.top),
                       (gameSquare.image.get_width(), gameSquare.image.get_height() * (1 - ratio)),
                       'black')
      
      self.character = Character('assets/character.png',
                                 (2 * (gameSquare.image.get_width() // 8) + gameSquare.rect.left,
                                 gameSquare.rect.centery), 5, (20, 20))
      self.boss = NotSquare('assets/boss.png',
                            (6 * (gameSquare.image.get_width() // 8) + gameSquare.rect.left,
                            gameSquare.rect.centery), 5, (50, 50))
      
      reRender = False
    
    keys = pygame.key.get_pressed()
    self.modeStates[self.gameStateManager.getMode()].run(self.display, self.gameStateManager)
    
    self.character.movement(keys, self.arena)
    dashKeys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    if key in dashKeys:
      self.character.dash(key)
    
    self.display.blit(self.arena.image, self.arena.rect)
    self.display.blit(self.character.image, self.character.rect)
    self.display.blit(self.boss.image, self.boss.rect)

class EasyMode:
  def __init__(self, display, gameStateManager):
    pass
  def run(self, gameSquare, reRender):
    pass
  
class NormalMode:
  def __init__(self, display, gameStateManager):
    pass
  def run(self, gameSquare, reRender):
    pass
  
class HardMode:
  def __init__(self, display, gameStateManager):
    pass
  def run(self, gameSquare, reRender):
    pass

  