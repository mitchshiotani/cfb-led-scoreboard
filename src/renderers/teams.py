from rgbmatrix import graphics
from utils import get_font, get_file
import json
import pprint

class TeamsRenderer:
  """Renders the scoreboard team banners including background color, team abbreviation text,
  and their scored runs."""

  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()
    # self.default_colors = self.data.config.team_colors.color("default")
    self.default_colors = {'r': 255, 'g': 255, 'b': 255} # just setting to white for now, used for text

  # def __team_colors(self, team_abbrev):
  #   try:
  #     team_colors = self.data.config.team_colors.color(team_abbrev.lower())
  #   except KeyError as e:
  #     team_colors = self.data.config.team_colors.color("default")
  #   return team_colors

  # def __default_home_color(self):
  #   return self.data.config.team_colors.color("default.home")
  
  # def __default_accent_color(self):
  #   return self.data.config.team_colors.color("default.accent")

  def render(self):
    # colors
    away_team_color = self.game.away.team_color_prm
    home_team_color = self.game.home.team_color_prm
    # away_colors = self.__team_colors(self.away_team.abbrev)
    # try:
    #   away_team_color = away_colors['home']
    # except KeyError as e:
    #   away_team_color = self.__default_home_color()
      
    # home_colors = self.__team_colors(self.home_team.abbrev)
    # try:
    #   home_team_color = home_colors['home']
    # except KeyError as e:
    #   home_team_color = self.__default_home_color()
      
    # accents (?)
    # for now, just going to make it the same as the team colors
    away_team_color = self.__convert_hex_to_rgb(self.game.away.team_color_prm)
    home_team_color = self.__convert_hex_to_rgb(self.game.home.team_color_prm)

    # away_accents = self.__team_colors(self.away_team.abbrev)
    # try:
    #   away_team_accent = away_accents['accent']
    # except KeyError as e:
    #   away_team_accent = self.__default_accent_color()
      
    # home_accents = self.__team_colors(self.home_team.abbrev)
    # try:
    #   home_team_accent = home_accents['accent']
    # except KeyError as e:
    #   home_team_accent = self.__default_accent_color()

    # coordinates
    bg_coords = {}
    bg_coords["away"] = self.data.config.layout.coords("teams.background.away")
    bg_coords["home"] = self.data.config.layout.coords("teams.background.home")
    
    accent_coords = {}
    accent_coords["away"] = self.data.config.layout.coords("teams.accent.away")
    accent_coords["home"] = self.data.config.layout.coords("teams.accent.home")

    away_name_coords = self.data.config.layout.coords("teams.name.away")
    home_name_coords = self.data.config.layout.coords("teams.name.home")

    away_score_coords = self.data.config.layout.coords("teams.scores.away")
    home_score_coords = self.data.config.layout.coords("teams.scores.home")

    # drawing/filling the boxes under team names

    # for team in ["away","home"]:
    #   for x in range(bg_coords[team]["width"]):
    #     for y in range(bg_coords[team]["height"]):
    #       color = away_team_color if team == "away" else home_team_color
    #       x_offset = bg_coords[team]["x"]
    #       y_offset = bg_coords[team]["y"]
    #       self.canvas.SetPixel(x + x_offset, y + y_offset, color['r'], color['g'], color['b'])

    # still dk what this is

    # for team in ["away","home"]:
    #   for x in range(accent_coords[team]["width"]):
    #     for y in range(accent_coords[team]["height"]):
    #       # color = away_team_accent if team == "away" else home_team_accent
    #       color = away_team_color if team == "away" else home_team_color # same as color for now
    #       x_offset = accent_coords[team]["x"]
    #       y_offset = accent_coords[team]["y"]
    #       self.canvas.SetPixel(x + x_offset, y + y_offset, color['r'], color['g'], color['b'])
          
    # render text and score
    # self.__render_team_text(self.game.away, "away", away_colors, away_name_coords["x"], away_name_coords["y"])
    # self.__render_team_text(self.game.home, "home", home_colors, home_name_coords["x"], home_name_coords["y"])
    # self.__render_team_score(self.game.away.score, "away", away_colors, away_score_coords["x"], away_score_coords["y"])
    # self.__render_team_score(self.game.home.score, "home", home_colors, home_score_coords["x"], home_score_coords["y"])

    self.__render_team_text(self.game.away, "away", away_team_color, away_name_coords["x"], away_name_coords["y"])
    self.__render_team_text(self.game.home, "home", home_team_color, home_name_coords["x"], home_name_coords["y"])
    self.__render_team_score(self.game.away.team_score, "away", away_team_color, away_score_coords["x"], away_score_coords["y"])
    self.__render_team_score(self.game.home.team_score, "home", home_team_color, home_score_coords["x"], home_score_coords["y"])

  # def __render_team_text(self, team, homeaway, colors, x, y):
  def __render_team_text(self, team, homeaway, color, x, y):
    # text_color = colors.get('text', self.default_colors['text'])
    text_color = color
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    # text_color_graphic = graphics.Color(255,255,255)
    font = self.data.config.layout.font("teams.name.{}".format(homeaway))
    team_text = team.team_name_abv.upper()[:4]

    if self.data.config.full_team_names and self.canvas.width > 32:
      team_text = team.team_location[:11]
      # team_text = '{:13s}'.format(team.team_location)

      # print "team_text:"
      # print team_text
    # print "x:"
    # print x
    # print "y:"
    # print y
    # print "font:"
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(font)
    # pp.pprint(font["font"])
    # font["font"] = self.layout.font("offday.time")
    graphics.DrawText(self.canvas, font["font"], x, y, text_color_graphic, team_text)

  # def __render_team_score(self, score, homeaway, colors, x, y):
  def __render_team_score(self, score, homeaway, color, x, y):
    # text_color = colors.get('text', self.default_colors['text'])
    text_color = color
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    coords = self.data.config.layout.coords("teams.scores.{}".format(homeaway))
    font = self.data.config.layout.font("teams.scores.{}".format(homeaway))
    team_score = str(score)
    team_score_x = coords["x"] - (len(team_score) * font["size"]["width"])
    graphics.DrawText(self.canvas, font["font"], team_score_x, y, text_color_graphic, team_score)

  def __convert_hex_to_rgb(self, hex_str):
    # convert hex to rgb, to put into graphics.Color()
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return {'r': r, 'g': g, 'b': b}
