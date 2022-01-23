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

  def game_index_for_preferred_team(self):
    if self.config.preferred_teams:
      return self.__game_index_for(self.config.preferred_teams[0])
    else:
      return 0

  def __next_game_index(self):
    counter = self.current_game_index + 1
    if counter >= len(self.games):
      counter = 0
    return counter

  def refresh_games(self):
    all_games = self.cfb.day()
    self.games = all_games
    
      

