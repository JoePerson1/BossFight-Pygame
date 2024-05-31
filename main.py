import sys
import time
# TODO import pygame GUI and other pygame libraries?
# https://www.reddit.com/r/pygame/comments/89ygm7/pygame_awesome_libraries/

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
  
  def run(self):
    while True:
      self.keyPresses = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False,
                         pygame.K_SPACE: False}
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
        
        if event.type == pygame.KEYDOWN:  # TODO make keys scalable
          if event.key in self.keyPresses:
            singleKey = event.key
            self.keyPresses[singleKey] = True
      
      # print(self.keyPresses)  # TODO DECIDE WHETHER TO PUT DOUBLE CLICK DETECTION HERE OR CHARACTER CLASS
      # print(list(self.keyPresses.values()))

      self.states[self.gameStateManager.getState()].run(self.gameSquare, self.reRender, self.keyPresses)
      self.reRender = False
      
      pygame.display.update()
      self.clock.tick(FPS)
      # TODO fps counter

class MainMenu:
  def __init__(self, display, gameStateManager):
    self.display = display
    self.gameStateManager = gameStateManager
    self.start = True
  
  def run(self, gameSquare, reRender, keyPresses):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      self.background = NotSquare('assets/backgrounds/main_menu_background.png',
                                  ((gameSquare.rect.right + gameSquare.rect.left) / 2,
                                   (gameSquare.rect.top + gameSquare.rect.bottom) / 2,),
                                  (gameSquare.image.get_width(), gameSquare.image.get_width() / 1920 * 1076))
      
      self.title = Text('Assignment Four', (gameSquare.rect.centerx,
                                            gameSquare.image.get_height() * (3 / 16) + gameSquare.rect.top),
                        'assets/fonts/pressStart.ttf', 'black',
                        gameSquare.image.get_height() // 12)
      
      buttonStart = gameSquare.image.get_height() * (2 / 5) + gameSquare.rect.top
      buttonSpacing = gameSquare.image.get_height() * (1 / 5)
      
      self.playButton = Button((gameSquare.rect.centerx, buttonStart), (gameSquare.image.get_width() / 3,
                                  gameSquare.image.get_height() / 8), 'dark green',
                               30)
      self.playButton.mergeText('Play', self.playButton.rect.center, 'assets/fonts/pressStart.ttf',
                                'white', gameSquare.image.get_height() // 20)
      self.settingsButton = Button((gameSquare.rect.centerx, buttonStart + buttonSpacing),
                                   (gameSquare.image.get_width() / 3, gameSquare.image.get_height() / 8),
                                   'dark green', 30)
      self.settingsButton.mergeText('Settings', self.settingsButton.rect.center, 'assets/fonts/pressStart.ttf',
                                    'white', gameSquare.image.get_height() // 20)
      self.quitButton = Button((gameSquare.rect.centerx, buttonStart + 2 * buttonSpacing),
                               (gameSquare.image.get_width() / 3, gameSquare.image.get_height() / 8),
                               'dark green', 30)
      self.quitButton.mergeText('Quit', self.quitButton.rect.center, 'assets/fonts/pressStart.ttf',
                                'white', gameSquare.image.get_height() // 20)
    
    self.display.blit(self.background.image, self.background.rect)
    self.display.blit(self.title.text, self.title.textRect)  # TODO optimize???
    
    self.buttonAssets = [self.playButton, self.settingsButton, self.quitButton]
    for asset in self.buttonAssets:
      asset.drawRect(self.display)
      asset.drawText(self.display)
      asset.checkClick()
    
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
  
  def run(self, gameSquare, reRender, keyPresses):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      self.background = NotSquare('assets/backgrounds/main_menu_background.png',
                                  ((gameSquare.rect.right + gameSquare.rect.left) / 2,
                                   (gameSquare.rect.top + gameSquare.rect.bottom) / 2,),
                                  (gameSquare.image.get_width(), gameSquare.image.get_width() / 1920 * 1076))
      
      buttonStart = gameSquare.image.get_height() * (2 / 5) + gameSquare.rect.top
      buttonSpacing = gameSquare.image.get_height() * (1 / 5)
      
      self.title = Text('Select Your Difficulty', (gameSquare.rect.centerx,
                                                   gameSquare.image.get_height() * (1 / 8) + gameSquare.rect.top),
                        None, 'black', gameSquare.image.get_height() // 5)
      self.easyButton = Button((gameSquare.rect.centerx, buttonStart), (gameSquare.image.get_width() / 4,
                                                                        gameSquare.image.get_height() / 8),
                               'green', 15)
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
      
      self.character = NotSquare('assets/character.png',
                                 (((self.easyButton.rect.left - gameSquare.rect.left) / 2) + gameSquare.rect.left,
                                  gameSquare.rect.centery), (250, 250))
      
      # TODO highlight method
      # TODO cooldown for buttons
    
    self.display.blit(self.background.image, self.background.rect)
    self.display.blit(self.character.image, self.character.rect)
    self.descBox.drawRect(self.display)
    self.display.blit(self.title.text, self.title.textRect)
    self.display.blit(self.descTitle.text, self.descTitle.textRect)
    
    self.buttonAssets = [self.easyButton, self.mediumButton, self.hardButton]
    for asset in self.buttonAssets:
      asset.drawRect(self.display)
      asset.drawText(self.display)
      asset.checkClick()
    
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
  
  def run(self, gameSquare, reRender, keyPresses):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      self.background = NotSquare('assets/backgrounds/main_menu_background.png',
                                  ((gameSquare.rect.right + gameSquare.rect.left) / 2,
                                   (gameSquare.rect.top + gameSquare.rect.bottom) / 2,),
                                  (gameSquare.image.get_width(), gameSquare.image.get_width() / 1920 * 1076))
      self.backButton = Button((7 * gameSquare.image.get_width() / 8, 1 * gameSquare.image.get_height() / 16),
                               (50, 50), 'black')
      self.backButton.mergeImage('assets/placeholder.png', self.backButton.rect.center, (50, 50))
      
    self.display.blit(self.background.image, self.background.rect)
    self.backButton.drawImage(self.display)
    self.backButton.checkClick()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      self.gameStateManager.setState('main')
    elif self.backButton.pressed:
      self.gameStateManager.setState('main')

game = Game()
game.run()
