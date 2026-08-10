import argparse
from collections import Counter
import chess.engine
from src.model.games import GameCollection
from src.model.puzzle_extraction import find_puzzles

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract tactics puzzles from your own games using Stockfish")
    parser.add_argument("--user", type=str, required=True, help="The user for whom puzzles are extracted")
    parser.add_argument("--num-games", type=int, default=None, help="Number of recent games to scan")
    parser.add_argument("--time-control", type=str, default=None, help="rapid, blitz, bullet or standard (daily)")
    parser.add_argument("--min-cp-loss", type=int, default=200, help="Minimum centipawn loss to flag a puzzle")
    parser.add_argument("--depth", type=int, default=14, help="Stockfish search depth per position")
    parser.add_argument("--include-wins", action="store_true", help="Also scan won/drawn games, not just losses")
    parser.add_argument("--output", type=str, default="chessgame/data/tactics_puzzles.csv", help="Output CSV path")
    parser.add_argument("--engine-path", type=str, default="stockfish", help="Path to the Stockfish binary")
    args = parser.parse_args()

    game_collection = GameCollection(args.user, args.num_games, args.time_control)

    if game_collection.total_games == 0:
        print(f"No games found for user {args.user} with time-control={args.time_control}")
    else:
        def report_progress(current, total):
            if current % 10 == 0 or current == total:
                print(f"Analyzing game {current}/{total}...", flush=True)

        engine = chess.engine.SimpleEngine.popen_uci(args.engine_path)
        try:
            puzzles = find_puzzles(
                game_collection, args.user, engine,
                depth=args.depth,
                min_cp_loss=args.min_cp_loss,
                include_wins=args.include_wins,
                progress_callback=report_progress,
            )
        finally:
            engine.quit()

        with open(args.output, "w") as f:
            f.write("ID, Category, Difficulty, FEN, Solution, GameLink, Date, Opening\n")
            for i, puzzle in enumerate(puzzles):
                f.write(
                    f"{i + 1}, {puzzle.category}, {puzzle.difficulty}, {puzzle.fen}, {puzzle.solution_uci}, "
                    f"{puzzle.game_link}, {puzzle.date.strftime('%Y-%m-%d')}, {puzzle.opening_name}\n"
                )

        print(f"\n{len(puzzles)} puzzles written to {args.output}")
        print("By category:", dict(Counter(p.category for p in puzzles)))
        print("By difficulty:", dict(Counter(p.difficulty for p in puzzles)))
