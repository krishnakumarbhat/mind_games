import random
from copy import deepcopy

from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from games.catalog import GAME_MAP

lite_bp = Blueprint("lite", __name__, url_prefix="/games")

SLIDING_GAMES = {"2048": 2048, "threes": 1024}
CARD_GAMES = {
    "gin-rummy",
    "canasta",
    "mahjong-card",
    "poker-texas-holdem",
    "teen-patti",
    "cheat",
}
DUEL_GAMES = {
    "backgammon",
    "chess",
    "go",
    "hive",
    "santorini",
    "onitama",
    "yinsh-dvonn",
    "azul",
    "arimaa",
    "diplomacy",
}
PUZZLE_GAMES = {"sudoku", "minesweeper", "rubiks-cube"}

DUEL_ACTIONS = {
    "backgammon": [("race", 5, 2), ("block", 3, 4), ("double", 7, 1)],
    "chess": [("tactic", 6, 1), ("develop", 4, 2), ("sacrifice", 8, 0)],
    "go": [("influence", 4, 3), ("cut", 6, 1), ("capture", 7, 0)],
    "hive": [("pin", 5, 2), ("swarm", 6, 1), ("queen-step", 7, 0)],
    "santorini": [("build", 4, 3), ("climb", 6, 1), ("god-power", 8, 0)],
    "onitama": [("tiger", 6, 1), ("dragon", 7, 0), ("boar", 4, 2)],
    "yinsh-dvonn": [("ring-flip", 6, 1), ("stack", 5, 2), ("remove", 8, 0)],
    "azul": [("draft", 5, 2), ("pattern", 6, 1), ("deny", 7, 0)],
    "arimaa": [("push", 5, 2), ("pull", 6, 1), ("trap", 8, 0)],
    "diplomacy": [("support", 4, 3), ("convoy", 6, 1), ("betray", 8, 0)],
}

DUEL_BOARD_SIZES = {
    "backgammon": 8,
    "chess": 8,
    "go": 9,
    "hive": 7,
    "santorini": 7,
    "onitama": 7,
    "yinsh-dvonn": 7,
    "azul": 7,
    "arimaa": 8,
    "diplomacy": 8,
}


def _state_key(slug):
    return f"lite_state_{slug}"


def _game_mode(slug):
    if slug in SLIDING_GAMES:
        return "sliding"
    if slug in CARD_GAMES:
        return "cards"
    if slug in DUEL_GAMES:
        return "duel"
    if slug in PUZZLE_GAMES:
        return "puzzle"
    return None


def _new_board(size=4):
    return [[0 for _ in range(size)] for _ in range(size)]


def _empty_cells(board):
    cells = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                cells.append((row, col))
    return cells


def _spawn_2048_tile(board):
    empty = _empty_cells(board)
    if not empty:
        return
    row, col = random.choice(empty)
    board[row][col] = 4 if random.random() < 0.1 else 2


def _spawn_threes_tile(board):
    empty = _empty_cells(board)
    if not empty:
        return
    row, col = random.choice(empty)
    board[row][col] = random.choice([1, 2])


def _compress_line_2048(line):
    values = [value for value in line if value != 0]
    merged = []
    skip = False
    for index in range(len(values)):
        if skip:
            skip = False
            continue
        if index + 1 < len(values) and values[index] == values[index + 1]:
            merged.append(values[index] * 2)
            skip = True
        else:
            merged.append(values[index])
    return merged + [0] * (len(line) - len(merged))


def _compress_line_threes(line):
    values = [value for value in line if value != 0]
    merged = []
    index = 0
    while index < len(values):
        if index + 1 < len(values):
            current = values[index]
            nxt = values[index + 1]
            if {current, nxt} == {1, 2}:
                merged.append(3)
                index += 2
                continue
            if current >= 3 and current == nxt:
                merged.append(current * 2)
                index += 2
                continue
        merged.append(values[index])
        index += 1
    return merged + [0] * (len(line) - len(merged))


def _transpose(board):
    return [list(row) for row in zip(*board)]


def _move_board(board, direction, mode):
    original = deepcopy(board)
    compressor = _compress_line_2048 if mode == "2048" else _compress_line_threes

    work = deepcopy(board)
    if direction in ("up", "down"):
        work = _transpose(work)

    for row_index in range(len(work)):
        row = work[row_index]
        if direction in ("right", "down"):
            row = list(reversed(row))
        row = compressor(row)
        if direction in ("right", "down"):
            row = list(reversed(row))
        work[row_index] = row

    if direction in ("up", "down"):
        work = _transpose(work)

    changed = work != original
    return work, changed


def _can_move(board, mode):
    for direction in ["left", "right", "up", "down"]:
        moved, changed = _move_board(board, direction, mode)
        if changed:
            return True
        if moved != board:
            return True
    return False


def _init_sliding_state(slug):
    board = _new_board(4)
    if slug == "2048":
        _spawn_2048_tile(board)
        _spawn_2048_tile(board)
    else:
        _spawn_threes_tile(board)
        _spawn_threes_tile(board)
    return {
        "mode": "sliding",
        "board": board,
        "message": "Use arrow buttons to move tiles.",
        "game_over": False,
        "target": SLIDING_GAMES[slug],
    }


def _rank_hand(hand):
    counts = {}
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    sorted_counts = sorted(counts.values(), reverse=True)
    unique_sorted = sorted(set(hand))
    is_run = len(unique_sorted) == len(hand) and max(unique_sorted) - min(unique_sorted) == len(hand) - 1

    if sorted_counts[0] == 3:
        return 700 + max(hand)
    if is_run:
        return 500 + max(hand)
    if sorted_counts[0] == 2:
        pair_value = max(value for value, count in counts.items() if count == 2)
        return 300 + pair_value
    return 100 + sum(hand)


def _deal_hand(size=3):
    deck = list(range(1, 14)) * 4
    random.shuffle(deck)
    return sorted(deck[:size])


def _init_cards_state(slug):
    return {
        "mode": "cards",
        "round": 1,
        "player_score": 0,
        "ai_score": 0,
        "player_hand": [],
        "ai_hand": [],
        "message": f"Round 1 in {GAME_MAP[slug]['name']}. Click Deal Round.",
        "game_over": False,
        "winner": None,
    }


def _init_duel_state(slug):
    size = DUEL_BOARD_SIZES[slug]
    return {
        "mode": "duel",
        "round": 1,
        "board_size": size,
        "board": [[0 for _ in range(size)] for _ in range(size)],
        "player_score": 0,
        "ai_score": 0,
        "selected_move": DUEL_ACTIONS[slug][0][0],
        "message": "Pick a move style, then click an empty board cell.",
        "game_over": False,
        "winner": None,
        "actions": DUEL_ACTIONS[slug],
    }


def _init_sudoku_state():
    puzzle = [
        [1, 0, 0, 4],
        [0, 4, 1, 0],
        [0, 1, 4, 0],
        [4, 0, 0, 1],
    ]
    solution = [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1],
    ]
    fixed = [[value != 0 for value in row] for row in puzzle]
    return {
        "mode": "puzzle",
        "puzzle_type": "sudoku",
        "board": puzzle,
        "fixed": fixed,
        "solution": solution,
        "message": "Fill all cells with numbers 1-4.",
        "game_over": False,
        "winner": None,
    }


def _neighbor_cells(row, col, size):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < size and 0 <= nc < size:
                yield nr, nc


def _init_minesweeper_state():
    size = 6
    mine_count = 8
    mines = set()
    while len(mines) < mine_count:
        mines.add((random.randint(0, size - 1), random.randint(0, size - 1)))

    revealed = [[False for _ in range(size)] for _ in range(size)]
    return {
        "mode": "puzzle",
        "puzzle_type": "minesweeper",
        "size": size,
        "mines": [list(item) for item in mines],
        "revealed": revealed,
        "message": "Reveal safe cells. Avoid mines.",
        "game_over": False,
        "winner": None,
    }


def _init_rubiks_state():
    target = [1, 2, 3, 4, 5, 6]
    current = target[:]
    for _ in range(8):
        if random.random() < 0.5:
            current = current[1:] + current[:1]
        else:
            current[0], current[1] = current[1], current[0]
    return {
        "mode": "puzzle",
        "puzzle_type": "rubiks-cube",
        "target": target,
        "current": current,
        "message": "Rubik's Cube Lite: rotate or swap until order matches target.",
        "game_over": False,
        "winner": None,
    }


def _init_state(slug):
    mode = _game_mode(slug)
    if mode == "sliding":
        return _init_sliding_state(slug)
    if mode == "cards":
        return _init_cards_state(slug)
    if mode == "duel":
        return _init_duel_state(slug)
    if slug == "sudoku":
        return _init_sudoku_state()
    if slug == "minesweeper":
        return _init_minesweeper_state()
    if slug == "rubiks-cube":
        return _init_rubiks_state()
    return None


def _get_state(slug):
    key = _state_key(slug)
    state = session.get(key)
    if state is None:
        state = _init_state(slug)
        session[key] = state
    mode = _game_mode(slug)
    if mode == "duel" and ("board" not in state or "board_size" not in state):
        state = _init_duel_state(slug)
        session[key] = state
    return state


def _save_state(slug, state):
    session[_state_key(slug)] = state
    session.modified = True


def _handle_sliding_action(slug, state, form):
    action = form.get("action")
    if action == "new":
        return _init_sliding_state(slug)

    if action not in {"left", "right", "up", "down"} or state["game_over"]:
        return state

    mode = "2048" if slug == "2048" else "threes"
    board, changed = _move_board(state["board"], action, mode)
    if not changed:
        state["message"] = "No tiles moved with that direction."
        return state

    state["board"] = board
    if slug == "2048":
        _spawn_2048_tile(state["board"])
    else:
        _spawn_threes_tile(state["board"])

    max_tile = max(max(row) for row in state["board"])
    if max_tile >= state["target"]:
        state["game_over"] = True
        state["winner"] = "You"
        state["message"] = f"You reached {state['target']}!"
    elif not _can_move(state["board"], mode):
        state["game_over"] = True
        state["winner"] = "Computer"
        state["message"] = "No moves left. Try again."
    else:
        state["message"] = "Move recorded."
    return state


def _handle_cards_action(slug, state, form):
    action = form.get("action")
    if action == "new":
        return _init_cards_state(slug)
    if action != "deal" or state["game_over"]:
        return state

    state["player_hand"] = _deal_hand(3)
    state["ai_hand"] = _deal_hand(3)
    player_rank = _rank_hand(state["player_hand"])
    ai_rank = _rank_hand(state["ai_hand"])

    if player_rank > ai_rank:
        state["player_score"] += 1
        round_result = "You won this round."
    elif ai_rank > player_rank:
        state["ai_score"] += 1
        round_result = "Computer won this round."
    else:
        round_result = "Round draw."

    if state["player_score"] >= 5 or state["ai_score"] >= 5 or state["round"] >= 9:
        state["game_over"] = True
        if state["player_score"] > state["ai_score"]:
            state["winner"] = "You"
            state["message"] = f"Match over. You win {state['player_score']} - {state['ai_score']}."
        elif state["ai_score"] > state["player_score"]:
            state["winner"] = "Computer"
            state["message"] = f"Match over. Computer wins {state['ai_score']} - {state['player_score']}."
        else:
            state["winner"] = "Draw"
            state["message"] = f"Match over. Draw {state['player_score']} - {state['ai_score']}."
    else:
        state["round"] += 1
        state["message"] = f"{round_result} Next: round {state['round']}."
    return state


def _duel_neighbors(row, col, size):
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < size and 0 <= nc < size:
            yield nr, nc


def _duel_count_owner(board, owner):
    total = 0
    for row in board:
        for value in row:
            if value == owner:
                total += 1
    return total


def _duel_empty_cells(board):
    cells = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                cells.append((row, col))
    return cells


def _duel_apply_placement(board, row, col, owner, attack, defense):
    size = len(board)
    board[row][col] = owner

    enemy = -1 if owner == 1 else 1
    adjacent_enemy = []
    for nr, nc in _duel_neighbors(row, col, size):
        if board[nr][nc] == enemy:
            adjacent_enemy.append((nr, nc))

    random.shuffle(adjacent_enemy)
    flips = min(len(adjacent_enemy), max(0, defense))
    for index in range(flips):
        nr, nc = adjacent_enemy[index]
        board[nr][nc] = owner

    if attack >= 7:
        extra = []
        for nr, nc in _duel_neighbors(row, col, size):
            if board[nr][nc] == 0:
                extra.append((nr, nc))
        if extra:
            er, ec = random.choice(extra)
            board[er][ec] = owner


def _duel_pick_ai_cell(board):
    size = len(board)
    ai_frontier = []
    for row in range(size):
        for col in range(size):
            if board[row][col] != 0:
                continue
            for nr, nc in _duel_neighbors(row, col, size):
                if board[nr][nc] == -1:
                    ai_frontier.append((row, col))
                    break

    if ai_frontier:
        return random.choice(ai_frontier)

    empty = _duel_empty_cells(board)
    if not empty:
        return None
    return random.choice(empty)


def _duel_finish_if_needed(state):
    if _duel_empty_cells(state["board"]):
        return

    state["game_over"] = True
    if state["player_score"] > state["ai_score"]:
        state["winner"] = "You"
        state["message"] = f"Board complete. You win {state['player_score']} - {state['ai_score']}."
    elif state["ai_score"] > state["player_score"]:
        state["winner"] = "Computer"
        state["message"] = f"Board complete. Computer wins {state['ai_score']} - {state['player_score']}."
    else:
        state["winner"] = "Draw"
        state["message"] = f"Board complete. Draw {state['player_score']} - {state['ai_score']}."


def _handle_duel_action(slug, state, form):
    action = form.get("action")
    if action == "new":
        return _init_duel_state(slug)
    if state["game_over"]:
        return state

    if action == "choose_move":
        selected = form.get("move")
        if any(item[0] == selected for item in state["actions"]):
            state["selected_move"] = selected
            state["message"] = f"Selected move: {selected}. Now click an empty board cell."
        else:
            state["message"] = "Invalid move style."
        return state

    if action != "place":
        return state

    try:
        row = int(form.get("row", "-1"))
        col = int(form.get("col", "-1"))
    except ValueError:
        state["message"] = "Invalid board cell."
        return state

    size = state["board_size"]
    if not (0 <= row < size and 0 <= col < size):
        state["message"] = "Cell out of range."
        return state
    if state["board"][row][col] != 0:
        state["message"] = "That cell is already occupied."
        return state

    action_name = form.get("move") or state.get("selected_move")
    player_action = None
    for item in state["actions"]:
        if item[0] == action_name:
            player_action = item
            break

    if player_action is None:
        state["message"] = "Invalid action."
        return state

    state["selected_move"] = player_action[0]
    _duel_apply_placement(state["board"], row, col, 1, player_action[1], player_action[2])
    state["player_score"] = _duel_count_owner(state["board"], 1)
    state["ai_score"] = _duel_count_owner(state["board"], -1)

    _duel_finish_if_needed(state)
    if state["game_over"]:
        return state

    ai_action = random.choice(state["actions"])
    ai_cell = _duel_pick_ai_cell(state["board"])
    if ai_cell is not None:
        ai_row, ai_col = ai_cell
        _duel_apply_placement(state["board"], ai_row, ai_col, -1, ai_action[1], ai_action[2])

    state["player_score"] = _duel_count_owner(state["board"], 1)
    state["ai_score"] = _duel_count_owner(state["board"], -1)
    state["round"] += 1

    _duel_finish_if_needed(state)
    if not state["game_over"]:
        state["message"] = (
            f"You played {player_action[0]} at ({row},{col}). "
            f"Computer played {ai_action[0]}"
            + (f" at ({ai_cell[0]},{ai_cell[1]})." if ai_cell else ".")
        )

    return state


def _count_adjacent_mines(mines, row, col, size):
    mine_set = {(item[0], item[1]) for item in mines}
    count = 0
    for nr, nc in _neighbor_cells(row, col, size):
        if (nr, nc) in mine_set:
            count += 1
    return count


def _reveal_safe_cells(state, row, col):
    size = state["size"]
    mine_set = {(item[0], item[1]) for item in state["mines"]}
    stack = [(row, col)]
    seen = set()

    while stack:
        cr, cc = stack.pop()
        if (cr, cc) in seen:
            continue
        seen.add((cr, cc))
        if (cr, cc) in mine_set:
            continue

        state["revealed"][cr][cc] = True
        adjacent = _count_adjacent_mines(state["mines"], cr, cc, size)
        if adjacent == 0:
            for nr, nc in _neighbor_cells(cr, cc, size):
                if not state["revealed"][nr][nc]:
                    stack.append((nr, nc))


def _all_safe_revealed(state):
    size = state["size"]
    mine_set = {(item[0], item[1]) for item in state["mines"]}
    for row in range(size):
        for col in range(size):
            if (row, col) not in mine_set and not state["revealed"][row][col]:
                return False
    return True


def _handle_puzzle_action(slug, state, form):
    action = form.get("action")
    if action == "new":
        return _init_state(slug)
    if state["game_over"]:
        return state

    if slug == "sudoku":
        if action != "set":
            return state
        try:
            row = int(form.get("row", "-1"))
            col = int(form.get("col", "-1"))
            value = int(form.get("value", "0"))
        except ValueError:
            state["message"] = "Invalid input."
            return state

        if not (0 <= row < 4 and 0 <= col < 4 and 1 <= value <= 4):
            state["message"] = "Use row/col in 0..3 and value in 1..4."
            return state
        if state["fixed"][row][col]:
            state["message"] = "That cell is fixed."
            return state

        state["board"][row][col] = value
        if state["board"] == state["solution"]:
            state["game_over"] = True
            state["winner"] = "You"
            state["message"] = "Sudoku solved."
        else:
            state["message"] = "Value placed."
        return state

    if slug == "minesweeper":
        if action != "reveal":
            return state
        try:
            row = int(form.get("row", "-1"))
            col = int(form.get("col", "-1"))
        except ValueError:
            state["message"] = "Invalid cell."
            return state
        if not (0 <= row < state["size"] and 0 <= col < state["size"]):
            state["message"] = "Cell out of bounds."
            return state

        mine_set = {(item[0], item[1]) for item in state["mines"]}
        if (row, col) in mine_set:
            state["game_over"] = True
            state["winner"] = "Computer"
            state["revealed"][row][col] = True
            state["message"] = "Mine hit. Game over."
            return state

        _reveal_safe_cells(state, row, col)
        if _all_safe_revealed(state):
            state["game_over"] = True
            state["winner"] = "You"
            state["message"] = "You cleared all safe cells."
        else:
            state["message"] = "Safe reveal."
        return state

    if slug == "rubiks-cube":
        if action == "rotate":
            state["current"] = state["current"][1:] + state["current"][:1]
        elif action == "rotate-back":
            state["current"] = state["current"][-1:] + state["current"][:-1]
        elif action == "swap":
            state["current"][0], state["current"][1] = state["current"][1], state["current"][0]
        else:
            return state

        if state["current"] == state["target"]:
            state["game_over"] = True
            state["winner"] = "You"
            state["message"] = "Rubik's Cube Lite solved."
        else:
            state["message"] = "Move applied."
        return state

    return state


@lite_bp.route("/<slug>/", methods=["GET", "POST"])
def play_lite_game(slug):
    game = GAME_MAP.get(slug)
    if game is None:
        abort(404)

    mode = _game_mode(slug)
    if mode is None:
        abort(404)

    state = _get_state(slug)

    if request.method == "POST":
        if mode == "sliding":
            state = _handle_sliding_action(slug, state, request.form)
        elif mode == "cards":
            state = _handle_cards_action(slug, state, request.form)
        elif mode == "duel":
            state = _handle_duel_action(slug, state, request.form)
        else:
            state = _handle_puzzle_action(slug, state, request.form)

        _save_state(slug, state)
        return redirect(url_for("lite.play_lite_game", slug=slug))

    mines_counts = None
    if slug == "minesweeper":
        mines_counts = []
        for row in range(state["size"]):
            count_row = []
            for col in range(state["size"]):
                count_row.append(_count_adjacent_mines(state["mines"], row, col, state["size"]))
            mines_counts.append(count_row)

    return render_template(
        "lite_game.html",
        game=game,
        slug=slug,
        mode=mode,
        state=state,
        mines_counts=mines_counts,
    )
