# ChessProject

This is a project for developping an IA for chess.
It is based on the python library [python-chess]{https://python-chess.readthedocs.io/en/latest/} for the chess engine.

It relies on [django]{https://www.djangoproject.com/} for the interface part so it is easy to interact with the engine.

## Python-chess

- create the board:
  `chess.Board()`
- obtain the list of legal moves:
  `board.legal_moves` returns an iterator of legal moves in SAN standard notation
- make a move:
  `board.push("e4")` handle white and black's turn inside the board
- check if it is checkmate, stalemate, draws:
  `board.is_checkmate()`
  `board.is_stalemate()`
  `board.is_insufficient_material()`
  `board.is_five_fold_repetition()`
  `board.is_seventyfive_moves()`
- check for checks and attacks:
  `board.is_check()`
  `board.attacks(chess.E8)` return the set of squares that the given square attacks
  `board.is_attacked_by(chess.WHITE, chess.E8)` check if the given side attacks the given square
  `board.attackers(chess.WHITE, chess.F3)` get the set of squares that attacks the given square
- read and write Portable Game Notation
  ```python
  import chess.pgn
  with open("data/pgn/molinari-bordais-1979.pgn") as pgn:
      first game = chess.pgn.read_game(pgn)
  white = first_game.headers["White"]   # 'Molinari'
  black = first_game.headers["Black"]   # 'Bordais'
  gameline = first_game.mainline()      # (1. e4 c5 2. c4 Nc6 ... 5. g3 Nd3#)
  result = first_game.headers["Result"] # '0-1'
  ```
- image rendering:

  ```python
  import chess
  import chess.svg

  board = chess.Board("8/8/8/8/4N3/8/8/8 w - - 0 1") # declare a board with 4 empty row, 4 empty squares, a knight, ...
  chess.svg.board(
      board,
      fill=dict.fromkey(board.attacks(chess.E4), "#cc0000cc"), # color in red the squares attacked by the piece in E4
      arrows=[chess.svg.Arrow(chess.E4, chess.F6), color="#0000cccc"], # color in blue an arrow from E4 to F6
      size=350, # the size of the image
  )
  ```

## Django

- run the server
  `python manage.py runserver`

## The interface

The interface first asks yo to create a game and to chose the opponents

## Composing your own AI

Your ai must implement the AI abstract class and you must update the AI_LIST constant in the `chess_engine/models/ai_list.py` file.
