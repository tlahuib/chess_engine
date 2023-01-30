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

    # Move this logic to the board class
    # def move(self, new_position: list):
    #     if new_position in self.possible_moves.tolist():
    #         # Update position
    #         self.position = np.array(new_position)

    #         # Update possible moves
    #         self.possible_moves = self.moves + self.position
    #         self.possible_moves = self.possible_moves[np.where(
    #             np.apply_along_axis(lambda a: all(a>=0) & all(a<=7), 1, self.possible_moves)
    #         )]
    #         return True
    #     return False


class king(piece):
    def __init__(self, position: np.array, color: bool):
        super().__init__(position, color)
        self.moves = np.array([
            [[0, 1]],  # Front
            [[1, 1]],  # Front-right
            [[1, 0]],  # Right
            [[1, -1]],  # Back-right
            [[0, -1]],  # Back
            [[-1, -1]],  # Back-left
            [[-1, 0]],  # Left
            [[-1, 1]]  # Front-left
        ])

        # self.possible_moves = self.moves + self.position
        # self.possible_moves = self.possible_moves[np.where(
        #     np.apply_along_axis(lambda a: all(a>=0) & all(a<=7), 1, self.possible_moves)
        # )]


class queen(piece):
    def __init__(self, position: np.array, color: bool, b_size=[8, 8]):
        super().__init__(position, color)
        self.moves = np.array([
            [[0, i] for i in range(1, b_size[1])],  # Front
            [[i, i] for i in range(1, min(b_size))],  # Front-right
            [[i, 0] for i in range(1, b_size[0])],  # Right
            [[i, -i] for i in range(1, min(b_size))],  # Back-right
            [[0, -i] for i in range(1, b_size[1])],  # Back
            [[-i, -i] for i in range(1, min(b_size))],  # Back-left
            [[-i, 0] for i in range(1, b_size[0])],  # Left
            [[-i, i] for i in range(1, min(b_size))]  # Front-left
        ])


class bishop(piece):
    def __init__(self, position: np.array, color: bool, b_size=[8, 8]):
        super().__init__(position, color)
        self.moves = np.array([
            [[i, i] for i in range(1, min(b_size))],  # Front-right
            [[i, -i] for i in range(1, min(b_size))],  # Back-right
            [[-i, -i] for i in range(1, min(b_size))],  # Back-left
            [[-i, i] for i in range(1, min(b_size))]  # Front-left
        ])


class rook(piece):
    def __init__(self, position: np.array, color: bool, b_size=[8, 8]):
        super().__init__(position, color)
        self.moves = np.array([
            [[0, i] for i in range(1, b_size[1])],  # Front
            [[i, 0] for i in range(1, b_size[0])],  # Right
            [[0, -i] for i in range(1, b_size[1])],  # Back
            [[-i, 0] for i in range(1, b_size[0])]  # Left
        ])


class knight(piece):
    def __init__(self, position: np.array, color: bool):
        super().__init__(position, color)
        self.moves = np.array([
            [1, 2],
            [2, 1],
            [2, -1],
            [1, -2],
            [-1, -2],
            [-2, -1],
            [-2, 1],
            [-1, 2]
        ])


class initial_pawn(piece):
    def __init__(self, position: np.array, color: bool):
        super().__init__(position, color)
        self.moves = np.array([
            [[0, 1], [0, 2]]
        ])


class board:
    def __init__(self, size=[8, 8]):
        self.size = size
        self.turn = False
        self.possible_moves_dict = {}

        # Black
        self.black = {
            '1R': rook(position=np.array([0, 7]), color=True, b_size=size),
            '1N': knight(position=np.array([1, 7]), color=True),
            '1B': bishop(position=np.array([2, 7]), color=True, b_size=size),
            'Q': queen(position=np.array([3, 7]), color=True, b_size=size),
            'K': king(position=np.array([4, 7]), color=True),
            '2B': bishop(position=np.array([5, 7]), color=True, b_size=size),
            '2N': knight(position=np.array([6, 7]), color=True),
            '2R': rook(position=np.array([7, 7]), color=True, b_size=size),
            '1p': initial_pawn(position=np.array([0, 6]), color=True),
            '2p': initial_pawn(position=np.array([1, 6]), color=True),
            '3p': initial_pawn(position=np.array([2, 6]), color=True),
            '4p': initial_pawn(position=np.array([3, 6]), color=True),
            '5p': initial_pawn(position=np.array([4, 6]), color=True),
            '6p': initial_pawn(position=np.array([5, 6]), color=True),
            '7p': initial_pawn(position=np.array([6, 6]), color=True),
            '8p': initial_pawn(position=np.array([7, 6]), color=True)
        }

        # White
        self.white = {
            '1R': rook(position=np.array([0, 0]), color=False, b_size=size),
            '1N': knight(position=np.array([1, 0]), color=False),
            '1B': bishop(position=np.array([2, 0]), color=False, b_size=size),
            'Q': queen(position=np.array([3, 0]), color=False, b_size=size),
            'K': king(position=np.array([4, 0]), color=False),
            '2B': bishop(position=np.array([5, 0]), color=False, b_size=size),
            '2N': knight(position=np.array([6, 0]), color=False),
            '2R': rook(position=np.array([7, 0]), color=False, b_size=size),
            '1p': initial_pawn(position=np.array([0, 1]), color=False),
            '2p': initial_pawn(position=np.array([1, 1]), color=False),
            '3p': initial_pawn(position=np.array([2, 1]), color=False),
            '4p': initial_pawn(position=np.array([3, 1]), color=False),
            '5p': initial_pawn(position=np.array([4, 1]), color=False),
            '6p': initial_pawn(position=np.array([5, 1]), color=False),
            '7p': initial_pawn(position=np.array([6, 1]), color=False),
            '8p': initial_pawn(position=np.array([7, 1]), color=False)
        }

        # Positions
        self.positions = {}
        for item in self.black:
            self.positions[str(
                self.black[item].position.tolist())] = 'b' + item
        for item in self.white:
            self.positions[str(
                self.white[item].position.tolist())] = 'w' + item

    def __repr__(self):
        s = ''
        for row in reversed(range(self.size[1])):
            s += str(row)
            for col in range(self.size[0]):
                position = str([col, row])
                if position in self.positions:
                    s += f'|{self.positions[position][0]}{self.positions[position][-1]}'
                else:
                    s += '|  '
            s += '|\n ' + ' --' * self.size[1] + '\n'
        s += '  ' + ' '.join([str(item).rjust(2)
                             for item in list(range(self.size[1]))])
        return s

    def possible_moves(self, str_piece: str):
        if str_piece in set(self.possible_moves_dict.keys()):
            return self.possible_moves_dict[str_piece]

        print(f'Calculating moves for {str_piece}')
        # Get piece from correct color
        try:
            if self.turn:
                piece2move = self.black[str_piece]
            else:
                piece2move = self.white[str_piece]
        except KeyError:
            print(f'Piece {str_piece} not found on the board')

        # Account for piece blocking
        moves = piece2move.moves + piece2move.position
        possible_moves = []
        if piece2move.__class__.__name__ != 'knight':
            for direction in moves:
                for move in direction:
                    if str(move.tolist()) in self.positions:
                        if self.turn ^ (self.positions[str(move.tolist())] == 'b'):
                            possible_moves.append(move)
                            break
                        else:
                            break
                    possible_moves.append(move)
        else:
            for move in moves:
                if str(move.tolist()) in self.positions and not self.turn ^ (self.positions[str(move.tolist())] == 'b'):
                    continue
                possible_moves.append(move)
        possible_moves = np.array(possible_moves)

        # Limit moves to board boundaries
        possible_moves = possible_moves[np.where(
            np.apply_along_axis(
                lambda a: (all(a >= 0)) & (
                    a[0] < self.size[0]) & (a[1] < self.size[1]),
                1, possible_moves
            )
        )]

        self.possible_moves_dict[str_piece] = possible_moves
        return possible_moves


if __name__ == '__main__':
    game = board()
    print(game)
    print(game.possible_moves('1N'))
