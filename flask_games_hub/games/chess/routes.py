import chess
from flask import Blueprint, redirect, render_template, request, session, url_for

from games.chess.engine import (
    board_from_fen,
    board_matrix,
    choose_computer_move,
    game_status,
    initial_fen,
    legal_destinations_for_square,
)

chess_bp = Blueprint("chess", __name__, url_prefix="/games/chess")


def _new_state():
    return {
        "fen": initial_fen(),
        "selected": None,
        "legal_destinations": [],
        "message": "Your turn. Select a piece, then select destination.",
        "game_over": False,
    }


def _get_state():
    state = session.get("chess_state")
    if state:
        return state
    state = _new_state()
    session["chess_state"] = state
    return state


def _save_state(state):
    session["chess_state"] = state
    session.modified = True


def _handle_square_click(state, square_name):
    board = board_from_fen(state["fen"])

    if state["game_over"]:
        return state

    selected = state["selected"]

    if selected and square_name in state["legal_destinations"]:
        candidate_moves = []
        for candidate in board.legal_moves:
            from_sq = candidate.from_square
            to_sq = candidate.to_square
            from_name = chess.square_name(from_sq)
            to_name = chess.square_name(to_sq)
            if from_name == selected and to_name == square_name:
                candidate_moves.append(candidate)

        move = None
        for candidate in candidate_moves:
            if candidate.promotion == chess.QUEEN:
                move = candidate
                break
        if move is None and candidate_moves:
            move = candidate_moves[0]

        if move:
            board.push(move)

            status = game_status(board)
            if board.is_game_over():
                state["fen"] = board.fen()
                state["selected"] = None
                state["legal_destinations"] = []
                state["game_over"] = True
                state["message"] = status
                return state

            ai_move = choose_computer_move(board)
            if ai_move:
                board.push(ai_move)

            state["fen"] = board.fen()
            state["selected"] = None
            state["legal_destinations"] = []
            state["message"] = game_status(board)
            state["game_over"] = board.is_game_over()
            return state

    piece = board.piece_at(chess.parse_square(square_name))
    if piece and piece.color:
        destinations = legal_destinations_for_square(board, square_name)
        if destinations:
            state["selected"] = square_name
            state["legal_destinations"] = destinations
            state["message"] = f"Selected {square_name}. Pick destination square."
            return state

    state["selected"] = None
    state["legal_destinations"] = []
    state["message"] = "Invalid selection. Choose one of your pieces with legal moves."
    return state


@chess_bp.route("/", methods=["GET", "POST"])
def play_chess():
    state = _get_state()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "new":
            state = _new_state()
            _save_state(state)
            return redirect(url_for("chess.play_chess"))

        if action == "click":
            square = request.form.get("square")
            if square:
                state = _handle_square_click(state, square)
                _save_state(state)
                return redirect(url_for("chess.play_chess"))

    board = board_from_fen(state["fen"])
    rows = board_matrix(board)

    return render_template(
        "chess.html",
        state=state,
        rows=rows,
    )
