from rgbmatrix import graphics

class TimekeeperRenderer:

  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()
    # self.default_colors = self.data.config.team_colors.color("default")
    self.default_colors = {'r': 255, 'g': 255, 'b': 255} # just setting to white for now, used for text
    self.color_graphics = graphics.Color(self.default_colors['r'], self.default_colors['g'], self.default_colors['b'])

    ### TODO: going to change data here for testing purposes ###
    self.game.shortDetail = '1:23 - 4th'
    self.game.down_and_distance = '2nd & 20'
    self.game.field_position = 'PIT 32'
    ######################################################

  def render(self):
    self.__render_game_time_text()

  def __render_game_time_text(self):
    # get coords from config
    coords = self.data.config.layout.coords("time")
    font = self.data.config.layout.font("teams.scores.home") # TODO:honestly have no idea how the fonts are being pulled. should figure it out.
    # get data from data object
    text = "{} P{}".format(self.game.time, self.game.period)
    text = "2:34 P4"
    padded_text = text.zfill(8)
    graphics.DrawText(self.canvas, font['font'], coords['x'], coords['y'], self.color_graphics, padded_text)
    return 1
