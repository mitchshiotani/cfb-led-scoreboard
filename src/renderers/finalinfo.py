from rgbmatrix import graphics

class FinalInfoRenderer:
  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()
    # self.default_colors = self.data.config.team_colors.color("default")
    self.default_colors = {'r': 255, 'g': 255, 'b': 255} # just setting to white for now, used for text
    self.color_graphics = graphics.Color(self.default_colors['r'], self.default_colors['g'], self.default_colors['b'])

  def render(self):
    coords = self.data.config.layout.coords("final")
    font = self.data.config.layout.font("teams.scores.home") # TODO:honestly have no idea how the fonts are being pulled. should figure it out.
    graphics.DrawText(self.canvas, font['font'], coords['x'], coords['y'], self.color_graphics, 'FINAL')
