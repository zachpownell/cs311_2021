# Import fun stuff.
import argparse
import random
import json
from os.path import exists

########################################################################################################################

# Name: Zachary Pownell
# Professor: Cary Jardin
# Class: CS311 Data Structures & Algorithms
# Date: 26 October, 2021

# How my agent works:
# My agent will acknowledge when a new game begins and keep track of how many iterations will be played, along with
# my opponents move history. By using this information, we can try to get the least jail time. My agent has special
# parameters to hold a grudge, become aggressive (and also become more aggressive), randomly confess when my agent
# would otherwise choose to be silent, and choose to confess on the final rounds. I figured the strategy of confessing
# on only the final round of my opponents may be common, so we can confess on the last x amount of rounds.
# Assignment of these parameters can be found in the params dictionary below. My agent will also keep track of their
# opponents move history. The use of data structures is applied to counting the length of games to make decisions on
# whether to be silent or confess. By assigning our parameters in the params dictionary, our agent can either be a nice
# agent or a real asshole.

########################################################################################################################

# Name assignment of the opponent move history and params json files.
OPPONENT_HISTORY_FILE = "opponent_history_file.json"
PARAM_FILE = "param_file.json"

# Params dictionary containing all of my agents parameters.
params = {
    # If hold_a_grudge = True, my agent will hold a grudge and confess for the duration of HOLD_A_GRUDGE_LENGTH.
    "hold_a_grudge": True,
    # How many turns my agent will hold a grudge (chooses confess) if the opponent initially chooses confess.
    "hold_a_grudge_length": 2,
    # If this is true, then we will increase our hold_a_grudge_length by 1.
    "hold_a_grudge_increment": True,
    # If random_confess = True, randomly become confess if my agent chooses to silent.
    "random_confess": True,
    # Chooses a number between 1 and random_confess_odds if random_confess = True. If my agent chooses to be silent,
    # flip to confess. Adds unpredictable spice.
    "random_confess_odds": 100,
    # If become_aggressive = True, decrement our random_confess_odds by aggressive_decrement. Do this until our
    # aggressive_cap is reached.
    "become_aggressive": True,
    "aggressive_decrement": 1,
    "aggressive_cap": 5,
    # Do we want to confess on the final x amount of rounds? x being the parameter confess_on_last.
    "confess_on_final_rounds": True,
    "confess_on_last": 4,
    # Iterations in game to make sure we can confess on the final rounds. IGNORE.
    "iterations_in_game": 0,
    # Counter for holding a grudge. IGNORE.
    "hold_a_grudge_counter": 0
}

# Opponents history dictionary to keep track of my opponents moves in. Will save this to a separate json file from
# params (OPPONENT_HISTORY_FILE).
opponent_history = {
    "history": ""
}


# dump_file function saves param or opponent dictionary from program into json file.
def dump_file(file):

    if file == PARAM_FILE:
        with open(PARAM_FILE, "w") as f:
            json.dump(params, f)
    elif file == OPPONENT_HISTORY_FILE:
        with open(OPPONENT_HISTORY_FILE, "w") as f:
            json.dump(opponent_history, f)


# load_file function loads param or opponent history from json file into program.
def load_file(file):

    # Check if our file actually exists.
    if not exists(file):
        dump_file(file)
    with open(file) as f:
        return json.load(f)


# Print all the elements from dictionaries. Used for debugging purposes. IGNORE.
def print_data():

    print("\n\n\n-------------- PARAM FILE --------------")
    print(params)

    print("\n-------------- OPPONENT HISTORY FILE --------------")
    print(opponent_history)
    print("\n\n\n")


# Lets start a round.
if __name__ == "__main__":

    # Argparse initiation.
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', help='called when new game')
    parser.add_argument('--iterations', help='number of iterations in game')
    parser.add_argument('--last_opponent_move', help='last opponent move')
    args = parser.parse_args()

    # Assign opponents_last_move to the opponents last move, iterations to iterations, and is_new_game to init from
    # arg parser.
    is_new_game = args.init
    iterations = args.iterations
    opponents_last_move = args.last_opponent_move

    # First, lets check if a new game is initialized. If so, reset our params and opponent history json files to
    # default settings found in our programs dictionary.
    if is_new_game is not None:
        dump_file(PARAM_FILE)
        dump_file(OPPONENT_HISTORY_FILE)
    else:
        # Load up our param file and opponent history file from json into program by calling functions.
        params = load_file(PARAM_FILE)
        opponent_history = load_file(OPPONENT_HISTORY_FILE)

    # Lets record our opponent history.
    try:
        opponent_history["history"] += opponents_last_move[0]
    except TypeError:
        pass

    # Save our opponent history to json file.
    dump_file(OPPONENT_HISTORY_FILE)

    # Now, lets check if iterations was assigned. If so, assign our iterations in game to iterations.
    if iterations is not None:
        params["iterations_in_game"] = int(iterations)

    # Decrement iterations in game.
    params["iterations_in_game"] -= 1

    # Time to determine if our opponents last move was confess or stay silent.

    # Opponent confessed.
    if opponents_last_move == "confess":

        # Check if our agent is going to hold a grudge.
        if params["hold_a_grudge"]:

            # If so, we assign our hold a grudge counter to hold a grudge length. Start a new grudge.
            params["hold_a_grudge_counter"] = params["hold_a_grudge_length"]

            if params["hold_a_grudge_increment"]:
                params["hold_a_grudge_length"] += 1

            print("confess")

        # Otherwise if hold a grudge is false, keep silent. Even if opponent's last move was confess.
        else:
            print("silent")

        # Now lets check if my agent will become more aggressive now that my opponent chose confess.
        if params["become_aggressive"]:

            if params["random_confess_odds"] >= params["aggressive_cap"]:

                params["random_confess_odds"] -= params["aggressive_decrement"]

    # Opponent silent.
    else:

        # First, lets check if we're playing the last few rounds.
        if params["iterations_in_game"] <= params["confess_on_last"]:

            # If so, lets check if confess_on_final_rounds is true.
            if params["confess_on_final_rounds"]:
                print("confess")
            else:
                print("silent")

        # If its not the last few iterations in game, lets check if our agent is currently holding a grudge or wants to
        # randomly confess.
        else:

            # If the hold_a_grudge_counter does not equal 0, confess and decrement hold_a_grudge_counter by 1.
            if params["hold_a_grudge_counter"] != 0:

                # Confess because we are holding a grudge. Angry.
                print("confess")
                params["hold_a_grudge_counter"] -= 1

            # Otherwise if we are not holding a grudge, check if we want to randomly confess. We use this if else
            # statement so we don't accidentally say say confess twice.
            else:

                # Lets check if our agent is randomly confessing. Sneaky.
                if params["random_confess"]:

                    # Try catch statement to make sure we are not infinitely randomly confessing.
                    try:

                        if random.randint(0, params["random_confess_odds"]) == 0:
                            print("confess")
                        else:
                            print("silent")

                    # We are super aggressive. Lets be nice.
                    except ValueError:

                        print("silent")

                # Otherwise if our agent is not randomly confessing, be silent.
                else:

                    print("silent")

    # Save our game to param files.
    dump_file(PARAM_FILE)
    dump_file(OPPONENT_HISTORY_FILE)
