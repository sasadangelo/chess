import argparse
from src.model.games import GameCollection, ResultGame

if __name__ == "__main__":
    # Configura il parser per gestire gli argomenti da riga di comando
    parser = argparse.ArgumentParser(description='Chess games Report')
    parser.add_argument('--user', type=str, default="", required=True, help='The user for whom the report is to be created')
    parser.add_argument('--num-games', type=int, default=-1, required=True, help='Number of recent games to select')
    parser.add_argument('--time-control', type=str, default="", required=True, help='The desired chess game time control (daily, rapid, blitz, bullet, etc.)')
    parser.add_argument('--output', type=str, default="docs/REPORT.md", required=False, help='The output report')
    parser.add_argument('--color', type=str, default="", required=False, help='The pieces color (white, black, or any)')
    args = parser.parse_args()

    num_games = args.num_games if args.num_games >= 0 else None
    time_control = args.time_control if args.time_control != "" else None
    color = args.color if args.color != "" else None
    game_collection = GameCollection(args.user, num_games, time_control, color)

    # Apre il file REPORT.md in modalità scrittura
    with open(args.output, "w") as report_file:
        report_file.write(f"# Chess games Report for the latest {args.num_games} {args.user}'s games.\n\n")
        report_file.write(f"Total games: {game_collection.total_games}\n")
        report_file.write(f"- Win games: {game_collection.win_games} ({game_collection.win_games*100/game_collection.total_games:.2f} %)\n")
        report_file.write(f"- Lost games: {game_collection.lost_games} ({game_collection.lost_games*100/game_collection.total_games:.2f} %)\n")
        report_file.write(f"- Draw games: {game_collection.draw_games} ({game_collection.draw_games*100/game_collection.total_games:.2f} %)\n")
        for opening_name, games in game_collection.games_by_opening.items():
            report_file.write(f"\n## {opening_name} ({len(games)})\n\n")
            report_file.write( "| Opening | Date and Time | Variation | Result |\n")
            report_file.write( "|---------|---------------|-----------|--------|\n")
            for game in games:
                if (args.color == "") or (args.color == "white" and game.white_player == args.user) or (args.color == "black" and game.black_player == args.user):
                    if game.result == ResultGame.DRAW:
                        image_markdown = "![Draw](img/draw.png)"
                    elif game.result == ResultGame.WIN:
                        image_markdown = "![Win](img/win.png)"
                    else:
                        image_markdown = "![Lose](img/lose.png)"
                    report_file.write(f"| [{game.white_player} ({game.white_elo}) vs {game.black_player} ({game.black_elo})]({game.link}) | {game.start_time.strftime("%Y%m%d %H:%M")} | [{game.opening_variation}]({game.opening_url}) | {image_markdown} |\n")