import sys
import time

from modes import *
from gameStateManager import *

# DO NOT resize the window while fighting, will cause issues

FPS = 60


class Game:
  def __init__(self):
    pygame.init()
    info = pygame.display.Info()
    self.monitorWidth = info.current_w
    self.monitorHeight = info.current_h
    
    windowWidth = 1920
    windowHeight = 1080
    self.gameSquare = Square((windowWidth / 2, windowHeight / 2),
                             (windowWidth, windowHeight))
    self.screen = pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)
    self.clock = pygame.time.Clock()
    
    self.reRender = True
    self.gameStateManager = GameStateManager('main')
    
    self.main = MainMenu(self.screen, self.gameStateManager)
    self.play = PlayOptions(self.screen, self.gameStateManager)
    self.settings = Settings(self.screen, self.gameStateManager)
    self.mode = Mode(self.screen, self.gameStateManager)
    
    self.states = {'main': self.main, 'play': self.play, 'settings': self.settings, 'mode': self.mode}
    
    self.lastSingleKey = None
    self.dash = False
    self.keyPressDict = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False,
                         pygame.K_SPACE: False}
  
  def run(self):
    while True:
      keyDownCount = 0
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.VIDEORESIZE:
          self.reRender = True
          windowWidth, windowHeight = pygame.display.get_surface().get_size()
          print('windowWidth: ' + str(windowWidth) + ' | WindowHeight: ' + str(windowHeight))  # TODO delete later
          self.TL = Square((windowWidth / 2, windowHeight / 2), (windowWidth, windowHeight), 'black')
          self.BR = Square((windowWidth / 2, windowHeight / 2), (windowWidth, windowHeight), 'black')
          if windowWidth > windowHeight * (16 / 9):
            self.gameSquare = Square((windowWidth / 2, windowHeight / 2),
                                     (windowHeight * (16 / 9), windowHeight))
            self.TL.rect.right = self.gameSquare.rect.left
            self.BR.rect.left = self.gameSquare.rect.right
          else:
            self.gameSquare = Square((windowWidth / 2, windowHeight / 2),
                                     (windowWidth, windowWidth * (9 / 16)))
            self.TL.rect.bottom = self.gameSquare.rect.top
            self.BR.rect.top = self.gameSquare.rect.bottom
            
            self.screen.blit(self.TL.image, self.TL.rect)
            self.screen.blit(self.BR.image, self.BR.rect)
        
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_w or event.key == pygame.K_s or \
              event.key == pygame.K_a or event.key == pygame.K_d:
            keyDownCount += 1
            singleKey = event.key
            print(keyDownCount)
      if keyDownCount == 1:
        if singleKey == self.lastSingleKey:
          print('ok')
        self.lastSingleKey = singleKey
      
      # TODO remove self.key later?
      self.key = None
      self.states[self.gameStateManager.getState()].run(self.gameSquare, self.reRender, self.key)
      self.reRender = False
      
      pygame.display.update()
      self.clock.tick(FPS)


class MainMenu:  # TODO make it so that it re-renders when it switches states
  def __init__(self, display, gameStateManager):
    self.display = display
    self.gameStateManager = gameStateManager
    self.start = True
  
  def run(self, gameSquare, reRender, key):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      self.background = gameSquare
      self.background.color = 'gray'
      
      self.title = Text('Assignment Four', (gameSquare.rect.centerx,
                                            gameSquare.image.get_height() * (1 / 8) + gameSquare.rect.top),
                        None, 'white', gameSquare.image.get_height() // 5, True)
      
      buttonStart = gameSquare.image.get_height() * (2 / 5) + gameSquare.rect.top
      buttonSpacing = gameSquare.image.get_height() * (1 / 5)
      
      self.playButton = Button((gameSquare.rect.centerx, buttonStart), (gameSquare.image.get_width() / 3,
                                                                        gameSquare.image.get_height() / 8), 'dark blue',
                               30)
      self.playButton.mergeText('Play', self.playButton.rect.center, None, 'white',
                                gameSquare.image.get_height() // 12)
      self.settingsButton = Button((gameSquare.rect.centerx, buttonStart + buttonSpacing),
                                   (gameSquare.image.get_width() / 3, gameSquare.image.get_height() / 8),
                                   'dark blue', 30)
      self.settingsButton.mergeText('Settings', self.settingsButton.rect.center, None, 'white',
                                    gameSquare.image.get_height() // 12)
      self.quitButton = Button((gameSquare.rect.centerx, buttonStart + 2 * buttonSpacing),
                               (gameSquare.image.get_width() / 3, gameSquare.image.get_height() / 8),
                               'dark blue', 30)
      self.quitButton.mergeText('Quit', self.quitButton.rect.center, None, 'white',
                                gameSquare.image.get_height() // 12)
    
    self.background.draw(self.display)
    self.playButton.draw(self.display)
    self.settingsButton.draw(self.display)
    self.quitButton.draw(self.display)
    self.display.blit(self.title.text, self.title.textRect)
    
    if self.playButton.pressed:
      self.gameStateManager.setState('play')
    elif self.settingsButton.pressed:
      self.gameStateManager.setState('settings')
    elif self.quitButton.pressed:
      pygame.quit()
      sys.exit()


class PlayOptions:  # TODO fix bug where if you hold a button you cant go back
  def __init__(self, display, gameStateManager):
    self.display = display
    self.gameStateManager = gameStateManager
    self.start = True
    self.highlightCount = 0
  
  def run(self, gameSquare, reRender, key):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      self.background = gameSquare
      self.background.color = 'gray'
      
      buttonStart = gameSquare.image.get_height() * (2 / 5) + gameSquare.rect.top
      buttonSpacing = gameSquare.image.get_height() * (1 / 5)
      
      self.title = Text('Select Your Difficulty', (gameSquare.rect.centerx,
                                                   gameSquare.image.get_height() * (1 / 8) + gameSquare.rect.top),
                        None, 'black', gameSquare.image.get_height() // 5)
      self.easyButton = Button((gameSquare.rect.centerx, buttonStart), (gameSquare.image.get_width() / 4,
                                                                        gameSquare.image.get_height() / 8), 'green', 15)
      self.easyButton.mergeText('Easy', self.easyButton.rect.center, None, 'black',
                                gameSquare.image.get_height() // 12)
      
      self.mediumButton = Button((gameSquare.rect.centerx, buttonStart + buttonSpacing),
                                 (gameSquare.image.get_width() / 4, gameSquare.image.get_height() / 8),
                                 'orange', 15)
      self.mediumButton.mergeText('Normal', self.mediumButton.rect.center, None, 'black',
                                  gameSquare.image.get_height() // 12)
      
      self.hardButton = Button((gameSquare.rect.centerx, buttonStart + 2 * buttonSpacing),
                               (gameSquare.image.get_width() / 4, gameSquare.image.get_height() / 8),
                               'red', 15)
      self.hardButton.mergeText('Hard', self.hardButton.rect.center, None, 'black',
                                gameSquare.image.get_height() // 12)
      
      self.descTitle = Text('Description',
                            (((gameSquare.rect.right - self.easyButton.rect.right) / 2) + self.easyButton.rect.right,
                             gameSquare.image.get_height() * (5 / 16) + gameSquare.rect.top), None,
                            'black', gameSquare.image.get_height() // 10)
      self.descBox = Square((self.descTitle.textRect.centerx,
                             5 * (gameSquare.image.get_height() / 8) + gameSquare.rect.top),
                            (gameSquare.image.get_width() * (1 / 4), gameSquare.image.get_height() / 2, 10),
                            'black')
      
      self.character = NotSquare('data/character.png',
                                 (((self.easyButton.rect.left - gameSquare.rect.left) / 2) + gameSquare.rect.left,
                                  gameSquare.rect.centery), 5, (250, 250))
      
      # TODO highlight method
      # TODO cooldown for buttons
    
    self.background.draw(self.display)
    self.display.blit(self.character.image, self.character.rect)
    self.descBox.draw(self.display)
    self.display.blit(self.title.text, self.title.textRect)
    self.display.blit(self.descTitle.text, self.descTitle.textRect)
    self.easyButton.draw(self.display)
    self.mediumButton.draw(self.display)
    self.hardButton.draw(self.display)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      self.gameStateManager.setState('main')
    elif self.easyButton.pressed:
      self.gameStateManager.setMode('easy')
      self.gameStateManager.setState('mode')


class Settings:
  def __init__(self, display, gameStateManager):
    self.display = display
    self.gameStateManager = gameStateManager
    self.start = True
  
  def run(self, gameSquare, reRender, key):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      self.background = gameSquare
      self.background.color = 'gray'
    
    self.background.draw(self.display)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      self.gameStateManager.setState('main')


game = Game()
game.run()
