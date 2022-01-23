# from api.cfb import FootballAPIWrapper as cfb
from cfb import FootballAPIWrapper as CFB
import pprint

def main():
  cfb = CFB()
  all_games = cfb.day()
  print("all_games")
  pprint.pprint(all_games)
  # for game in all_games:
  #   # to show that munchify worked properly
  #   print(game.home.team_color_prm)
  #   print(__convert_hex_to_rgb(game.home.team_color_prm))
  #   print(game.away.team_color_prm)
  #   print(__convert_hex_to_rgb(game.away.team_color_prm))

def __convert_hex_to_rgb(hex_str):
  # convert hex to rgb, to put into graphics.Color()
  r = int(hex_str[0:2], 16)
  g = int(hex_str[2:4], 16)
  b = int(hex_str[4:6], 16)
  return {'r': r, 'g': g, 'b': b}

main()

