import argparse
import csv
import chess
import chess.engine

WIN_THRESHOLD_CP = 250
DRAW_THRESHOLD_CP = 100


def load_rows(path):
    with open(path) as f:
        reader = csv.reader(f)
        header = [h.strip() for h in next(reader)]
        rows = [[c.strip() for c in row] for row in reader if row]
    return header, rows


def classify(score):
    mate = score.mate()
    if mate is not None:
        return ("Win" if mate > 0 else "Loss"), f"mate in {abs(mate)}"
    cp = score.score()
    if cp >= WIN_THRESHOLD_CP:
        return "Win", f"{cp}cp"
    if cp <= -WIN_THRESHOLD_CP:
        return "Loss", f"{cp}cp"
    if abs(cp) < DRAW_THRESHOLD_CP:
        return "Draw", f"{cp}cp"
    return "REVIEW", f"{cp}cp (ambiguous)"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Label Win/Draw objective for each endgame position using Stockfish")
    parser.add_argument("--input", type=str, default="chessgame/data/end_games.csv")
    parser.add_argument("--depth", type=int, default=22)
    parser.add_argument("--engine-path", type=str, default="stockfish")
    parser.add_argument("--apply", action="store_true", help="Write the Objective column back to the CSV (default: report only)")
    args = parser.parse_args()

    header, rows = load_rows(args.input)
    name_idx = header.index("Name")
    fen_idx = header.index("FEN")

    engine = chess.engine.SimpleEngine.popen_uci(args.engine_path)
    results = []
    try:
        for row in rows:
            fen = row[fen_idx]
            board = chess.Board(fen)
            info = engine.analyse(board, chess.engine.Limit(depth=args.depth))
            objective, detail = classify(info["score"].pov(board.turn))
            results.append((row[name_idx], fen, objective, detail))
    finally:
        engine.quit()

    print(f"{'Name':<45} {'Objective':<8} Detail")
    print("-" * 80)
    for name, fen, objective, detail in results:
        flag = " <-- REVIEW" if objective in ("REVIEW", "Loss") else ""
        print(f"{name:<45} {objective:<8} {detail}{flag}")

    if args.apply:
        if "Objective" not in header:
            header.append("Objective")
        for row, (_, _, objective, _) in zip(rows, results):
            if len(row) < len(header):
                row.append(objective)
            else:
                row[header.index("Objective")] = objective
        with open(args.input, "w") as f:
            f.write(", ".join(header) + "\n")
            for row in rows:
                f.write(", ".join(row) + "\n")
        print(f"\nObjective column written to {args.input}")
    else:
        print("\nDry run (no file written). Re-run with --apply after reviewing.")
