import random
from chess import Move
import chess
from chess_engine.models.base import InitPlayer, AI

class RandomAI(AI): 
    def __init__(self, player: InitPlayer) -> None:
        super().__init__(player)
    
    def makeMove(self, board: chess.Board) -> Move:
        moves = list(board.legal_moves)
        if len(moves) == 0:
            raise Exception("there are no moves")
        if len(moves) == 1:
            return moves[0]
        
        move = random.randint(0, len(moves)-1)
        return moves[move]
    
    def __str__(self) -> str:
        return "[name: {}, class: RandomAI]".format(self.name)