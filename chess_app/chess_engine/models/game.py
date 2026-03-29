import chess
import chess.svg

from chess import Move
from chess_engine.models.base import InitPlayer, Player
from chess_engine.models.ai_list import AI_LIST
from chess_engine.models.ai_algorithm.pieceCountH import PieceCountH

AI_PARAMS = {
    "b2p": {
        "heuristic": PieceCountH(),
        "depth": 5
    },
    "random": {}
}


class Game:
    def __init__(self, black: InitPlayer, white: InitPlayer) -> None:
        create = lambda p : self._createPlayer(p) if not p.is_ai else self._createAI(p, AI_PARAMS[p.name])

        self.players = {
            chess.BLACK: create(black),
            chess.WHITE: create(white)
        }
        
        self.board = chess.Board()

    def _createPlayer(self, player: InitPlayer) -> Player :
        return Player(player)
    
    def _createAI(self, player: InitPlayer, params) -> Player:
        ai = AI_LIST[player.name](player, **params)
        return ai

    def legalMoves(self) -> list[Move]:
        return list(self.board.legal_moves)
    
    def isCheckmate(self) -> bool:
        return self.board.is_checkmate()
    
    def isDraw(self) -> tuple[bool,str]:
        if self.board.is_insufficient_material():
            return (True, "Insufficient material")
        if self.board.is_stalemate():
            return (True, "Stalemate")
        if self.board.is_seventyfive_moves():
            return True, "75 moves without a pawn move or capture"
        if self.board.is_fivefold_repetition():
            return True, "5 fold repetition of the position"

        return (False, "")
    
    def currentColor(self) -> chess.Color:
        return self.board.turn
    
    def getHistory(self) -> list[Move] :
        return self.board.move_stack
    
    def getBoardImage(self) -> str:
        return chess.svg.board(
            self.board,
            lastmove= self.board.peek() if len(self.board.move_stack) > 0 else None
        )
    
    def play(self, move: Move):
        self.board.push(move)
    
    def gameResultString(self):
        if self.board.is_game_over(claim_draw=True):
            res = ""
            if self.isDraw()[0]:
                return "1/2-1/2"
            if self.board.turn:
                return "0-1"
            else:
                return "1-0"
        else:
            raise Exception("game not finished, impossible to generate result string")
