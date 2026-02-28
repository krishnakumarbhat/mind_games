from flask import Blueprint, redirect, render_template, request, session, url_for

from games.checkers.engine import apply_move, choose_ai_move, initial_board, legal_moves, winner

checkers_bp = Blueprint("checkers", __name__, url_prefix="/games/checkers")


def _get_state():
    state = session.get("checkers_state")
    if state:
        return state
    state = {
        "board": initial_board(),
        "turn": "human",
        "message": "Your turn.",
        "game_over": False,
    }
    session["checkers_state"] = state
    return state


def _save_state(state):
    session["checkers_state"] = state
    session.modified = True


@checkers_bp.route("/", methods=["GET", "POST"])
def play_checkers():
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
            return redirect(url_for("checkers.play_checkers"))

        if not state["game_over"] and state["turn"] == "human" and action == "move":
            legal = legal_moves(state["board"], "human")
            try:
                move_index = int(request.form.get("move_index", "-1"))
            except ValueError:
                move_index = -1

            if 0 <= move_index < len(legal):
                selected = legal[move_index]
                state["board"] = apply_move(state["board"], selected)
                won = winner(state["board"])

                if won:
                    state["message"] = f"Game over: {won} wins."
                    state["game_over"] = True
                    _save_state(state)
                    return redirect(url_for("checkers.play_checkers"))

                ai_move = choose_ai_move(state["board"])
                if ai_move:
                    state["board"] = apply_move(state["board"], ai_move)

                won = winner(state["board"])
                if won:
                    state["message"] = f"Game over: {won} wins."
                    state["game_over"] = True
                else:
                    state["message"] = "Your turn."
            else:
                state["message"] = "Invalid move. Please pick a move from the list."

            _save_state(state)
            return redirect(url_for("checkers.play_checkers"))

    legal = legal_moves(state["board"], "human") if not state["game_over"] else []

    return render_template(
        "checkers.html",
        state=state,
        legal=legal,
    )
