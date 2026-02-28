from flask import Flask, render_template

from games.catalog import GAMES
from games.chess.routes import chess_bp
from games.checkers.routes import checkers_bp
from games.lite.routes import lite_bp
from games.mancala.routes import mancala_bp
from games.placeholder.routes import placeholder_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mind-games-dev-secret-key"

    app.register_blueprint(checkers_bp)
    app.register_blueprint(chess_bp)
    app.register_blueprint(mancala_bp)
    app.register_blueprint(lite_bp)
    app.register_blueprint(placeholder_bp)

    @app.get("/")
    def index():
        return render_template("index.html", games=GAMES)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
