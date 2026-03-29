import chess
from chess import Board
from chess_engine.models.base import Heuristic
import chess.polyglot

class PieceCountH(Heuristic):
    def __init__(self) -> None:
        self.pawn_value = 1
        self.rook_value = 5
        self.knigh_value = 3
        self.bishop_value = 3
        self.queen_value = 9
        super().__init__()

    def evaluate(self, board: Board) -> float:
        current_color = board.turn
        value_player = self.pieces_value(board, not current_color) + self.pawn_structure(board, not current_color)
        value_other = self.pieces_value(board, current_color) + self.pawn_structure(board, current_color)
        return value_player - value_other
    
    def pieces_value(self, node: Board, color: chess.Color) -> float:
        nb_pawn = len(node.pieces(chess.PAWN, color))
        nb_rook = len(node.pieces(chess.ROOK, color))
        nb_knight = len(node.pieces(chess.KNIGHT, color))
        nb_bishop = len(node.pieces(chess.BISHOP, color))
        nb_queen = len(node.pieces(chess.QUEEN, color))
        total_player = nb_pawn * self.pawn_value + nb_rook * self.rook_value + nb_knight * self.knigh_value + nb_bishop * self.bishop_value + nb_queen * self.queen_value
        return total_player

    def pawn_structure(self, board: Board, color: chess.Color) -> float:
        pawns = board.pieces(chess.PAWN, color)
        score = 0

        files = [chess.square_file(sq) for sq in pawns]

        for f in files:
            if files.count(f) > 1:
                score -= 0.5

            if (f - 1 not in files) and (f + 1 not in files):
                score -= 0.5

        return score

        
#TODO: ajouter : pièces protégées, pièces attaquées, promotion de pion
