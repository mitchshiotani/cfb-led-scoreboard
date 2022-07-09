from rgbmatrix import graphics

class TimekeeperRenderer:
  """Renders the scoreboard team banners including background color, team abbreviation text,
  and their scored runs."""

  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()
    # self.default_colors = self.data.config.team_colors.color("default")
    self.default_colors = {'r': 255, 'g': 255, 'b': 255} # just setting to white for now, used for text
    self.color_graphics = graphics.Color(self.default_colors['r'], self.default_colors['g'], self.default_colors['b'])

    ### TODO: going to change data here for testing purposes ###
    self.game.time_and_period = '1:23 - 4th'
    self.game.down_and_distance = '2nd & 20'
    self.game.field_position = 'PIT 32'
    ######################################################

  def render(self):
    self.__render_game_time_text()
    self.__render_downs_and_field_position_text()

  def __render_game_time_text(self):
    # get coords from config
    coords = self.data.config.layout.coords("time")
    font = self.data.config.layout.font("teams.scores.home") # TODO:honestly have no idea how the fonts are being pulled. should figure it out.
    # get data from data object
    graphics.DrawText(self.canvas, font['font'], coords['x'], coords['y'], self.color_graphics, self.game.time_and_period)
    return 1

  def __render_downs_and_field_position_text(self):
    coords = self.data.config.layout.coords("downs")
    font = self.data.config.layout.font("teams.scores.home") # TODO:honestly have no idea how the fonts are being pulled. should figure it out.
    text = "{}, {}".format(self.game.down_and_distance, self.game.field_position)
    graphics.DrawText(self.canvas, font['font'], coords['x'], coords['y'], self.color_graphics, text)
    return 1
