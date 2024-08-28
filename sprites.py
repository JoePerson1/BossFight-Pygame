import pygame  # TODO hitboxes different than sprite

class NotSquare(pygame.sprite.Sprite):
  def __init__(self, picture, pos, scale):   # TODO make scale normal but still stretchable
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(picture).convert_alpha()
    self.image = pygame.transform.scale(self.image, scale)
    self.rect = self.image.get_rect()  # TODO self.image.rect
    self.rect.center = (pos[0], pos[1])
    self.decimal = pygame.math.Vector2([self.rect.centerx,
                                        self.rect.centery])

class Square(pygame.sprite.Sprite):
  def __init__(self, pos, size, squareColor=None, radius=0):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((size[0], size[1]))
    self.rect = self.image.get_rect()
    self.rect.center = (pos[0], pos[1])
    self.borderRadius = radius
    if squareColor is not None:
      self.color = squareColor
      self.image.fill(squareColor)
  def drawRect(self, screen):
    pygame.draw.rect(screen, self.color, self.rect, border_radius=self.borderRadius)

class Text:
  def __init__(self, text, pos, font, color, size):  # TODO fix bold/italics
    textFont = pygame.font.Font(font, size)
    self.text = textFont.render(text, True, color)
    self.textRect = self.text.get_rect(center=(pos[0], pos[1]))
    
class Button(Square, Text, NotSquare):
  # TODO do i even need this class? since im spriting all, cant i just add checkclick to notSquare?
  def __init__(self, pos, size, squareColor=None, radius=0):
    Square.__init__(self, pos, size, squareColor, radius)
    self.pressed = False
  def mergeText(self, text, pos, font, color, size):
    Text.__init__(self, text, pos, font, color, size)
  def mergeImage(self, picture, pos, scale):
    NotSquare.__init__(self, picture, pos, scale)
  def drawRect(self, screen):  # TODO do something about this
    pygame.draw.rect(screen, self.color, self.rect, border_radius=self.borderRadius)
  def drawText(self, screen):
    screen.blit(self.text, self.textRect)
  def drawImage(self, screen):
    screen.blit(self.image, self.rect)
  def checkClick(self):  # TODO button activate if mouse clicked and released on it
    mousePos = pygame.mouse.get_pos()
    if self.rect.collidepoint(mousePos):
      if pygame.mouse.get_pressed()[0]:
        self.pressed = True
      elif self.pressed:
        self.pressed = False
  def highlight(self):
    pass
  
# TODO add reAdjust method for resizing during fight
