
import random
from diplomacy import Game
from diplomacy.utils.export import from_saved_game_format
from diplomacy.utils.export import is_valid_saved_game
from diplomacy.utils.export import to_saved_game_format
import ujson as json
import sys, getopt, os

# Creating a game
# map file's baseName can be the map_name argument. e.g. Game(map_name='pure')
# the following script, from https://pypi.org/project/diplomacy/
# plays a game locally by submitting random valid orders until the game is completed.
def main():
  try:   
   (options, arguments) = getopt.getopt(sys.argv[1:], 'h')
  except getopt.error:

  if [] == arguments:
    sys.exit("Unknown input parameter.")

  file_name = arguments[0]
  phrase = arguments[1]
  with open(file_name, 'r') as file:
    for line in file:
      input_combined_lines = ''
      if(line.strip().find("orders") != -1):
        input_combined_lines += '"orders":{},"results":{},"messages":[]}]}'
        input = json.loads(input_combined_lines)
        break
      input_combined_lines += line.strip()
    else:
      sys.exit("File %s is invalid")

  input_path = "../unitTestPureGame.json"
  if not os.path.exists(input_path):
    sys.exit("File %s does not exist." % input_path)
  with open(input_path, 'r') as file:
    combined_lines = ''
    for line in file:
      game_combined_lines += line.strip()
      if(line.strip()== ''):
        saved_game = json.loads(game_combined_lines)
        game = from_saved_game_format(saved_game)
        break
    else:
      sys.exit("File %s is invalid")

  if not is_valid_saved_game(saved_game):
    sys.exit("File %s was evaluated as invalid." % input_path)
  if not game.is_game_done:
    # For each power, the F1922M orders are already set
    game.process() # process those, then for W1922A, do random
    # Getting the list of possible orders for all locations
    possible_orders = game.get_all_possible_orders()

    # For each power, randomly sampling a valid order
    for power_name, power in game.powers.items():
        power_orders = []
        for loc in game.get_orderable_locations(power_name):
          if '/' == loc[-1]:
            loc = loc[:-1]
          if possible_orders[loc]:
            power_orders.append(random.choice(possible_orders[loc]))
            print("%s for %s" % (power_orders[-1], power_name))
        game.set_orders(power_name, power_orders)
    game.process()
# Exporting the game to disk to visualize
    with open('unitTestResult_game.json', 'w') as outp:
      outp.write(to_saved_game_format(game))

if __name__ == '__main__':
   main()
