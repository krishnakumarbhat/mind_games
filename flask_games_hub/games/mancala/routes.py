from flask import Blueprint, redirect, render_template, request, session, url_for

from games.mancala.engine import (
    AI_PITS,
    AI_STORE,
    HUMAN_PITS,
    HUMAN_STORE,
    apply_move,
    choose_ai_move,
    initial_board,
    legal_moves,
    winner,
)

mancala_bp = Blueprint("mancala", __name__, url_prefix="/games/mancala")


def _get_state():
    state = session.get("mancala_state")
    if state:
        return state
    state = {
        "board": initial_board(),
        "turn": "human",
        "message": "Your turn.",
        "game_over": False,
    }
    session["mancala_state"] = state
    return state


def _save_state(state):
    session["mancala_state"] = state
    session.modified = True


def _is_game_over(board):
    return all(board[p] == 0 for p in HUMAN_PITS) or all(board[p] == 0 for p in AI_PITS)


@mancala_bp.route("/", methods=["GET", "POST"])
def play_mancala():
    state = _get_state()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "new":
            state = {
                "board": initial_board(),
                "turn": "human",
                "message": "New game started. Your turn.",
                "game_over": False,
            }
            _save_state(state)
            return redirect(url_for("mancala.play_mancala"))

        if action == "move" and not state["game_over"] and state["turn"] == "human":
            try:
                pit = int(request.form.get("pit", "-1"))
            except ValueError:
                pit = -1

            if pit not in legal_moves(state["board"], "human"):
                state["message"] = "Invalid move. Choose a non-empty pit on your side."
                _save_state(state)
                return redirect(url_for("mancala.play_mancala"))

            state["board"], human_extra = apply_move(state["board"], pit, "human")

            if _is_game_over(state["board"]):
                state["game_over"] = True
                state["message"] = f"Game over: {winner(state['board'])} wins."
                _save_state(state)
                return redirect(url_for("mancala.play_mancala"))

            if human_extra:
                state["message"] = "You got an extra turn."
                _save_state(state)
                return redirect(url_for("mancala.play_mancala"))

            state["turn"] = "ai"

            while state["turn"] == "ai" and not state["game_over"]:
                ai_move = choose_ai_move(state["board"])
                if ai_move is None:
                    state["game_over"] = True
                    state["message"] = f"Game over: {winner(state['board'])} wins."
                    break

                state["board"], ai_extra = apply_move(state["board"], ai_move, "ai")

                if _is_game_over(state["board"]):
                    state["game_over"] = True
                    state["message"] = f"Game over: {winner(state['board'])} wins."
                    break

                if not ai_extra:
                    state["turn"] = "human"
                    state["message"] = "Your turn."

            _save_state(state)
            return redirect(url_for("mancala.play_mancala"))

    return render_template(
        "mancala.html",
        state=state,
        human_pits=HUMAN_PITS,
        ai_pits=AI_PITS,
        human_store=HUMAN_STORE,
        ai_store=AI_STORE,
        legal_human_moves=legal_moves(state["board"], "human") if not state["game_over"] else [],
    )
