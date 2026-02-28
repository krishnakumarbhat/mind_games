from flask import Blueprint, abort, render_template

from games.catalog import GAME_MAP

placeholder_bp = Blueprint("placeholder", __name__, url_prefix="/games")


@placeholder_bp.get("/<slug>")
def game_placeholder(slug):
    game = GAME_MAP.get(slug)
    if game is None:
        abort(404)

    if game.get("implemented"):
        abort(404)

    return render_template("placeholder.html", game=game)
