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
    self.scrolling_finished = False
    self.starttime = time.time()

  def render(self):
    self.starttime = time.time()

    # # Always display the news ticker
    # if self.data.config.news_ticker_always_display:
    #   self.__render_offday()

    # # Always display the standings
    # elif self.data.config.standings_always_display:
    #   self.__render_standings()

    # # Full MLB Offday
    # elif self.data.is_offday():
    #   if self.data.config.standings_mlb_offday:
    #     self.__render_standings()
    #   else:
    #     self.__render_offday()

    # # Preferred Team Offday
    # elif self.data.is_offday_for_preferred_team():
    #   if self.data.config.news_ticker_team_offday:
    #     self.__render_offday()
    #   elif self.data.config.standings_team_offday:
    #     self.__render_standings()
    #   else:
    #     self.__render_game()

    # # Playball!
    # else:
    #   self.__render_game()
    self.__render_game() # to make it clear to just render games for now

  # Renders a game screen based on it's status
  def __render_game(self):
    while True:
      # If we need to refresh the overview data, do that

      # if self.data.needs_refresh:
      #   self.data.refresh_overview()

      # Draw the current game
      # self.__draw_game(self.data.current_game(), self.data.overview)
      # self.__draw_game(self.data)
      self.__draw_game()

      # # Check if we need to scroll until it's finished
      # if self.data.config.rotation_scroll_until_finished == False:
      #   self.scrolling_finished = True

      # # Set the refresh rate
      # refresh_rate = self.data.config.scrolling_speed

      # # Currently the only thing that's always static is the live scoreboard
      # if Status.is_static(self.data.overview.status):
      #   self.scrolling_finished = True

      # # If the status is irregular and there's no 'reason' text, finish scrolling
      # if Status.is_irregular(self.data.overview.status) and Scoreboard(self.data.overview).get_text_for_reason() is None:
      #   self.scrolling_finished = True

      # time.sleep(refresh_rate)
      # endtime = time.time()
      # time_delta = endtime - self.starttime
      # rotate_rate = self.__rotate_rate_for_status(self.data.overview.status)

      # # If we're ready to rotate, let's do it
      # if time_delta >= rotate_rate and self.scrolling_finished:
      #   self.starttime = time.time()
      #   self.scrolling_finished = False
      #   self.data.needs_refresh = True

      #   if Status.is_fresh(self.data.overview.status):
      #     self.scrolling_text_pos = self.canvas.width

      #   if self.__should_rotate_to_next_game(self.data.overview):
      #     self.scrolling_text_pos = self.canvas.width
      #     game = self.data.advance_to_next_game()

      #   if endtime - self.data.games_refresh_time >= GAMES_REFRESH_RATE:
      #     self.data.refresh_games()

      #   if self.data.needs_refresh:
      #     self.data.refresh_overview()

      #   if Status.is_complete(self.data.overview.status):
      #     if Final(self.data.current_game()).winning_pitcher == 'Unknown':
      #       self.data.refresh_games()

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

