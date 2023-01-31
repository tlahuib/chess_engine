import numpy as np
import re


class piece:
    def __init__(self, position: np.array, color: bool):
        self.name = ''
        self.position = position
        self.color = color  # white = False, black = True
        self.moves = np.array([[0, 0]])
        self.possible_moves = position


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
        front = 1
        if color: front = -1
        self.moves = np.array([
            [[0, front], [0, 2 * front]]
        ])


class pawn(piece):
    def __init__(self, position: np.array, color: bool):
        super().__init__(position, color)
        front = 1
        if color: front = -1
        self.moves = np.array([
            [[0, front]]
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
        # TODO:
        #   - Castle
        #   - Restrict movement in check
        if str_piece in set(self.possible_moves_dict.keys()):
            return self.possible_moves_dict[str_piece]

        # Get piece from correct color
        try:
            if self.turn:
                piece2move = self.black[str_piece]
                opponent = self.white
                front = -1
            else:
                piece2move = self.white[str_piece]
                opponent = self.black
                front = 1
        except KeyError:
            print(f'Piece {str_piece} not found on the board')
        piece_name = piece2move.__class__.__name__

        # Account for piece blocking
        moves = piece2move.moves + piece2move.position
        possible_moves = []
        if piece_name != 'knight':
            for direction in moves:
                for move in direction.tolist():
                    if str(move) in self.positions:
                        if self.turn ^ (self.positions[str(move)] == 'b'):
                            possible_moves.append(move)
                            break
                        else:
                            break
                    possible_moves.append(move)
        else:
            for move in moves.tolist():
                if str(move) in self.positions and not self.turn ^ (self.positions[str(move)] == 'b'):
                    continue
                possible_moves.append(move)

        # Special moves
        if piece_name in {'initial_pawn', 'pawn'}:
            # Capture Diagonally
            captures = set(self.positions.keys()).intersection(
                    {str(item) for item in ([[1, front], [-1, front]] + piece2move.position).tolist()}
            )
            captures = [[int(n) for n in re.sub('[\[\]]', '', item).split(', ')] for item in captures]
            if captures: possible_moves += captures

            # Can't capture directly in front
            front_move = (piece2move.position + [0, front]).tolist()
            if str(front_move) in self.positions: 
                possible_moves = [item for item in possible_moves if item != front_move]

            # En Passant
            try:
                if (self.en_passant[1] - piece2move.position).tolist() in [[-1, front], [1, front]]:
                    possible_moves.append(self.en_passant[1].tolist())
            except AttributeError:
                pass



        # Limit moves to board boundaries
        possible_moves = np.array(possible_moves)
        possible_moves = possible_moves[np.where(
            np.apply_along_axis(
                lambda a: (all(a >= 0)) & (
                    a[0] < self.size[0]) & (a[1] < self.size[1]),
                1, possible_moves
            )
        )]

        self.possible_moves_dict[str_piece] = possible_moves
        return possible_moves


    def move_piece(self, str_piece: str, move: list):
        if move in self.possible_moves(str_piece).tolist():
            if self.turn:
                color = self.black
                opponent = self.white
                prefix = 'b'
                front = -1
            else:
                color = self.white
                opponent = self.black
                prefix = 'w'
                front = 1

            # Delete piece if captured
            if str(move) in self.positions:
                opponent.pop(self.positions[str(move)][1:])
            try:
                if move == self.en_passant[1].tolist():
                    self.positions.pop(str(opponent[self.en_passant[0]].position.tolist()))
                    opponent.pop(self.en_passant[0])
            except AttributeError:
                pass

            # Update pieces with special moves
            try:
                del self.en_passant
            except AttributeError:
                pass
            if color[str_piece].__class__.__name__ == 'initial_pawn':
                color[str_piece] = pawn(color[str_piece].position, color[str_piece].color)
                if abs(move[1] - color[str_piece].position[1]) == 2: 
                    self.en_passant = [str_piece, np.array([move[0], move[1] - front])]
            
            # Update position in board
            self.positions.pop(str(color[str_piece].position.tolist()))
            self.positions[str(move)] = prefix + str_piece

            # Update position in piece
            color[str_piece].position = np.array(move)

            # Update board turns
            self.turn = ~ self.turn
            self.possible_moves_dict = {}


if __name__ == '__main__':
    game = board()
    game.move_piece('3p', [2, 3])
    game.move_piece('2p', [1, 4])
    game.move_piece('2p', [1, 3])
    game.move_piece('2p', [2, 3])
    game.move_piece('2p', [1, 4])
    game.move_piece('1p', [0, 4])
    game.move_piece('2p', [0, 5])
    # print(game.possible_moves('2p'))
    print(game)
