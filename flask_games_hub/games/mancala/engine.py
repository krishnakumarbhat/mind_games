from copy import deepcopy

HUMAN_PITS = [0, 1, 2, 3, 4, 5]
HUMAN_STORE = 6
AI_PITS = [7, 8, 9, 10, 11, 12]
AI_STORE = 13


def initial_board():
    return [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]


def legal_moves(board, player):
    pits = HUMAN_PITS if player == "human" else AI_PITS
    return [pit for pit in pits if board[pit] > 0]


def opposite_pit(index):
    return 12 - index


def apply_move(board, pit, player):
    next_board = deepcopy(board)
    stones = next_board[pit]
    next_board[pit] = 0
    index = pit

    while stones > 0:
        index = (index + 1) % 14
        if player == "human" and index == AI_STORE:
            continue
        if player == "ai" and index == HUMAN_STORE:
            continue
        next_board[index] += 1
        stones -= 1

    extra_turn = (player == "human" and index == HUMAN_STORE) or (player == "ai" and index == AI_STORE)

    if not extra_turn:
        if player == "human" and index in HUMAN_PITS and next_board[index] == 1:
            opposite = opposite_pit(index)
            if next_board[opposite] > 0:
                next_board[HUMAN_STORE] += next_board[opposite] + 1
                next_board[index] = 0
                next_board[opposite] = 0
        elif player == "ai" and index in AI_PITS and next_board[index] == 1:
            opposite = opposite_pit(index)
            if next_board[opposite] > 0:
                next_board[AI_STORE] += next_board[opposite] + 1
                next_board[index] = 0
                next_board[opposite] = 0

    game_over = all(next_board[p] == 0 for p in HUMAN_PITS) or all(next_board[p] == 0 for p in AI_PITS)
    if game_over:
        human_remaining = sum(next_board[p] for p in HUMAN_PITS)
        ai_remaining = sum(next_board[p] for p in AI_PITS)

        for p in HUMAN_PITS:
            next_board[p] = 0
        for p in AI_PITS:
            next_board[p] = 0

        next_board[HUMAN_STORE] += human_remaining
        next_board[AI_STORE] += ai_remaining

    return next_board, extra_turn


def score(board):
    return (board[AI_STORE] - board[HUMAN_STORE]) + 0.1 * (sum(board[p] for p in AI_PITS) - sum(board[p] for p in HUMAN_PITS))


def minimax(board, depth, alpha, beta, maximizing):
    player = "ai" if maximizing else "human"
    moves = legal_moves(board, player)

    game_over = all(board[p] == 0 for p in HUMAN_PITS) or all(board[p] == 0 for p in AI_PITS)
    if depth == 0 or game_over or not moves:
        return score(board), None

    best_move = None

    if maximizing:
        max_eval = float("-inf")
        for move in moves:
            next_board, extra_turn = apply_move(board, move, "ai")
            next_is_max = True if extra_turn else False
            eval_score, _ = minimax(next_board, depth - 1, alpha, beta, next_is_max)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return max_eval, best_move

    min_eval = float("inf")
    for move in moves:
        next_board, extra_turn = apply_move(board, move, "human")
        next_is_max = False if extra_turn else True
        eval_score, _ = minimax(next_board, depth - 1, alpha, beta, next_is_max)

        if eval_score < min_eval:
            min_eval = eval_score
            best_move = move

        beta = min(beta, eval_score)
        if beta <= alpha:
            break

    return min_eval, best_move


def choose_ai_move(board):
    _, move = minimax(board, depth=6, alpha=float("-inf"), beta=float("inf"), maximizing=True)
    return move


def winner(board):
    if board[HUMAN_STORE] > board[AI_STORE]:
        return "You"
    if board[AI_STORE] > board[HUMAN_STORE]:
        return "Computer"
    return "Draw"
