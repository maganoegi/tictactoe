from typing import List
import enum
import dataclasses


class CellStatus( enum.Enum ):
    EMPTY = '_' 
    X = 'X'
    O = 'O'

    @classmethod
    def toggle_other_playable(cls, current: 'CellStatus') -> 'CellStatus':
        """ Helper function for getting the other player value. """
        return cls.X if current == cls.O else cls.O

    @classmethod
    def get_playables(cls) -> List['CellStatus']: 
        return [v for v in cls if v is not cls.EMPTY]


@dataclasses.dataclass
class Grid:
    height: int
    width: int
    grid: List[List[CellStatus]]

    @classmethod
    def generate_with_dims(cls, height: int, width: int) -> 'Grid':
        grid = [[CellStatus.EMPTY for _ in range(width)] for _ in range(height)]
        return cls(height, width, grid)

    def is_insert_valid(self, row: int, col: int) -> bool:
        is_in_bounds_y = 0 <= row < self.height
        is_in_bounds_x = 0 <= col < self.width

        return(
            self.get_value_at(row, col) == CellStatus.EMPTY 
            if is_in_bounds_x and is_in_bounds_y 
            else False
        )

    def insert_at(self, row: int, col: int, player: CellStatus) -> 'Grid':
        self.grid[row][col] = player
        return self

    def get_value_at(self, row: int, col: int) -> CellStatus:
        return self.grid[row][col]

    def __str__(self) -> str:
        return "\n".join([
            f"{row_nb} " + 
            "".join([v.value for v in row]) 
                for row_nb, row 
                in enumerate(self.grid)
        ]) + "\n  " + "".join([str(i) for i in range(len(self.grid[0]))])