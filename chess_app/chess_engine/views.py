from typing import List
import chess
import chess.svg as svg
import traceback

from django.http import HttpRequest
from django.shortcuts import render
from functools import reduce

from chess_engine.models import Game, InitPlayer, AI_LIST, GameRepository

# TODO: when two AI are selected, press a button for fast forward that plays a move every 0.5s

GAME_REPO: GameRepository = GameRepository()

def game_history():
    res = []
    for game in GAME_REPO.game_history:
        res.append((game.headers["White"], game.headers["Black"], game.headers["Result"]))
    return res

def move_stack(moves: List[chess.Move]): # change from list of move to list of (turn number, white move, black move)
    move_stack = []
    for i in range(int(len(moves)/2)+1):
        move_stack.append((
            "{}. ".format(i+1),
            moves[i*2] if len(moves) > i*2 else "",
            moves[1+i*2] if len(moves) > 1+i*2 else ""
        ))
    return move_stack

def base_game_res(game: Game):
    draw = game.isDraw()
    return {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": move_stack(game.getHistory()),
        "draw": draw[0],
        "draw_reason": draw[1],
        "win": game.isCheckmate(),
        "both_ai": reduce(lambda x, y: x.is_ai and y.is_ai, game.players.values())
    }

def roll_out():
    game: Game = GAME_REPO.current_game
    res = {}
    while not (game.isCheckmate() or game.isDraw()[0]):
        res = _ais(game)
    return res

################### views ###################

def index(request):
    return render(request, "chess_engine/index.html", {
        "ais": AI_LIST.keys(),
        "error_message": "",
        "games": game_history()
    })

def createGame(request: HttpRequest):
    wname = request.POST.get("wname")
    bname = request.POST.get("bname")
    wis_ai = request.POST.get("wis_ai")
    bis_ai = request.POST.get("bis_ai")
    ai = lambda x : x == 'AI' 

    black = InitPlayer(bname, ai(bis_ai))
    white = InitPlayer(wname, ai(wis_ai))
    try:
        game = Game(black, white)
    except Exception as err:
        traceback.print_exc()

        return render(request, "chess_engine/index.html", {
        "ais": AI_LIST.keys(),
        "error_message": "{} ne correspond a aucune IA".format(err)
    })

    GAME_REPO.setCurrentGame(game)
    return render(request, "chess_engine/game.html", {
        **base_game_res(game),
        "error_message": "",
        })

def play(request: HttpRequest):
    move = request.POST.get("move")
    game = GAME_REPO.current_game
    roll = request.POST.get("roll")

    results = {}
    if roll == 'roll':
        results = roll_out()

    elif game.isCheckmate() or game.isDraw()[0]:
        results = {
        **base_game_res(game),
        "error_message": "",
        }
    else:
        if game.players[game.currentColor()].is_ai:
            results = _ais(game)
        else:
            results = _player(move, game)
        
    if results["win"] or results["draw"]: # game ended
        results["current"] = game.players[not game.board.turn]
        GAME_REPO.pushHistory()
    
    return render(request, "chess_engine/game.html", results)

def _player(move: str | None, game: Game):  
    error_message = ""
    if move is None:
        error_message = "no move present"
    else:
        try:
            uci_move = chess.Move.from_uci(move)
            if uci_move in game.legalMoves():
                game.play(uci_move)
            else:
                raise Exception("Illegal Move among {}".format([x.uci() for x in game.legalMoves()]))
        except Exception as err:
            error_message = err
            traceback.print_exc()
    return {
        **base_game_res(game),
        "error_message": error_message,
        }

def _ais(game: Game):
    # player is an AI
    move = game.players[game.currentColor()].makeMove(game.board)
    game.play(move)
    return {
        **base_game_res(game),
        "error_message": "",
        }

def review(request: HttpRequest, id: int, move: int):
    print(GAME_REPO.game_history)
    print("review: id ", id, "/", len(GAME_REPO.game_history), " move ", move)
    game = GAME_REPO.game_history[id]
    board = game.board()
    mainline = list(game.mainline_moves())
    print("main line", mainline)
    for i in range(move+1):
        board.push(mainline[i])

    return render(request, "chess_engine/game_view.html", {
        "image": svg.board(
            board,
            lastmove=board.peek() if len(board.move_stack) > 0 else None
        ),
        "history": move_stack(list(game.mainline_moves())),
        "white": game.headers["White"],
        "black": game.headers["Black"],
        "game_id": id,
        "prev": max(0, move-1),
        "next": min(len(list(game.mainline_moves()))-1, move+1),
        "move": move
    })