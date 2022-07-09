from src.renderers.teams import TeamsRenderer
from src.renderers.timekeeper import TimekeeperRenderer
# have to replace above with the football equivalents

class Scoreboard:
  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data

  def render(self):
    TeamsRenderer(self.canvas, self.data).render()
    TimekeeperRenderer(self.canvas, self.data).render()
    # NetworkErrorRenderer(self.canvas, self.data).render()
