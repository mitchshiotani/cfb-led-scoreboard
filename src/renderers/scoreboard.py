from src.renderers.teams import TeamsRenderer
from src.renderers.timekeeper import TimekeeperRenderer
from src.renderers.pregameinfo import PregameInfoRenderer
from src.renderers.finalinfo import FinalInfoRenderer
from src.renderers.game_situation import GameSituationRenderer
# have to replace above with the football equivalents

class Scoreboard:
  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()

  def render(self):
    TeamsRenderer(self.canvas, self.data).render()
    if self.game.status == 'STATUS_IN_PROGRESS':
      TimekeeperRenderer(self.canvas, self.data).render()
      GameSituationRenderer(self.canvas, self.data).render()
    if self.game.status == 'STATUS_SCHEDULED':
      # PregameInfoRenderer(self.canvas, self.data).render()
      TimekeeperRenderer(self.canvas, self.data).render()
      GameSituationRenderer(self.canvas, self.data).render()
    if self.game.status == 'STATUS_FINAL':
      FinalInfoRenderer(self.canvas, self.data).render()
    # NetworkErrorRenderer(self.canvas, self.data).render()
