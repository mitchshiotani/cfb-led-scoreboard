# pseudo-code
# fetch data from api
# save relevant data into variables

import urllib.request
import json
from scrape_util import api_to_json


def give_display_period(period):
    if period <= 4:
        return "Q" + str(period)
    elif period == 5:
        return "OT"
    elif period > 5:
        return str(period - 4) + "OT"

def get_basic_data(match_info, event):
    """input: dictionary | output: dictionary updated"""
    match_info['status'] = event['status']['type']['name']
    match_info['start_time'] = event['date']
    match_info['match_id'] = event['id']
    match_info['time'] = event['status']['displayClock']
    match_info['period'] = event['status']['period']
    match_info['display_period'] = give_display_period(match_info['period'])
    match_info['detail'] = event['status']['type']['detail']
    match_info['match_type_id'] = event['status']['type']['id']
    return match_info

def get_team_data(match_info, event, num, key):
    match_info['team_{}_score'.format(num)] = int(event["competitions"][0]['competitors'][key]['score'])
    #    name
    match_info['team_{}_id'.format(num)] = int(event["competitions"][0]['competitors'][key]['team']['id'])
    match_info['team_{}_name'.format(num)] = event["competitions"][0]['competitors'][key]['team']['displayName']
    match_info['team_{}_name_abv'.format(num)] = event["competitions"][0]['competitors'][key]['team']['abbreviation']
    #    color (primary and alternative)
    match_info['team_{}_color_prm'.format(num)] = event["competitions"][0]['competitors'][key]['team']['color']
    try:
        match_info['team_{}_color_alt'.format(num)] = event["competitions"][0]['competitors'][key]['team']['alternateColor']
    except KeyError:
        match_info['team_{}_color_alt'.format(num)] = 'ffffff'
    # more exceptions
    try:
        match_info['team_{}_score_qtrs'.format(num)] = [int(score['value']) for score in event["competitions"][0]['competitors'][key]['linescores']]
    except KeyError:
        pass
    try:
        match_info['team_{}_ranking'.format(num)] = event["competitions"][0]['competitors'][key]['curatedRank']['current']
    except KeyError:
        pass

    return match_info

# for 'STATUS_IN_PROGRESS' games, get live data

def get_live_data(match_info, event):
    """input: dictionary | output: dictionary updated if match is live"""
    for stat in ['downDistanceText', 'shortDownDistanceText', 'possession', 'possessionText', 'isRedZone']:
        try:
            match_info[stat] = event["competitions"][0]['situation'][stat]
        except KeyError:
            pass
    return match_info


def generate_match_info(event):
    # ignore if event is postponed
    if event['status']['type']['name'] in ['STATUS_POSTPONED', 'STATUS_CANCELED']:
        return None
    # otherwise, continue
    match_info = {}
    match_info = get_basic_data(match_info, event)
    # team info for both teams
    team_enc = {'one' : 0, 'two' : 1}
    for t in team_enc:
        match_info = get_team_data(match_info, event, t, team_enc[t])
    # get live data
    match_info = get_live_data(match_info, event)
    return match_info

def generate_match_list(url):
    parsed = api_to_json(url)
    master_list = [generate_match_info(e) for e in parsed['events'] if generate_match_info(e)]
    return master_list

if __name__ == "__main__":
    url = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
    master_list = generate_match_list(url)
    print(master_list[0])






