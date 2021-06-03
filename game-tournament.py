#
# Juego Hoopers
# César Rodas 16776
# 

# from piece import Piece
from board import *
from ia import *
from xml.dom import minidom
from xml.etree import ElementTree

class HoopersTournament():

    def __init__(self):

        # tiempo limite y profundidad
        self.time_limit = 30
        self.depth = 3

        # se carga el tablero y el agente para jugar
        self.b = Board()
        self.ia = Agent(self.b)

        # se crea un tablero inicial y se establece que las blancas inician
        self.board = self.b.get_board()
        
        # se obtienen las posiciones iniciales para blancas y negras
        self.black_home = self.b.get_black_home(self.board)
        self.withe_home = self.b.get_white_home(self.board)
        
        # TODO: definir quien inicia la partida
        # self.current_player = 1 #blancas inician
    
    
    def other_IA_move(self, A, B):
        
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

    
    def my_agent_move(self):

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
        
        
        # TODO: llamar a la función que envía el xml

    
    def load_move(self, file_name):
        load_xml = minidom.parse(file_name)
        
        from_move = load_xml.getElementsByTagName('from')
        to_move = load_xml.getElementsByTagName('to')
        path = load_xml.getElementsByTagName('pos')

        moves = {}

        moves['from_row'] = from_move[0].attributes['row'].value
        moves['from_col'] = from_move[0].attributes['col'].value

        moves['to_row'] = to_move[0].attributes['row'].value
        moves['to_col'] = to_move[0].attributes['col'].value

        moves['path'] = []

        for elem in path:
            dict = {}
            dict['row'] = elem.attributes['row'].value
            dict['col'] = elem.attributes['col'].value
            moves['path'].append(dict)

        self.other_IA_move(self, moves)


    def make_move(self, A, B, path):
        root = ElementTree.Element('move')

        from_xml = ElementTree.SubElement(root, 'from')
        from_xml.set('row', A[0])
        from_xml.set('col', A[1])

        to_xml = ElementTree.SubElement(root, 'to')
        to_xml.set('row', B[0])
        to_xml.set('col', B[1])

        path_xml = ElementTree.SubElement(root, 'path')

        for jump in path:
            pos = ElementTree.SubElement(path_xml, 'pos')
            pos.set('row', jump['row'])
            pos.set('col', jump['col'])

        my_tree = ElementTree.tostring(root).decode()

        filename = "move.xml"

        my_move = open(filename, "w")
        my_move.write(my_tree)