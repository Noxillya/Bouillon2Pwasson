from chess import Move
import chess
from dataclasses import dataclass
from chess_engine.models.ai_algorithm.pieceCountH import PieceCountH
from chess_engine.models.base import InitPlayer, AI, Heuristic
import chess.polyglot


@dataclass
class LookupEntry:
    depth: int
    score: float

class Bouillon2Pwasson(AI):
    def __init__(self, player: InitPlayer, heuristic: Heuristic | None = None, depth: int = 3) -> None:
        super().__init__(player)
        self.heuristic = heuristic if heuristic is not None else PieceCountH()  
        self.depth = depth
        self.lookup_table: dict[tuple[str, chess.Color], LookupEntry] = {}

    def _lookup_key(self, position: chess.Board, player: chess.Color) -> tuple[str, chess.Color]:

        return (position.fen(), player)

    def _store_lookup(self, key: tuple[str, chess.Color], depth: int, score: float) -> None:
        existing = self.lookup_table.get(key)
        if existing is None or depth >= existing.depth:
            self.lookup_table[key] = LookupEntry(depth=depth, score=score)

    def _evaluate_for_player(self, position: chess.Board, heuristic: Heuristic, player: chess.Color) -> float:
        if position.is_checkmate():
            return -float("inf") if position.turn == player else float("inf")

        if position.is_stalemate() or position.is_insufficient_material() or position.is_seventyfive_moves() or position.is_fivefold_repetition():
            return 0.0

        score = heuristic(position)

        if position.turn == player:
            score = -score
        return score

    def minmax(
        self,
        position: chess.Board,
        depth: int,
        heuristic: Heuristic,
        player: chess.Color,
        alpha: float = -float("inf"),
        beta: float = float("inf"),
    ) -> float:
        lookup_key = self._lookup_key(position, player)
        cached_entry = self.lookup_table.get(lookup_key)
        if cached_entry is not None and cached_entry.depth >= depth:
            return cached_entry.score

        if depth == 0 or position.is_game_over(claim_draw=True):
            score = self._evaluate_for_player(position, heuristic, player)
            self._store_lookup(lookup_key, depth, score)
            return score

        legal_moves = list(position.legal_moves)
        if len(legal_moves) == 0:
            score = self._evaluate_for_player(position, heuristic, player)
            self._store_lookup(lookup_key, depth, score)
            return score

        maximizing = position.turn == player
        best_score = -float("inf") if maximizing else float("inf")
        pruned = False

        for move in legal_moves:
            position.push(move)
            child_score = self.minmax(position, depth - 1, heuristic, player, alpha, beta)
            position.pop()

            if maximizing:
                best_score = max(best_score, child_score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, child_score)
                beta = min(beta, best_score)

            if beta <= alpha:
                pruned = True
                break

        if not pruned:
            self._store_lookup(lookup_key, depth, best_score)
        return best_score

    
    def makeMove(self, board: chess.Board) -> Move:
        """ 
        Utilisation du book "Cerebellum3Merge.bin" contenant des ouvertures théoriques
        Semble réaliser des coups théoriques, jusqu'au moment ou l'adversaire joue un coup hors théorie
        Semble vouloir réaliser des coups illégaux par moments
        """
    
        try:
            with chess.polyglot.open_reader("Cerebellum3Merge.bin") as reader:
                entry = reader.weighted_choice(board)
                return entry.move
        except:
            pass
    
        moves = list(board.legal_moves)
        if not moves:
            raise Exception("there are no moves")
        if len(moves) == 1:
            return moves[0]
        player = board.turn
        best_move = moves[0]
        best_score = -float("inf")

        for move in moves:
            board.push(move)
            score = self.minmax(board, self.depth - 1, self.heuristic, player, best_score, float("inf"))
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def __str__(self) -> str:
        return "[name: {}, class: Bouillon2Pwasson]".format(self.name)