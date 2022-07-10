from rgbmatrix import graphics
from src.renderers.renderer_utils import RendererUtils
import math

class GameSituationRenderer:

  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()
    # self.default_colors = self.data.config.team_colors.color("default")
    self.default_colors = {'r': 255, 'g': 255, 'b': 255} # just setting to white for now, used for text
    self.color_graphics = graphics.Color(self.default_colors['r'], self.default_colors['g'], self.default_colors['b'])

    ### TODO: going to change data here for testing purposes ###
    self.game.down = '2'
    self.game.distance = '20'
    self.game.yardLine = '32'
    self.game.possession_home_or_away = 'away'
    ######################################################

  def render(self):
    self.__render_downs()
    self.__render_field_position()

  def __render_downs(self):
    down_px = []
    # TODO: add coords
    down_px.append(self.data.config.layout.coords("game_situation.downs.1"))
    down_px.append(self.data.config.layout.coords("game_situation.downs.2"))
    down_px.append(self.data.config.layout.coords("game_situation.downs.3"))
    down_px.append(self.data.config.layout.coords("game_situation.downs.4"))

    colors = []
    # TODO: add colors (or honestly just use whatever)
    colors.append(self.data.config.colors.graphics_color("game_situation.downs.1"))
    colors.append(self.data.config.colors.graphics_color("game_situation.downs.2"))
    colors.append(self.data.config.colors.graphics_color("game_situation.downs.3"))
    colors.append(self.data.config.colors.graphics_color("game_situation.downs.4"))
    
    for down in range(len(down_px)):
      self.__render_down_square(down_px[down], colors[down])
      # Fill in the circle if that out has occurred
      if (self.game.down > down):
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
                'home': RendererUtils().convert_hex_to_rgb(self.game.home.team_color_prm),
                'away': RendererUtils().convert_hex_to_rgb(self.game.away.team_color_prm)
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
    x_offset            = math.ceil( self.game.yardLine / yard_to_pixel_ratio )
    # TODO: should change camel case to snake case for yardLine (and other keys), over at cfb.py

    coords = self.data.config.layout.coords("game_situation.field_position.position_stick")
    x      = coords['x']
    y      = coords['y']
    height = coords['height']
    colors = {
                'home': RendererUtils().convert_hex_to_rgb(self.game.home.team_color_prm),
                'away': RendererUtils().convert_hex_to_rgb(self.game.away.team_color_prm)
             }
    color  = colors[self.game.possession_home_or_away]

    graphics.DrawLine(self.canvas, x + x_offset, y, x + x_offset, y - height, color)

  def __render_distance(self):
    # TODO: being used in multiple functions, so best to evaluation beforehand
    territory_coords    = self.data.config.layout.coords("game_situation.field_position.territory")
    yard_to_pixel_ratio = math.ceil( 100 / ( territory_coords['home']['width'] + territory_coords['away']['width'] ) )
    x_offset            = math.ceil( self.game.yardLine / yard_to_pixel_ratio )
    ######
    distance = self.game.distance
    if self.game.possession_home_or_away == 'away':
      distance *= -1

    coords = self.data.config.layout.coords("game_situation.field_position.position_stick")
    x      = coords['x']
    y      = coords['y']
    colors = {
                'home': RendererUtils().convert_hex_to_rgb(self.game.home.team_color_prm),
                'away': RendererUtils().convert_hex_to_rgb(self.game.away.team_color_prm)
             }
    color  = colors[self.game.possession_home_or_away]

    graphics.DrawLine(self.canvas, x + x_offset, y, x + x_offset + distance, y, color)
