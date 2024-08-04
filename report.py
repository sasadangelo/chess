import argparse
from src.model.games import GameCollection, Game

if __name__ == "__main__":
    # Configura il parser per gestire gli argomenti da riga di comando
    parser = argparse.ArgumentParser(description='Chess games Report')
    parser.add_argument('--user', type=str, default="", required=True, help='The user for whom the report is to be created')
    parser.add_argument('--num-games', type=int, default=-1, required=True, help='Number of recent games to select')
    parser.add_argument('--time-control', type=str, default="", required=True, help='The desired chess game time control (daily, rapid, blitz, bullet, etc.)')
    parser.add_argument('--output', type=str, default="docs/REPORT.md", required=False, help='The output report')
    args = parser.parse_args()

    pgn_file_name = args.user + ".pgn"
    num_games = args.num_games if args.num_games >= 0 else None
    time_control = args.time_control if args.time_control != "" else None
    game_collection = GameCollection(pgn_file_name, num_games, time_control)

    # Apre il file REPORT.md in modalità scrittura
    with open(args.output, "w") as report_file:
        report_file.write(f"# Chess games Report for the latest {args.num_games} {args.user}'s games.\n\n")
        for opening_name, games in game_collection.games_by_opening.items():
            report_file.write(f"\n## {opening_name} ({len(games)})\n\n")
            report_file.write( "| Opening | Date and Time | Variation | Result |\n")
            report_file.write( "|---------|---------------|-----------|--------|\n")
            for game in games:
                if game.result == "1/2-1/2":
                    report_file.write(f"| [{game.white_player} ({game.white_elo}) vs {game.black_player} ({game.black_elo})]({game.link}) | {game.start_time.strftime("%Y%m%d %H:%M")} | [{game.opening_variation}]({game.opening_url}) | ![Draw](img/draw.png) |\n")
                elif (game.white_player == args.user and game.result == "1-0") or (game.black_player == args.user and game.result == "0-1"):
                    report_file.write(f"| [{game.white_player} ({game.white_elo}) vs {game.black_player} ({game.black_elo})]({game.link}) | {game.start_time.strftime("%Y%m%d %H:%M")} | [{game.opening_variation}]({game.opening_url}) | ![Win](img/win.png) |\n")
                else:
                    report_file.write(f"| [{game.white_player} ({game.white_elo}) vs {game.black_player} ({game.black_elo})]({game.link}) | {game.start_time.strftime("%Y%m%d %H:%M")} | [{game.opening_variation}]({game.opening_url}) | ![Lose](img/lose.png) |\n")
