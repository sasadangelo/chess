import chess
import chess.engine
from src.model.games import ResultGame

MATE_SCORE_CP = 100000

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}


class PuzzleCandidate:
    def __init__(self, fen, solution_uci, cp_loss, category, difficulty, game):
        self.fen = fen
        self.solution_uci = solution_uci
        self.cp_loss = cp_loss
        self.category = category
        self.difficulty = difficulty
        self.game_link = game.link
        self.date = game.start_time
        self.opening_name = game.opening_name


def _score_cp(pov_score):
    return pov_score.score(mate_score=MATE_SCORE_CP)


def _classify_category(board_before, move, mover_color, mate_missed):
    if mate_missed:
        return "Matto Mancato"

    board_after = board_before.copy()
    moving_piece = board_before.piece_at(move.from_square)
    captured_piece = board_before.piece_at(move.to_square)
    board_after.push(move)

    # Forchetta: dalla casa di arrivo il pezzo attacca almeno 2 pezzi avversari di valore (cavallo o superiore).
    attacked = board_after.attacks(move.to_square)
    valuable_targets = [
        sq for sq in attacked
        if board_after.piece_at(sq) and board_after.piece_at(sq).color != mover_color
        and PIECE_VALUES[board_after.piece_at(sq).piece_type] >= 3
    ]
    if len(valuable_targets) >= 2:
        return "Forchetta"

    # Pezzo appeso / cattura vantaggiosa: si cattura un pezzo di valore maggiore, o la casa non è più difesa.
    if captured_piece is not None:
        gain = PIECE_VALUES[captured_piece.piece_type] - PIECE_VALUES[moving_piece.piece_type]
        defenders = board_after.attackers(not mover_color, move.to_square)
        if gain > 0 or not defenders:
            return "Pezzo Appeso"

    # Scoperta: rimuovendo il pezzo mosso, un proprio pezzo a lungo raggio scopre un nuovo attacco.
    for square in chess.SQUARES:
        if square in (move.from_square, move.to_square):
            continue
        piece = board_before.piece_at(square)
        if not piece or piece.color != mover_color:
            continue
        if piece.piece_type not in (chess.BISHOP, chess.ROOK, chess.QUEEN):
            continue
        before_attacks = board_before.attacks(square)
        after_attacks = board_after.attacks(square)
        newly_attacked = after_attacks - before_attacks
        for sq in newly_attacked:
            target = board_after.piece_at(sq)
            if target and target.color != mover_color and PIECE_VALUES[target.piece_type] >= 3:
                return "Scoperta"

    return "Tattica Generica"


def _difficulty_from_cp_loss(cp_loss):
    # Euristica basata sulla grandezza dell'errore, non un rating di puzzle calibrato:
    # un errore molto grande (es. donna appesa) è tipicamente più facile da individuare
    # in un puzzle isolato di un errore vicino alla soglia, più subdolo.
    if cp_loss >= 600:
        return "Facile"
    if cp_loss >= 350:
        return "Media"
    return "Difficile"


def find_puzzles(game_collection, username, engine, depth=14, min_cp_loss=200, include_wins=False, progress_callback=None):
    puzzles = []
    for i, game in enumerate(game_collection.games):
        if progress_callback:
            progress_callback(i + 1, len(game_collection.games))
        if not include_wins and game.result != ResultGame.LOSE:
            continue

        mover_color = chess.WHITE if game.white_player == username else chess.BLACK
        board = game.game.board()

        for move in game.game.mainline_moves():
            if board.turn != mover_color:
                board.push(move)
                continue

            fen_before = board.fen()
            info_before = engine.analyse(board, chess.engine.Limit(depth=depth))
            score_before = info_before["score"].pov(mover_color)
            best_move = info_before["pv"][0] if info_before.get("pv") else move
            mate_before = score_before.mate()

            board.push(move)
            info_after = engine.analyse(board, chess.engine.Limit(depth=depth))
            score_after = info_after["score"].pov(mover_color)

            cp_loss = _score_cp(score_before) - _score_cp(score_after)
            mate_missed = bool(mate_before and mate_before > 0 and not (score_after.is_mate() and score_after.mate() and score_after.mate() > 0))

            if cp_loss >= min_cp_loss or mate_missed:
                board_before_move = chess.Board(fen_before)
                category = _classify_category(board_before_move, best_move, mover_color, mate_missed)
                difficulty = _difficulty_from_cp_loss(cp_loss)
                puzzles.append(PuzzleCandidate(fen_before, best_move.uci(), cp_loss, category, difficulty, game))

    return puzzles
