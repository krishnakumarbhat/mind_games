GAMES = [
    {"slug": "checkers", "name": "Checkers (Draughts)", "implemented": True, "route": "checkers.play_checkers"},
    {"slug": "backgammon", "name": "Backgammon", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "chess", "name": "Chess", "implemented": True, "route": "chess.play_chess"},
    {"slug": "go", "name": "Go (Weiqi/Baduk)", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "mancala", "name": "Mancala", "implemented": True, "route": "mancala.play_mancala"},
    {"slug": "2048", "name": "2048 (and 1024)", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "threes", "name": "Threes!", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "sudoku", "name": "Sudoku", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "minesweeper", "name": "Minesweeper", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "rubiks-cube", "name": "Rubik’s Cube", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "hive", "name": "Hive", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "santorini", "name": "Santorini", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "onitama", "name": "Onitama", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "yinsh-dvonn", "name": "YINSH / DVONN", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "azul", "name": "Azul", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "arimaa", "name": "Arimaa", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "diplomacy", "name": "Diplomacy", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "gin-rummy", "name": "Gin Rummy", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "canasta", "name": "Canasta", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "mahjong-card", "name": "Mahjong (Card Version)", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "poker-texas-holdem", "name": "Poker (Texas Hold'em)", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "teen-patti", "name": "Teen Patti", "implemented": True, "route": "lite.play_lite_game"},
    {"slug": "cheat", "name": "Cheat (Bullsh*t / I Doubt It)", "implemented": True, "route": "lite.play_lite_game"},
]


GAME_MAP = {game["slug"]: game for game in GAMES}
