from rgbmatrix import graphics
from src.renderers.renderer_utils import RendererUtils
import math
import random

# TODO: set as constant read from config files
NOTICE_COLOR_HEX       = 'fc7f03'
WARN_COLOR_HEX         = 'ed0e37'
GOOD_COLOR_HEX         = '26f50f'
ALMOST_THERE_COLOR_HEX = '05c3fc'

class GameSituationRenderer:

  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()
    # self.default_colors = self.data.config.team_colors.color("default")
    self.default_colors = {'r': 255, 'g': 255, 'b': 255} # just setting to white for now, used for text
    self.color_graphics = graphics.Color(self.default_colors['r'], self.default_colors['g'], self.default_colors['b'])

    ### TODO: going to change data here for testing purposes ###
    # down_list = ['1','2','3','4']
    # distance_list = ['5','8','12','20']
    # yard_line_list = ['30','10','60','90']
    # home_away_list = ['home','away']
    # self.game.down      = random.choice(down_list)
    # self.game.distance  = random.choice(distance_list)
    # self.game.yardLine  = random.choice(yard_line_list)
    # self.game.possession_home_or_away = random.choice(home_away_list)
    self.game.down = '2'
    self.game.distance = '4'
    self.game.yardLine = '32'
    self.game.possession_home_or_away = 'away'
    ######################################################

  def render(self):
    self.__render_downs()
    self.__render_field_position()

    return 1
  def __render_downs(self):
    down_px = []
    # TODO: add coords
    down_px.append(self.data.config.layout.coords("game_situation.downs.1"))
    down_px.append(self.data.config.layout.coords("game_situation.downs.2"))
    down_px.append(self.data.config.layout.coords("game_situation.downs.3"))
    down_px.append(self.data.config.layout.coords("game_situation.downs.4"))

    colors = []
    # TODO: add colors (or honestly just use whatever)
    # colors.append(self.data.config.colors.graphics_color("game_situation.downs.1"))
    # colors.append(self.data.config.colors.graphics_color("game_situation.downs.2"))
    # colors.append(self.data.config.colors.graphics_color("game_situation.downs.3"))
    # colors.append(self.data.config.colors.graphics_color("game_situation.downs.4"))

    # color_graphic = RendererUtils().convert_hex_to_color_graphic(self.game.home.team_color_prm)
    color_graphic = RendererUtils().convert_hex_to_color_graphic(NOTICE_COLOR_HEX)
 
    colors.append(color_graphic)
    colors.append(color_graphic)
    colors.append(color_graphic)
    colors.append(color_graphic)

    for down in range(len(down_px)):
      self.__render_down_square(down_px[down], colors[down])
      # Fill in the circle if that out has occurred
      if (int(self.game.down) > down):
        self.__fill_down_square(down_px[down], colors[down])

  def __render_down_square(self, down, color):
    x, y, size = (down["x"], down["y"], down["size"])
    graphics.DrawLine(self.canvas, x, y, x + size, y, color)
    graphics.DrawLine(self.canvas, x, y, x, y + size, color)
    graphics.DrawLine(self.canvas, x + size, y + size, x, y + size, color)
    graphics.DrawLine(self.canvas, x + size, y + size, x + size, y, color)

  def __fill_down_square(self, down, color):
    size = down["size"]
    x, y = (down["x"], down["y"])
    for y_offset in range(size):
      graphics.DrawLine(self.canvas, x, y + y_offset, x + size, y + y_offset, color)

  def __render_field_position(self):

    self.__render_territory()
    self.__render_position_stick()
    self.__render_distance()
    return 1

  def __render_territory(self):
    coords = self.data.config.layout.coords("game_situation.field_position.territory")
    coords['home']['x']
    coords['away']['y']
    colors = {
                # 'home': RendererUtils().convert_hex_to_color_graphic(self.game.home.team_color_prm),
                # 'away': RendererUtils().convert_hex_to_color_graphic(self.game.away.team_color_prm)
                'home': RendererUtils().convert_hex_to_color_graphic(NOTICE_COLOR_HEX),
                'away': RendererUtils().convert_hex_to_color_graphic(NOTICE_COLOR_HEX)
             }

    for homeaway in ['home', 'away']:
      x = coords[homeaway]['x']
      y = coords[homeaway]['y']
      width = coords[homeaway]['width']
      for y_offset in range(coords['away']['height']):
        graphics.DrawLine(self.canvas, x, y + y_offset, x + width, y + y_offset, colors[homeaway])

  def __render_position_stick(self):
    territory_coords    = self.data.config.layout.coords("game_situation.field_position.territory")
    yard_to_pixel_ratio = math.ceil( 100 / ( territory_coords['home']['width'] + territory_coords['away']['width'] ) )
    x_offset            = math.ceil( int(self.game.yardLine) / yard_to_pixel_ratio )
    # TODO: should change camel case to snake case for yardLine (and other keys), over at cfb.py

    coords = self.data.config.layout.coords("game_situation.field_position.position_stick")
    x      = coords['x']
    y      = coords['y']
    height = coords['height']
    colors = {
                # 'home': RendererUtils().convert_hex_to_color_graphic(self.game.home.team_color_prm),
                # 'away': RendererUtils().convert_hex_to_color_graphic(self.game.away.team_color_prm)
                'home': RendererUtils().convert_hex_to_color_graphic(NOTICE_COLOR_HEX),
                'away': RendererUtils().convert_hex_to_color_graphic(NOTICE_COLOR_HEX)
             }
    color  = colors[self.game.possession_home_or_away]

    graphics.DrawLine(self.canvas, x + x_offset, y, x + x_offset, y - height, color)

  def __render_distance(self):
    # TODO: being used in multiple functions, so best to evaluation beforehand
    territory_coords    = self.data.config.layout.coords("game_situation.field_position.territory")
    yard_to_pixel_ratio = math.ceil( 100 / ( territory_coords['home']['width'] + territory_coords['away']['width'] ) )
    x_offset            = math.ceil( int(self.game.yardLine) / yard_to_pixel_ratio )
    ######

    distance = math.ceil( int(self.game.distance) / yard_to_pixel_ratio )
    if self.game.possession_home_or_away == 'away':
      distance *= -1

    if int(self.game.distance) <= 10:
      distance_color_hex = GOOD_COLOR_HEX
      if int(self.game.distance) <= 5:
        distance_color_hex = ALMOST_THERE_COLOR_HEX
    else:
      distance_color_hex = WARN_COLOR_HEX

    color = RendererUtils().convert_hex_to_color_graphic(distance_color_hex)


    coords = self.data.config.layout.coords("game_situation.field_position.distance")
    x      = coords['x']
    y      = coords['y']


    graphics.DrawLine(self.canvas, x + x_offset, y, x + x_offset + distance, y, color)
