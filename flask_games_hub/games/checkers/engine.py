import random
from copy import deepcopy

EMPTY = 0
HUMAN_MAN = 1
HUMAN_KING = 2
AI_MAN = -1
AI_KING = -2


def initial_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = AI_MAN
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = HUMAN_MAN
    return board


def piece_owner(piece):
    if piece > 0:
        return "human"
    if piece < 0:
        return "ai"
    return None


def move_directions(piece):
    if piece in (HUMAN_KING, AI_KING):
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if piece == HUMAN_MAN:
        return [(-1, -1), (-1, 1)]
    if piece == AI_MAN:
        return [(1, -1), (1, 1)]
    return []


def in_bounds(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def legal_moves(board, player):
    capture_moves = []
    normal_moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece_owner(piece) != player:
                continue

            for dr, dc in move_directions(piece):
                step_r, step_c = row + dr, col + dc
                jump_r, jump_c = row + (2 * dr), col + (2 * dc)

                if in_bounds(step_r, step_c) and board[step_r][step_c] == EMPTY:
                    normal_moves.append(
                        {
                            "from": [row, col],
                            "to": [step_r, step_c],
                            "captures": [],
                        }
                    )

                if not in_bounds(jump_r, jump_c):
                    continue

                middle_piece = board[step_r][step_c] if in_bounds(step_r, step_c) else EMPTY
                if middle_piece != EMPTY and piece_owner(middle_piece) not in (player, None) and board[jump_r][jump_c] == EMPTY:
                    capture_moves.append(
                        {
                            "from": [row, col],
                            "to": [jump_r, jump_c],
                            "captures": [[step_r, step_c]],
                        }
                    )

    return capture_moves if capture_moves else normal_moves


def _promote(piece, row):
    if piece == HUMAN_MAN and row == 0:
        return HUMAN_KING
    if piece == AI_MAN and row == 7:
        return AI_KING
    return piece


def apply_move(board, move):
    updated = deepcopy(board)
    from_r, from_c = move["from"]
    to_r, to_c = move["to"]
    piece = updated[from_r][from_c]
    updated[from_r][from_c] = EMPTY

    for cap_r, cap_c in move["captures"]:
        updated[cap_r][cap_c] = EMPTY

    updated[to_r][to_c] = _promote(piece, to_r)
    return updated


def board_value(board):
    value = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == AI_MAN:
                value += 3 + row * 0.1
            elif piece == AI_KING:
                value += 5
            elif piece == HUMAN_MAN:
                value -= 3 + (7 - row) * 0.1
            elif piece == HUMAN_KING:
                value -= 5
    return value


def choose_ai_move(board):
    moves = legal_moves(board, "ai")
    if not moves:
        return None

    best_score = None
    best_moves = []

    for move in moves:
        next_board = apply_move(board, move)
        score = board_value(next_board)
        if move["captures"]:
            score += 1.5
        to_r, _ = move["to"]
        if to_r == 7:
            score += 0.5

        if best_score is None or score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)


def winner(board):
    human_pieces = 0
    ai_pieces = 0

    for row in board:
        for piece in row:
            if piece > 0:
                human_pieces += 1
            elif piece < 0:
                ai_pieces += 1

    if human_pieces == 0:
        return "Computer"
    if ai_pieces == 0:
        return "You"

    if not legal_moves(board, "human"):
        return "Computer"
    if not legal_moves(board, "ai"):
        return "You"

    return None
