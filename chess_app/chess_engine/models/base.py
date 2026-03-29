import abc
import chess

class InitPlayer:
    def __init__(self, name: str, is_ai: bool = False) -> None:
        self.name = name
        self.is_ai = is_ai

class Player:
    def __init__(self, player: InitPlayer) -> None:
        super().__init__()
        self.name = player.name
        self.is_ai = player.is_ai

class Heuristic(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, board: chess.Board) -> float:
        pass

    def __call__(self, board: chess.Board) -> float:
        return self.evaluate(board)

class AI(Player, abc.ABC):
    def __init__(self, player: InitPlayer) -> None:
        Player.__init__(self, player)
        abc.ABC.__init__(self)
    
    @abc.abstractmethod
    def makeMove(self, board: chess.Board) -> chess.Move:
        pass
