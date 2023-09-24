from src.infra.rgb_matrix_wrapper import graphics
from src.renderers.renderer_utils import RendererUtils

# TODO: set as constant read from config files
GOOD_COLOR_HEX = '26f50f'
DEFAULT_COLOR_HEX = 'ffffff'

class TimekeeperRenderer:

  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()
    # self.default_colors = self.data.config.team_colors.color("default")
    self.default_colors = {'r': 255, 'g': 255, 'b': 255} # just setting to white for now, used for text
    self.color_graphics = graphics.Color(self.default_colors['r'], self.default_colors['g'], self.default_colors['b'])

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

    color = RendererUtils().convert_hex_to_color_graphic(DEFAULT_COLOR_HEX)

    if __is_good_game(self.game):
        color = RendererUtils().convert_hex_to_color_graphic(GOOD_COLOR_HEX)

    graphics.DrawText(self.canvas, font['font'], coords['x'], coords['y'], color, padded_text)
    return 1

# TODO: this probably shouldn't be here, but oh well
def __is_good_game(game):
  if game.period >= 3 and abs(game.away.team_score - game.home.team_score) <= 7:
      return True
  return False
