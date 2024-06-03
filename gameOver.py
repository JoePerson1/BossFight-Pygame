from sprites import *

class GameOver:
  def __init__(self, display, gameStateManager):
    self.display = display
    self.gameStateManager = gameStateManager
    self.start = True
  def run(self, gameSquare, reRender, keyPresses):
    if self.start:
      reRender = True
      self.start = False
    if reRender:
      self.background = Square(gameSquare.rect.center, (gameSquare.image.get_width() / 2,
                                  gameSquare.image.get_height() / 2), (255, 0, 0, 255), 30)
    self.background.drawRect(self.display)
    