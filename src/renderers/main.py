# from src.data.final import Final
# from src.data.pregame import Pregame
# from src.data.scoreboard import Scoreboard
# from src.data.status import Status
# from src.renderers.final import Final as FinalRenderer
# from src.renderers.pregame import Pregame as PregameRenderer
from src.renderers.scoreboard import Scoreboard as ScoreboardRenderer
# from src.renderers.status import StatusRenderer
# from src.renderers.standings import StandingsRenderer
# from src.renderers.offday import OffdayRenderer
# from src.data.data import Data
import debug
import time

GAMES_REFRESH_RATE = 900.0
SCROLL_TEXT_FAST_RATE = 0.1
SCROLL_TEXT_SLOW_RATE = 0.2

class MainRenderer:
  def __init__(self, matrix, data):
    self.matrix = matrix
    self.data = data
    self.canvas = matrix.CreateFrameCanvas()
    self.scrolling_text_pos = self.canvas.width
    self.starttime = time.time()

  def render(self):
    self.starttime = time.time()
    self.__render_game()

  def __render_game(self):
    while True:
      self.__draw_game()

      endtime = time.time()
      time_delta = endtime - self.starttime
      rotate_rate = 5 # TODO: need to make this a constant/ configurable

      # If we're ready to rotate, let's do it
      if time_delta >= rotate_rate:
        self.starttime = time.time()
        # self.data.needs_refresh = True
        game = self.data.advance_to_next_game()

  # Draws the provided game on the canvas
  def __draw_game(self):
    game = self.data.current_game()
    # overview = self.data.overview # I don't think I need this
    color = self.data.config.scoreboard_colors.color("default.background")
    self.canvas.Fill(color["r"], color["g"], color["b"])

    # # Draw the pregame renderer
    # if Status.is_pregame(overview.status):
    #   scoreboard = Scoreboard(overview)
    #   scroll_max_x = self.__max_scroll_x(self.data.config.layout.coords("pregame.scrolling_text"))
    #   pregame = Pregame(overview, self.data.config.time_format)
    #   renderer = PregameRenderer(self.canvas, pregame, scoreboard, self.data, self.scrolling_text_pos)
    #   self.__update_scrolling_text_pos(renderer.render())

    # # Draw the final game renderer
    # elif Status.is_complete(overview.status):
    #   scroll_max_x = self.__max_scroll_x(self.data.config.layout.coords("final.scrolling_text"))
    #   final = Final(game)
    #   scoreboard = Scoreboard(overview)
    #   renderer = FinalRenderer(self.canvas, final, scoreboard, self.data, self.scrolling_text_pos)
    #   self.__update_scrolling_text_pos(renderer.render())

    # # Draw the scoreboar renderer
    # elif Status.is_irregular(overview.status):
    #   scoreboard = Scoreboard(overview)
    #   if scoreboard.get_text_for_reason():
    #     scroll_max_x = self.__max_scroll_x(self.data.config.layout.coords("status.scrolling_text"))
    #     renderer = StatusRenderer(self.canvas, scoreboard, self.data, self.scrolling_text_pos)
    #     self.__update_scrolling_text_pos(renderer.render())
    #   else:
    #     StatusRenderer(self.canvas, scoreboard, self.data).render()
    # else:
    #   scoreboard = Scoreboard(overview)
    #   ScoreboardRenderer(self.canvas, scoreboard, self.data).render()
    # scoreboard = Scoreboard(overview)
    # ScoreboardRenderer(self.canvas, scoreboard, self.data).render()
    ScoreboardRenderer(self.canvas, self.data).render()
    self.canvas = self.matrix.SwapOnVSync(self.canvas) # TODO: what is this for? guess I'll find out

