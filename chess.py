import numpy as np
import json


class piece:
    def __init__(self, position: np.array, color: bool):
        self.name = ''
        self.position = position
        self.alive = True
        self.color = color  # white = False, black = True
        self.moves = np.array([[0, 0]])
        self.possible_moves = position

    def __repr__(self) -> str:
        str_color = 'white'
        if self.color: str_color = 'black'
        return json.dumps({
            'piece': self.name,
            'color': str_color,
            'is_alive': self.alive,
            'position': str(self.position),
            'possible_moves': str(self.possible_moves)
        }, indent=4)

    def move(self, new_position: list):
        if new_position in self.possible_moves.tolist():
            # Update position
            self.position = np.array(new_position)

            # Update possible moves
            self.possible_moves = self.moves + self.position
            self.possible_moves = self.possible_moves[np.where(
                np.apply_along_axis(lambda a: all(a>=0) & all(a<=7), 1, self.possible_moves)
            )]
            return True
        return False




class king(piece):
    def __init__(self, position: np.array, color: bool):
        super().__init__(position, color)
        self.name = 'K'
        self.moves = np.array([
            [1, 1], [1, 0], [1, -1], 
            [0, 1], [0, -1], 
            [-1, 1], [-1, 0], [-1, -1]
        ])

        self.possible_moves = self.moves + self.position
        self.possible_moves = self.possible_moves[np.where(
            np.apply_along_axis(lambda a: all(a>=0) & all(a<=7), 1, self.possible_moves)
        )]


if __name__ == '__main__':
    wK = king(position=np.array([4, 0]), color=0)
    print(wK)
    wK.move([4, 1])
    print(wK)
    wK.move([7, 1])
    print(wK)

