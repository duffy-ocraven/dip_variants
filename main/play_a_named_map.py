# the following script, from https://pypi.org/project/diplomacy/
# plays a game locally by submitting random valid orders until the game is completed.

import random
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format
import sys, getopt, os

# Creating a game
# Alternatively, a map_name can be specified as an argument. e.g. Game(map_name='pure')
def main():
  try:   
   (options, arguments) = getopt.getopt(sys.argv[1:], 'h')
  except getopt.error:
   sys.exit("Unknown input parameter.")
  if [] == arguments:
    arguments = ["shiftLeft"]
  if not os.path.exists(arguments[0] + ".map"):
    sys.exit("%s.map could not be opened" % (arguments[0],))
  game = Game(map_name=arguments[0])
  while not game.is_game_done:

    # Getting the list of possible orders for all locations
    possible_orders = game.get_all_possible_orders()

    # For each power, randomly sampling a valid order
    for power_name, power in game.powers.items():
#        power_orders = [random.choice(possible_orders[loc]) for loc in game.get_orderable_locations(power_name)
#                        if possible_orders[loc]]
        power_orders = []
        for loc in game.get_orderable_locations(power_name):
          if '/' == loc[-1]:
            loc = loc[:-1]
          if possible_orders[loc]:
            power_orders.append(random.choice(possible_orders[loc]))
        game.set_orders(power_name, power_orders)

    # Messages can be sent locally with game.add_message
    # e.g. game.add_message(Message(sender='FRANCE',
    #                               recipient='ENGLAND',
    #                               message='This is a message',
    #                               phase=self.get_current_phase(),
    #                               time_sent=int(time.time())))

    # Processing the game to move to the next phase
    game.process()

# to_saved_game_format(game, output_path='collected_autoplay_games.json')
# Exporting the game to disk to visualize (game is appended)
  with open('collected_autoplay_games.json', 'a') as outp:
    outp.write(to_saved_game_format(game))
      
if __name__ == '__main__':
   main()
