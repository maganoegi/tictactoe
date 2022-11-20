from typing import TYPE_CHECKING, Dict, Any, List
import abc
import random
if TYPE_CHECKING:
    import tictactoe as ttt

import grid

MAX_SCORE = 10.0
MIN_SCORE = -10.0

def count_consecutive_in_list(lst: List[Any], target_value: Any) -> int:
    counter = 0
    for v in lst:
        if v == target_value:
            counter += 1

        else: 
            break
    
    return counter
        

class TicTacToeEvaluationStrategy( abc.ABC ):
    @classmethod
    @abc.abstractmethod
    def evaluate(cls, game: 'ttt.TicTacToe') -> Dict[grid.CellStatus, float]:
        """ abstract method for grid evaluation algorithm. """


class RngStrategy( TicTacToeEvaluationStrategy ):
    @classmethod
    def evaluate(
        cls, 
        game: 'ttt.TicTacToe'
    ) -> Dict[grid.CellStatus, float]:
        """ Random approach at evaluating a configuration on the board. """
        return {
            p: float(random.randint(MIN_SCORE, MAX_SCORE))
            for p 
            in grid.CellStatus.get_playables()
        }


class CheckForWinStrategy( TicTacToeEvaluationStrategy ):
    @classmethod
    def evaluate(cls, game: 'ttt.TicTacToe') -> Dict[grid.CellStatus, float]:
        """ checks whether a given player has won.

            This is done by checking every direction from the last position of
            the player. Different sub-lists are then constructed, and the 
            sequences counted. If a sequence greater than K is found, the 
            maximum score is attributed
        """
        last_move = game.log[-1]
        board = last_move.board.grid
        row_played = last_move.row
        col_played = last_move.col
        player = last_move.player
        height = game.board.height
        width = game.board.width
        k = game.nb_align_2_win

        east = board[row_played][col_played:]
        west = board[row_played][:col_played][::-1]
        north = [v[col_played] for v in board[:row_played]][::-1]
        south = [v[col_played] for v in board[row_played:]]

        southeast = [
            board[r][c] 
            for c, r 
            in zip(range(col_played, width), range(row_played, height))
        ]
        northwest = [
            board[r][c] 
            for c, r
            in zip(reversed(range(col_played)), reversed(range(row_played)))
        ]
        northeast = [
            board[r][c] 
            for c, r 
            in zip(range(col_played, width), reversed(range(row_played+1)))
        ]
        southwest = [
            board[r][c] 
            for c, r 
            in zip(reversed(range(col_played+1)), range(row_played, height))
        ]

        east_counter = count_consecutive_in_list(east, player)
        west_counter = count_consecutive_in_list(west, player)
        horizontal_counter = east_counter + west_counter

        north_counter = count_consecutive_in_list(north, player)
        south_counter = count_consecutive_in_list(south, player)
        vertical_counter = north_counter + south_counter

        southeast_counter = count_consecutive_in_list(southeast, player)
        northwest_counter = count_consecutive_in_list(northwest, player)
        right_diagonal_counter = southeast_counter + northwest_counter

        northeast_counter = count_consecutive_in_list(northeast, player)
        southwest_counter = count_consecutive_in_list(southwest, player)
        left_diagonal_counter = northeast_counter + southwest_counter - 1

        counters = [
            horizontal_counter, 
            vertical_counter, 
            right_diagonal_counter,
            left_diagonal_counter
        ]

        contains_winning_sequence = any(map(lambda x: x >= k, counters))

        score = MAX_SCORE if contains_winning_sequence else MIN_SCORE

        return {
            player: score,
            grid.CellStatus.toggle_other_playable(player): MIN_SCORE
        }