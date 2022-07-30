from time import time
from rgbmatrix import graphics
from datetime import datetime, timedelta

class PregameInfoRenderer:
  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()
    # self.default_colors = self.data.config.team_colors.color("default")
    self.default_colors = {'r': 255, 'g': 255, 'b': 255} # just setting to white for now, used for text
    self.color_graphics = graphics.Color(self.default_colors['r'], self.default_colors['g'], self.default_colors['b'])

  def render(self):
    self.__render_gametime()
    self.__render_broadcast_info()

  def __render_gametime(self):
    start_time_changed = datetime.strptime(self.game.start_time, '%Y-%m-%dT%H:%MZ') + timedelta(hours=self.data.config.utc_difference)
    start_time_text = start_time_changed.strftime("%m/%d %H:%M")
    # start_time_text = datetime.strptime(self.game.start_time, '%Y-%m-%dT%H:%MZ').strftime("%m/%d %H:%M")
    # TODO: need to make this show in local time, but I'll have to figure out how to do that
    coords = self.data.config.layout.coords("pre_game_info.gametime")
    font = self.data.config.layout.font("teams.scores.home") # TODO:honestly have no idea how the fonts are being pulled. should figure it out.
    graphics.DrawText(self.canvas, font['font'], coords['x'], coords['y'], self.color_graphics, start_time_text)

  def __render_broadcast_info(self):
    coords = self.data.config.layout.coords("pre_game_info.broadcast_info")
    font = self.data.config.layout.font("teams.scores.home") # TODO:honestly have no idea how the fonts are being pulled. should figure it out.
    graphics.DrawText(self.canvas, font['font'], coords['x'], coords['y'], self.color_graphics, self.game.broadcast)
