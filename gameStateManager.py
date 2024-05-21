class GameStateManager:
  def __init__(self, currentState):
    self.mode = None
    self.currentState = currentState
  
  def getState(self):
    return self.currentState
  
  def setState(self, state):
    self.currentState = state
  
  def setMode(self, mode):
    self.mode = mode
  
  def getMode(self):
    return self.mode
  