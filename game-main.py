#
# Juego Hoopers
# César Rodas 16776
# 

# from piece import Piece
from board import *
from ia import *

class Hoopers():

    def __init__(self):

        # tiempo limite y profundidad
        self.time_limit = 30
        self.depth = 3

        # se carga el tablero y el agente para jugar
        self.b = Board()
        self.ia = Agent(self.b)

        # se crea un tablero inicial y se establece que las blancas inician
        self.board = self.b.get_board()
        self.current_player = 1 #blancas inician

        # se obtienen las posiciones iniciales para blancas y negras
        self.black_home = self.b.get_black_home(self.board)
        self.withe_home = self.b.get_white_home(self.board)

        print("\n\nInician las blancas\n\n")
        

    def play_hooper(self):
        play_game = True

        # ciclo que mantiene el juego activo, se realiza una movida el jugador y una la computadora.
        while play_game:

            # dibuja en pantalla y obtiene un ganador para terminar el ciclo
            self.b.draw_board(self.board)
            self.result = self.b.get_winner(self.board)
            
            if (self.b.get_winner(self.board) == 1):
                print("\nJuego Terminado, blancas ganan)")
                break
            
            if (self.b.get_winner(self.board) == 2):
                print("\nJuego Terminado, negras ganan)")
                break
            
            # si el turno es de las blancas entonces solicita que se ingresen las posiciones desde y hasta donde se movera una pieza
            if self.current_player == 1:
                    is_move = True
                    while (is_move):
                        
                        mi = input ("Mover desde (fila, columna): \n")
                        if (mi == 't'):
                            play_game = False
                            break   
                        mf = input ("Mover hasta (fila, columna): \n")
                        if (mf == 't'):
                            play_game = False
                            break   
                        
                        mix, miy = mi.split(',')
                        mfx, mfy = mf.split(',')

                        pi = (int(mix)-1, int(miy)-1)
                        pf = (int(mfx)-1, int(mfy)-1)
                                                
                        # se mueve la pieza
                        if (self.manual_move(pi,pf) == True):
                            is_move = False
                        
                        # se establece el turno para el oponente
                        self.current_player = 2
                        print()

            else:

                # si el turno es de las negras entonces el agente de IA hace el movimiento
                print('Turno de la compu, espere...')
                self.agent_move()
                # se establece el turno para el oponente
                self.current_player = 1


    def manual_move(self, A, B):
        
        # obtiene las posiciones que seran intercambiadas
        curr_pos = self.b.get_piece(A[0], A[1], self.board)
        final_pos = self.b.get_piece(B[0], B[1], self.board)    
        
        # valida que se seleccione una ficha y que la casilla final este libre
        if curr_pos.piece == 0 or final_pos.piece != 0:
            print("\nMovimiento incorrecto\n")
            return False

        # mueve la ficha
        final_pos.piece = curr_pos.piece
        curr_pos.piece = 0
        return True

    
    def agent_move(self):

        # se obtiene el tiempo limite
        time_to_move = time.time() + self.time_limit

        # se obtiene el mejor movimiento evaluando con MINIMAX
        val , best_move = self.ia.minimax(self.depth, time_to_move, self.board)

        print("Movimiento calculado")
        
        # se obtiene el mejor movimiento
        mi = (best_move[0][0],best_move[0][1])
        mf = (best_move[1][0],best_move[1][1])

        # se mueve la pieza
        self.manual_move(mi, mf)
        print("Movimiento de la computadora (fila, columna) desde " 
                +  str((mi[0] + 1, mi[1] + 1)) + ' hasta ' 
                +  str((mf[0] + 1, mf[1] + 1)))
        print()    


if __name__ == "__main__":
    game = Hoopers()
    game.play_hooper() # inicia el juego
