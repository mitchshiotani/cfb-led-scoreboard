from rgbmatrix import graphics
from src.renderers.renderer_utils import RendererUtils

class TeamsRenderer:
  """Renders the scoreboard team banners including background color, team abbreviation text,
  and their scored runs."""

  def __init__(self, canvas, data):
    self.canvas = canvas
    self.data = data
    self.game = self.data.current_game()

  def render(self):
    # colors
      
    # accents (?)
    # for now, just going to make it the same as the team colors
    away_team_color = self.__convert_hex_to_rgb(self.game.away.team_color_prm)
    home_team_color = self.__convert_hex_to_rgb(self.game.home.team_color_prm)

    away_team_accent = self.__convert_hex_to_rgb(self.game.away.team_color_alt)
    home_team_accent = self.__convert_hex_to_rgb(self.game.home.team_color_alt)

    # coordinates
    bg_coords = {}
    bg_coords["away"] = self.data.config.layout.coords("teams.background.away")
    bg_coords["home"] = self.data.config.layout.coords("teams.background.home")
    
    accent_coords = {}
    accent_coords["away"] = self.data.config.layout.coords("teams.accent.away")
    accent_coords["home"] = self.data.config.layout.coords("teams.accent.home")

    away_ranking_coords = self.data.config.layout.coords("teams.ranking.away")
    home_ranking_coords = self.data.config.layout.coords("teams.ranking.home")

    away_name_coords = self.data.config.layout.coords("teams.name.away")
    home_name_coords = self.data.config.layout.coords("teams.name.home")

    away_score_coords = self.data.config.layout.coords("teams.scores.away")
    home_score_coords = self.data.config.layout.coords("teams.scores.home")

    # drawing/filling the boxes under team names

    for team in ["away","home"]:
      for x in range(bg_coords[team]["width"]):
        for y in range(bg_coords[team]["height"]):
          # color = away_team_accent if team == "away" else home_team_accent
          color = away_team_color if team == "away" else home_team_color
          x_offset = bg_coords[team]["x"]
          y_offset = bg_coords[team]["y"]
          self.canvas.SetPixel(x + x_offset, y + y_offset, color['r'], color['g'], color['b'])

    # XXX: this should really be done in cfb.py, to make team_ranking null if it's 99 in the ESPN API
    if self.game.away.team_ranking and self.game.away.team_ranking != 99:
        self.__render_team_ranking(self.game.away, "away", away_team_color, away_team_accent, away_ranking_coords["x"], away_ranking_coords["y"])

    # XXX: this should really be done in cfb.py, to make team_ranking null if it's 99 in the ESPN API
    if self.game.home.team_ranking and self.game.home.team_ranking != 99:
        self.__render_team_ranking(self.game.home, "home", home_team_color, home_team_accent, home_ranking_coords["x"], home_ranking_coords["y"])

    self.__render_team_text(self.game.away, "away", away_team_accent, away_name_coords["x"], away_name_coords["y"])
    self.__render_team_text(self.game.home, "home", home_team_accent, home_name_coords["x"], home_name_coords["y"])

    if self.game.status == 'STATUS_IN_PROGRESS':
        self.__render_team_score(self.game.away.team_score, "away", away_team_accent, away_score_coords["x"], away_score_coords["y"])
        self.__render_team_score(self.game.home.team_score, "home", home_team_accent, home_score_coords["x"], home_score_coords["y"])
        self.__render_possession()

  def __render_team_ranking(self, team, homeaway, color, accent, ranking_x, ranking_y):
    team_bg_coords = self.data.config.layout.coords("teams.ranking.background.{}".format(homeaway))
    # draw squares
    for x in range(team_bg_coords["width"]):
      for y in range(team_bg_coords["height"]):
        # color = away_team_accent if team == "away" else home_team_accent
        x_offset = team_bg_coords["x"]
        y_offset = team_bg_coords["y"]
        self.canvas.SetPixel(x + x_offset, y + y_offset, accent['r'], accent['g'], accent['b'])

    # draw ranking
    text_color = color
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    # text_color_graphic = graphics.Color(255,255,255)
    font = self.data.config.layout.font("teams.ranking.{}".format(homeaway))
    ranking = str(team.team_ranking)

    # graphics.DrawText(self.canvas, font["font"], x, y, text_color_graphic, ranking)
    graphics.DrawText(self.canvas, font["font"], ranking_x, ranking_y, text_color_graphic, ranking)

  def __render_team_text(self, team, homeaway, color, x, y):
    text_color = color
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    # text_color_graphic = graphics.Color(255,255,255)
    font = self.data.config.layout.font("teams.name.{}".format(homeaway))
    team_text = team.team_name_abv.upper()[:4]

    if self.data.config.full_team_names and self.canvas.width > 32:
      team_text = team.team_location[:9]

    graphics.DrawText(self.canvas, font["font"], x, y, text_color_graphic, team_text)

  # def __render_team_score(self, score, homeaway, colors, x, y):
  def __render_team_score(self, score, homeaway, color, x, y):
    text_color = color
    text_color_graphic = graphics.Color(text_color['r'], text_color['g'], text_color['b'])
    coords = self.data.config.layout.coords("teams.scores.{}".format(homeaway))
    font = self.data.config.layout.font("teams.scores.{}".format(homeaway))
    team_score = str(score)
    team_score_x = coords["x"] - (len(team_score) * font["size"]["width"])
    graphics.DrawText(self.canvas, font["font"], team_score_x, y, text_color_graphic, team_score)

  def __render_possession(self):
    # find out who has possession
    homeaway = self.game.possession_home_or_away
    coords = self.data.config.layout.coords("teams.possession.{}".format(homeaway))
    team_w_possession = getattr(self.game, homeaway)
    color = RendererUtils().convert_hex_to_color_graphic(team_w_possession.team_color_alt)

    x = coords['x']
    y = coords['y']
    width = coords['width']
    height = coords['height']
    for x_offset in range(width):
      graphics.DrawLine(self.canvas, x - x_offset, y + x_offset, x - x_offset, y + height - x_offset, color)
    
  def __convert_hex_to_rgb(self, hex_str):
    # convert hex to rgb, to put into graphics.Color()
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return {'r': r, 'g': g, 'b': b}
