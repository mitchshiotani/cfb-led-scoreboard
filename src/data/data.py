from src.api.cfb import FootballAPIWrapper as cfb

class Data:
  def __init__(self, config):
    # cfb module
    self.cfb = cfb()
    # Save the parsed config
    self.config = config

    # Parse today's date and see if we should use today or yesterday
    # self.set_current_date()

    # Flag to determine when to refresh data
    self.needs_refresh = True
    self.current_game_index = 0 # will do stuff with preferred teams later (game_index_for_preferred_team)
    
    # Fetch the games for today
    self.refresh_games()

  def advance_to_next_game(self):
    self.current_game_index = self.__next_game_index()
    return self.current_game()
 

  def current_game(self):
    return self.games[self.current_game_index]

  def __next_game_index(self):
    counter = self.current_game_index + 1
    if counter >= len(self.games):
      self.refresh_games()
      counter = 0
    return counter

  def refresh_games(self):
    games = self.cfb.day()
    if self.config.is_my_team_mode:
      # using lambda because making it a function would've been painful with getting team names and preferred teams and such
      print(games[0].home.team_name)
      filtered_games = filter(lambda x: x.home.team_location in self.config.preferred_teams or x.away.team_location in self.config.preferred_teams, games)
      games = list(filtered_games)
    self.games = games
