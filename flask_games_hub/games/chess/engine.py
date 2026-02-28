import random

import chess

PIECE_UNICODE = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}


def initial_fen():
    return chess.Board().fen()


def board_from_fen(fen):
    return chess.Board(fen)


def square_name(square):
    return chess.square_name(square)


def board_matrix(board):
    rows = []
    for rank in range(7, -1, -1):
        row = []
        for file_index in range(8):
            square = chess.square(file_index, rank)
            piece = board.piece_at(square)
            row.append(
                {
                    "square": chess.square_name(square),
                    "piece": PIECE_UNICODE[piece.symbol()] if piece else "",
                    "is_light": (rank + file_index) % 2 == 0,
                    "is_white_piece": piece.color if piece else None,
                }
            )
        rows.append(row)
    return rows


def legal_destinations_for_square(board, from_square):
    moves = []
    for move in board.legal_moves:
        if chess.square_name(move.from_square) == from_square:
            moves.append(chess.square_name(move.to_square))
    return moves


def _move_score(board, move):
    score = 0

    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        if captured_piece:
            score += PIECE_VALUES.get(captured_piece.piece_type, 0) * 10

    if move.promotion:
        score += PIECE_VALUES.get(move.promotion, 0) * 4

    board.push(move)
    if board.is_checkmate():
        score += 10000
    elif board.is_check():
        score += 30

    if board.is_stalemate():
        score -= 5

    score += random.randint(0, 3)
    board.pop()

    return score


def choose_computer_move(board):
    legal = list(board.legal_moves)
    if not legal:
        return None

    best = None
    best_score = None
    for move in legal:
        score = _move_score(board, move)
        if best_score is None or score > best_score:
            best_score = score
            best = move
    return best


def game_status(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return "Checkmate. Computer wins."
        return "Checkmate. You win."
    if board.is_stalemate():
        return "Draw by stalemate."
    if board.is_insufficient_material():
        return "Draw by insufficient material."
    if board.can_claim_threefold_repetition():
        return "Threefold repetition claim available."
    if board.can_claim_fifty_moves():
        return "Fifty-move rule claim available."
    if board.is_check():
        if board.turn == chess.WHITE:
            return "Your king is in check."
        return "Computer is in check."
    return "Your turn. Select a piece, then select destination."
