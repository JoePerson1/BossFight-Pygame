import pygame

def toCharacterVector(characterPos, followerPos):
  characterVector = pygame.math.Vector2(characterPos)
  followerVector = pygame.math.Vector2(followerPos)
  try:
    directionVector = pygame.math.Vector2.normalize(characterVector - followerVector)
  except ValueError:
    return pygame.math.Vector2((0, 0))
  return directionVector
