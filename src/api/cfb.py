import urllib.request
import json
from scrape_util import api_to_json
import munch

# NFL_URL = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
CFB_URL = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'

class FootballAPIWrapper:
  def overview(self, match_id):
    """
    Get details of specific game. 
    """
    matches = self.day()
    for match in matches:
      if match.match_id == match_id:
        return match
    # not the most efficient way, but it'll work

  def day(self):
    """
    Get all the games occurring in the day 
    """
    matches_data = self.__generate_match_list(CFB_URL)
    matches = []
    for match_data in matches_data:
      match = munch.munchify(match_data)
      matches.append(match)
    return matches

  def __give_display_period(self, period):
      if period <= 4:
          return "Q" + str(period)
      elif period == 5:
          return "OT"
      elif period > 5:
          return str(period - 4) + "OT"

  def __get_basic_data(self, match_info, event):
      """input: dictionary | output: dictionary updated"""
      match_info['status'] = event['status']['type']['name']
      match_info['start_time'] = event['date']
      match_info['match_id'] = event['id']
      match_info['time'] = event['status']['displayClock']
      match_info['period'] = event['status']['period']
      match_info['display_period'] = self.__give_display_period(match_info['period'])
      match_info['detail'] = event['status']['type']['detail']
      match_info['match_type_id'] = event['status']['type']['id']
      return match_info

  def __get_team_data(self, match_info, event, num, key):
      homeaway = event["competitions"][0]['competitors'][key]['homeAway']
      match_info[homeaway] = {}
      match_info[homeaway]['team_score'] = int(event["competitions"][0]['competitors'][key]['score'])
      #    name
      match_info[homeaway]['team_id'] = int(event["competitions"][0]['competitors'][key]['team']['id'])
      match_info[homeaway]['team_name'] = event["competitions"][0]['competitors'][key]['team']['displayName']
      match_info[homeaway]['team_name_abv'] = event["competitions"][0]['competitors'][key]['team']['abbreviation']
      match_info[homeaway]['team_location'] = event["competitions"][0]['competitors'][key]['team']['location']
      #    color (primary and alternative)
      match_info[homeaway]['team_color_prm'] = event["competitions"][0]['competitors'][key]['team']['color']
      try:
          match_info[homeaway]['team_color_alt'] = event["competitions"][0]['competitors'][key]['team']['alternateColor']
      except KeyError:
          match_info[homeaway]['team_color_alt'] = 'ffffff'
      # more exceptions
      try:
          match_info[homeaway]['team_score_qtrs'] = [int(score['value']) for score in event["competitions"][0]['competitors'][key]['linescores']]
      except KeyError:
          pass
      try:
          match_info[homeaway]['team_ranking'] = event["competitions"][0]['competitors'][key]['curatedRank']['current']
      except KeyError:
          pass

      return match_info

  # for 'STATUS_IN_PROGRESS' games, get live data

  def __get_live_data(self, match_info, event):
      """input: dictionary | output: dictionary updated if match is live"""
      for stat in ['downDistanceText', 'shortDownDistanceText', 'possession', 'possessionText', 'isRedZone']:
          try:
              match_info[stat] = event["competitions"][0]['situation'][stat]
          except KeyError:
              pass
      return match_info


  def __generate_match_info(self, event):
      # ignore if event is postponed
      if event['status']['type']['name'] in ['STATUS_POSTPONED', 'STATUS_CANCELED']:
          return None
      # otherwise, continue
      match_info = {}
      match_info = self.__get_basic_data(match_info, event)
      # team info for both teams
      team_enc = {'one' : 0, 'two' : 1}
      for t in team_enc:
          match_info = self.__get_team_data(match_info, event, t, team_enc[t])
      # get live data
      match_info = self.__get_live_data(match_info, event)
      return match_info

  def __generate_match_list(self, url):
      parsed = api_to_json(url)
      master_list = [self.__generate_match_info(e) for e in parsed['events'] if self.__generate_match_info(e)]
      return master_list
