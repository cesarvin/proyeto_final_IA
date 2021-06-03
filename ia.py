import time
import math
#from piece import Piece

class Agent():

    def __init__(self, board):
        self.board = board
        pass 
    
    def minimax(self, depth, time_limit, board, alpha=float("-inf"), beta=float("inf"), maximizing=True):
        node_option = None
        
        # valida que no haya llegado al ultimo nivel de profundidad, que se haya cumplido el tiempo o que haya un ganador.
        if depth == 0 or time.time() > time_limit or self.board.get_winner(board):
            return self.eval_fun(2, board), None

        # obtiene los posibles movimientos según se este maximizando o minimizando
        if maximizing:

            # como maximiza se setea el valor del nodo a menos infinito, mientras no se ha evaluado el nodo.
            node_value = float("-inf")
            # obtiene los posibles movimientos del jugador (maximiza para las negras)
            possible_moves = self.get_possible_moves(2, board)
        else:

            # como miminiza se setea el valor del nodo con infinito, mientras no se ha evaluado el nodo.
            node_value = float("inf")
            # obtiene los posibles movimientos del jugador (minimiza para las blancas)
            possible_moves = self.get_possible_moves(1, board)

        # Se recorren los posibles movimientos para calcular las jugadas.
        for move in possible_moves:
            for to in move[1]:

                # retorna el valor si ya se cumplió el tiempo
                if time.time() > time_limit:
                    return node_value, node_option

                # simula el movimiento
                piece = move[0].piece
                move[0].piece = 0
                to.piece = piece

                # llamada recursiva de la función MINMAX para minimizar la jugada del oponente. 
                val, mov = self.minimax(depth - 1, time_limit, board, alpha, beta, not maximizing)

                # regresa el movimiento luego de haber sido evaluado
                to.piece = 0    
                move[0].piece = piece

                # evalua el valor del modo, si el valor es mayor que el valor actual para tomar la mejor jugada
                if maximizing and val > node_value:
                    node_value = val
                    node_option = (move[0].pos, to.pos)
                    alpha = max(alpha, val)

                    # evalua el valor del modo, si el valor es menor que el valor actual para tomar la mejor jugada
                if not maximizing and val < node_value:
                    node_value = val
                    node_option = (move[0].pos, to.pos)
                    beta = min(beta, val)

                # alpha beta pruning para descartar nodos descartados porque ya hay un mejor valor.
                if beta <= alpha:
                    return node_value, node_option

        #retorna la mejor jugada que fue evaluada, y el valor que obtuvo el nodo
        return node_value, node_option
      


    def eval_fun(self, piece, board):

        result = 0
        # se obtienen los lugares finales para las piezas blancas y negras
        black_home = self.board.get_black_home(board)
        withe_home = self.board.get_white_home(board)

        # se recorre todo el tablero buscando piezas para evaluar la distancia que hay entre la pieza y la meta y obtener un valor max o min
        for col in range(10):
            for row in range(10):
                
                # si las piezas son blancas se maximiza la distancia para obtener el mejor resultado
                if board[row][col].piece == 1:
                    d = [math.sqrt((end.pos[0] - row)**2 + (end.pos[1] - col)**2) for end in black_home if end.piece != 1]
                    if len(d):
                        result -= max(d)
                    else:
                        result -= -100    
                
                # si las piezas son negras se minimiza la distancia para obtener el mejor resultado
                if board[row][col].piece == 2:
                    d = [math.sqrt((end.pos[0] - row)**2 + (end.pos[1] - col)**2) for end in withe_home if end.piece != 2]
                    if len(d):
                        result += min(d)
                    else:
                        result += -100    
                    
        if piece == 2:
            result *= -1

        return result

    
    def get_possible_moves(self, player, board) :
        moves = [] 
        # se recorre todo el tablero para ubicar todas las piezas del jugador
        for col in range(10):
            for row in range(10):
                # si en la posicion del tablero encuentra una pieza del jugador determina todas los posibles saltos que puede dar
                if board[row][col].piece == player:
                    moves.append([board[row][col], self.possible_moves(row,col, board)])

        return moves


    def possible_moves(self, row, col, board, new_mov=None, first_salt=True):
        
        if new_mov is None:
            new_mov = []

        # para una pieza especifica se calculan los saltos que esta puede dar
        for i in range(-1, 2):
            for j in range(-1, 2):
                
                # se determina si la casilla a donde se quiera saltar no sea la casilla desde donde se quiere saltar
                if ((row + j) != row and (col + i) != col):
                    new_row = row + j
                    new_col = col + i

                    # se valida que la posicion hasta donde quiera llegar esta dentro del tablero de 10x10
                    if (self.board.valid_board_position(new_row, new_col) == True):
                        # si la casilla esta libre salta
                        if board[new_row][new_col].piece == 0:  
                            # solo se permite mover a una casilla en blanco con un primer salto
                            if (first_salt == True):
                                new_mov.append(board[new_row][new_col])
                        
                        else: 
                            # si la casilla no está libre entonces evalua la casilla posterior para saltar la pieza                               
                            if (self.board.valid_board_position(new_row + j, new_col + i) == True):
                                # comprueba que no haya sido ingresado el destino para no duplicar posibles lugares a ocupar
                                if not (board[new_row + j][new_col + i] in new_mov):
                                    # si la siguiente casilla a una ocupada esta libre hace un salto
                                    if board[new_row + j][new_col + i].piece == 0:
                                        new_mov.insert(0, board[new_row + j][new_col + i])  

                                        # se evalúa recursivamente si puede saltar otra pieza
                                        self.possible_moves(board[new_row + j][new_col + i].pos[0], board[new_row + j][new_col + i].pos[1], board, new_mov, False)
        return new_mov

    