import numpy as np
# from piece import Piece

class Board():

    def __init__(self):
        pass


    def get_board(self):
        # se crea un tablero de 10x10, a cada tablero se le asigna una pieza inicial
        
        board = [[None] * 10 for _ in range(10)]
        for row in range(10):
            for col in range(10):
                pos = (row, col)

                # valores iniciales cuando se crea la pieza
                if row + col < 5:
                    piece = 2    
                elif row + col > 13:
                    piece = 1
                else:
                    piece = 0
                
                board[row][col] = type('Piece', (object,),{'pos': pos, 'piece': piece})()#Piece(row, col)  # la pieza puede ser blanca, negra, o ninguna
                
        return board


    def get_black_home(self, board):
        # retorna las posiciones en el tablero en donde se inician las piezas negras
        return [element for row in board
                    for element in row if element.piece == 2]


    def get_white_home(self, board):
        # retorna las posiciones en el tablero en donde se inician las piezas blancas
        return [element for row in board
                    for element in row if element.piece == 1]


    def get_piece(self, row, col, board):
        # retorna una pieza del tablero.
        return board[row][col]


    def draw_board(self, board):
        # dibuja el tablero en consola
        for i in range(0, 10):
            for j in range(0, 10):
                p = board[i][j].piece
                if (p ==1 or p ==2):
                    print('{}|'.format('w' if (board[i][j].piece == 1) else 'b'), end=" ")
                else: 
                    print('{}|'.format(' '), end=" ")
            print()
        print()


    def get_winner(self, board):
        # obtiene las posiciones iniciales de las piezas blancas que sirven para comprobar si ya las ocupo el equipo contrario
        black_home = self.get_black_home(board)
        withe_home = self.get_white_home(board)
        # valida que no haya ganador
        if all(win.piece == 1 for win in black_home):
            return 1
        elif all(win.piece == 2 for win in withe_home):
            return 2
        else:
            return None


    def valid_board_position(self, row, col):
        # retorna si la posición row,col estan dentro de la matriz del tablero
        return (False) if (row < 0 or row > 9 or col < 0  or col > 9) else True
