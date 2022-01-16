from src.renderers.teams import TeamsRenderer
# have to replace above with the football equivalents

class Scoreboard:
  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data

  def render(self):
    TeamsRenderer(self.canvas, self.data).render()
    # NetworkErrorRenderer(self.canvas, self.data).render()
