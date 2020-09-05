
import random
from diplomacy import Game
from diplomacy.utils.export import from_saved_game_format
from diplomacy.utils.export import is_valid_saved_game
from diplomacy.utils.export import to_saved_game_format
from argparse import ArgumentParser
import ujson as json
import sys, getopt, os

def Usage():
  sys.exit("loadDiplomacyGame.py\n"
   "file_name = arguments[0]\n"
   "phase = arguments[1]\n"
   "Outputs the game to disk to visualize\n"
   "with open('unitTestResult_game.json', 'w') as outp, so overwrites\n")
# the following script, from https://pypi.org/project/diplomacy/
# plays a game locally by submitting random valid orders until the game is completed.
def main(file_name, phase, UseExistingOrders):
  if(len(phase) != 6):
    sys.exit("Invalid phase length")
  if not os.path.exists(file_name):
    sys.exit("File %s does not exist." % file_name)


  with open(file_name, 'r') as file:
    loop_control = False
    input_combined_lines = ''
    for line in file:
      name_index = line.find("name")
      if(name_index != -1 and line[name_index+7] == phase[0]):
        if(line[name_index+8:name_index+13]==phase[1:]):
          loop_control = True
        elif(line[name_index+8:name_index+13]>phase[1:]):
          sys.exit("Phase value not found")
     
      if(line.find("orders")!= -1 and bool(loop_control)):
        if(bool(UseExistingOrders)):
          input_combined_lines += line.strip()
        else:
          input_combined_lines += '"orders":{},'
        input_combined_lines += '"results":{},"messages":[]}]}'
        loaded_input = json.loads(input_combined_lines)
        input = from_saved_game_format(loaded_input)
        break
      input_combined_lines += line.strip()
    else:
      sys.exit("File %s is invalid" % file_name)

  game = from_saved_game_format(loaded_input)
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
    if not game.is_game_done and bool(UseExistingOrders):
      game.process() # process those, then after do random
    while not game.is_game_done:
      possible_orders = game.get_all_possible_orders()
      for power_name, power in game.powers.items():
        power_orders = [random.choice(possible_orders[loc]) for loc in game.get_orderable_locations(power_name) if possible_orders[loc]]
        game.set_orders(power_name, power_orders)
      game.process()
# Exporting the game to disk to visualize
    with open('unitTestResult_game.json', 'w') as outp:
      outp.write(to_saved_game_format(game))

if __name__ == '__main__':
   p = ArgumentParser()
   p.add_argument('file_name')
   p.add_argument('phase')
   p.add_argument('-u', action='store_true')

   args = p.parse_args()

   main(args.file_name, args.phase, args.u)
