# Flask Mind Games Hub

Flask web app with a game selector where you can choose a game and play with the computer.

## Implemented and playable

- Checkers (Draughts) vs Computer (full app mode)
- Mancala vs Computer (full app mode)
- Backgammon (lite mode)
- Chess (proper rules + board GUI)
- Go (lite mode)
- 2048 (lite mode)
- Threes! (lite mode)
- Sudoku (lite mode)
- Minesweeper (lite mode)
- Rubik's Cube (lite mode)
- Hive (lite mode)
- Santorini (lite mode)
- Onitama (lite mode)
- YINSH / DVONN (lite mode)
- Azul (lite mode)
- Arimaa (lite mode)
- Diplomacy (lite mode)
- Gin Rummy (lite mode)
- Canasta (lite mode)
- Mahjong (Card Version) (lite mode)
- Poker (Texas Hold'em) (lite mode)
- Teen Patti (lite mode)
- Cheat (Bullsh*t / I Doubt It) (lite mode)

All game folders are separate under `games/`.

### Lite GUI notes

- Chess now uses proper legal rules (check/checkmate/stalemate) with a dedicated board GUI.
- Go and all other duel-lite games use a visible click-to-place board GUI.
- In duel-lite games: choose a move style, then click an empty board cell.
- Card/sliding/puzzle lite games have their own visual UIs as well.

## Run locally

```bash
cd flask_games_hub
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open: http://127.0.0.1:5000
