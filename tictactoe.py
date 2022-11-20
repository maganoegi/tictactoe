from typing import List, Dict, Optional
import dataclasses
import math

import grid
import strategies


@dataclasses.dataclass
class TicTacToeLogItem:
    board:  grid.Grid
    player: grid.CellStatus
    row: int
    col: int
    score: Optional[int] = None


@dataclasses.dataclass
class TicTacToe:
    board: grid.Grid
    nb_align_2_win: int
    current_turn: grid.CellStatus
    evaluation_strategy: strategies.TicTacToeEvaluationStrategy
    log: List[TicTacToeLogItem]

    @classmethod
    def create_game(
        cls, 
        height: int, 
        width: int, 
        nb_align_2_win: int, 
        evaluation_strategy: strategies.TicTacToeEvaluationStrategy
    ) -> 'TicTacToe':
        """ Named constructor, allowing for flow control of the program. """
        return cls(
            board=grid.Grid.generate_with_dims(height, width),
            current_turn=grid.CellStatus.X,
            evaluation_strategy=evaluation_strategy,
            nb_align_2_win=nb_align_2_win,
            log=[]
        )

    def is_done(self) -> bool:
        """ Custom logic for determining whether the game has ended. """
        is_first_turn = not len(self.log)
        res = False
        if not is_first_turn:
            res = math.isclose(self.log[-1].score, strategies.MAX_SCORE)
            print("SCORE", self.log[-1].score, res)

        return res

    def toggle_next_turn(self) -> 'TicTacToe':
        """ Functional style method. Toggles player state, then returns. """
        self.current_turn = grid.CellStatus.toggle_other_playable(
            self.current_turn
        )
        return self

    def is_play_valid(self, row: int, col: int) -> bool:
        """ checks whether the coordinates provided can be inserted """
        return self.board.is_insert_valid(row, col)

    def play_at(self, row: int, col: int) -> 'TicTacToe':
        """ Executes a turn at the specified coordinates. 

            We assume that the operation will be legal. Other methods can be 
            used to determine the validity of a play.
        """
        self.board = self.board.insert_at(row, col, self.current_turn)
        self.log.append(TicTacToeLogItem(
            self.board,
            self.current_turn, 
            row, 
            col
        ))
        score = self.evaluate_round_using_strategy(self.evaluation_strategy)
        self.log[-1].score = score[self.current_turn]
        return self

    def round_result_string(self) -> str:
        """  Simple helper formatting function. """
        last_turn = self.log[-1]
        return "\n".join([
            f"Player: {last_turn.player.value}",
            f"Inserted At row: {last_turn.row}, col: {last_turn.col}",
            f"Score: {last_turn.score}",
            f"with strategy: {self.evaluation_strategy.__name__}"
        ]) 

    def evaluate_round_using_strategy(
        self, 
        strategy: strategies.TicTacToeEvaluationStrategy
    ) -> Dict[grid.CellStatus, float]:
        """ Allows for inner as well as outer usages of strategies. 

            Low coupling for the different strategies that can be used to 
            evaluate a solution. Allows for a run-time strategy switch.
        """
        return strategy.evaluate(self)

    def __str__(self) -> str:
        return f"\n{self.board}\n\nCurrent player: {self.current_turn.value}"
