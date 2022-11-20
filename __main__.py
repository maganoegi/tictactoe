from typing import Tuple, Optional

import strategies
import tictactoe as ttt


def basic_numeric_input_handler(prompt: str) -> int:
    res = input(prompt) 
    return int(res) if res.isnumeric() else None

def basic_user_input_handler() -> Tuple[Optional[int], Optional[int]]:
    row = input("Row:\t")
    col = input("Col:\t") 
    
    col = int(col) if col.isnumeric() else None
    
    return row, col

def main() -> None:
    """ Driver function responsible for testing of the exercise code. 
    
        Mission statement: 
            * create a grid MxN
            * fill it with values representing X and O
            * evaluate the game status 
            * print the result

        The design of the structure was created to be an independent API. The 
        following design features have been implemented:
            * Easy-to-use interfacing with the grid entity.
            * low coupling evaluation strategy - Strategy design pattern
            * a mix between functional and object paradigms, allowing for 
                greater flexibility.
                * dataclasses
                * pure methods/functions
                * no mutability - rather return of object
    """
    m = 5
    n = 5
    k = 3

    # evaluation_strategy = strategies.RngStrategy
    evaluation_strategy = strategies.CheckForWinStrategy
    game = ttt.TicTacToe.create_game(m, n, k, evaluation_strategy)

    while not game.is_done():
        print("===================================================")
        print(game)

        row = basic_numeric_input_handler("Row:\t")
        col = basic_numeric_input_handler("Col:\t")
        is_coords_invalid = None in [row, col]
        if is_coords_invalid or not game.is_play_valid(row, col): 
            print("ERROR: Please provide correct integer input values...")
            continue

        game = game.play_at(row, col).toggle_next_turn()

        print(game.round_result_string())
    print(game)


if __name__ == '__main__':
    main()