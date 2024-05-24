import pygame.key

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
    
  def run(self, gameSquare, reRender, keyPresses):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      ratio = 7 / 8
      
      self.arena = Square(((gameSquare.image.get_width() / 2) + gameSquare.rect.left, 0),
                          (gameSquare.image.get_width(), gameSquare.image.get_height() * ratio),
                          'black')
      self.arena.rect.top = gameSquare.rect.top
      self.ui = Square(((gameSquare.image.get_width() / 2) + gameSquare.rect.left, 0),
                       (gameSquare.image.get_width(), gameSquare.image.get_height() * (1 - ratio)),
                       'white')
      self.ui.rect.bottom = gameSquare.rect.bottom
      self.character = Character('assets/character.png',
                                 (2 * (gameSquare.image.get_width() // 8) + gameSquare.rect.left,
                                 gameSquare.rect.centery), (20, 20))
      self.boss = NotSquare('assets/boss.png',
                            (6 * (gameSquare.image.get_width() // 8) + gameSquare.rect.left,
                            gameSquare.rect.centery), (50, 50))
      
      reRender = False
    
    keys = pygame.key.get_pressed()
    self.modeStates[self.gameStateManager.getMode()].run(self.display, self.gameStateManager)
    
    self.character.movement(keys, self.arena)
    self.character.dash(keyPresses)
    
    self.display.blit(self.arena.image, self.arena.rect)
    self.display.blit(self.ui.image, self.ui.rect)
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

  