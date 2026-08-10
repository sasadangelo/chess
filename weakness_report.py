import argparse
from src.model.games import GameCollection, TerminationReason
from src.model.weakness_analysis import WeaknessAnalysis

TERMINATION_LABELS = {
    TerminationReason.CHECKMATE: "Scacco matto",
    TerminationReason.RESIGNATION: "Resa",
    TerminationReason.TIMEOUT: "Tempo scaduto",
    TerminationReason.ABANDONED: "Partita abbandonata",
    TerminationReason.STALEMATE: "Stallo",
    TerminationReason.INSUFFICIENT_MATERIAL: "Materiale insufficiente",
    TerminationReason.REPETITION: "Ripetizione",
    TerminationReason.AGREEMENT: "Accordo",
    TerminationReason.UNKNOWN: "Sconosciuto",
}


def write_opening_table(report_file, title, openings):
    report_file.write(f"\n### {title}\n\n")
    if not openings:
        report_file.write("_Nessuna apertura con un numero di partite sufficiente per un'analisi affidabile._\n")
        return
    report_file.write("| Apertura | Partite | Vittorie | Sconfitte | Patte | Win rate |\n")
    report_file.write("|----------|---------|----------|-----------|-------|----------|\n")
    for stat in openings:
        report_file.write(
            f"| {stat.opening_name} | {stat.total} | {stat.wins} | {stat.losses} | {stat.draws} | {stat.win_rate:.1f}% |\n"
        )


def write_termination_table(report_file, title, counts):
    report_file.write(f"\n### {title}\n\n")
    total = sum(counts.values())
    if total == 0:
        report_file.write("_Nessuna partita in questa categoria._\n")
        return
    report_file.write("| Causa | Partite | % |\n")
    report_file.write("|-------|---------|---|\n")
    for reason, count in sorted(counts.items(), key=lambda item: -item[1]):
        label = TERMINATION_LABELS.get(reason, str(reason))
        report_file.write(f"| {label} | {count} | {count * 100 / total:.1f}% |\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess weakness report (no engine)")
    parser.add_argument("--user", type=str, required=True, help="The user for whom the report is to be created")
    parser.add_argument("--num-games", type=int, required=True, help="Number of recent games to select")
    parser.add_argument(
        "--time-control", type=str, required=True,
        help="rapid, blitz, bullet or standard (daily)",
    )
    parser.add_argument("--output", type=str, default="docs/WEAKNESS_REPORT.md", help="The output report")
    parser.add_argument(
        "--min-sample", type=int, default=5,
        help="Minimum number of games for an opening to be considered in best/worst rankings",
    )
    parser.add_argument(
        "--short-loss-ply-threshold", type=int, default=30,
        help="Sconfitte con meno semi-mosse di questa soglia vengono segnalate come 'partite corte'",
    )
    args = parser.parse_args()

    game_collection = GameCollection(args.user, args.num_games, args.time_control)

    if game_collection.total_games == 0:
        print(f"No games found for user {args.user} with time-control={args.time_control}")
    else:
        analysis = WeaknessAnalysis(
            game_collection, args.user,
            min_sample=args.min_sample,
            short_loss_ply_threshold=args.short_loss_ply_threshold,
        )

        with open(args.output, "w") as report_file:
            report_file.write(f"# Weakness Report for {args.user} ({args.time_control}, {game_collection.total_games} games)\n\n")

            report_file.write("## Sintesi\n\n")
            report_file.write(f"Total games: {game_collection.total_games}\n")
            report_file.write(
                f"- Win games: {game_collection.win_games} ({game_collection.win_games*100/game_collection.total_games:.2f} %)\n"
            )
            report_file.write(
                f"- Lost games: {game_collection.lost_games} ({game_collection.lost_games*100/game_collection.total_games:.2f} %)\n"
            )
            report_file.write(
                f"- Draw games: {game_collection.draw_games} ({game_collection.draw_games*100/game_collection.total_games:.2f} %)\n"
            )
            if analysis.rating_trend:
                first_date, first_elo = analysis.rating_trend[0]
                last_date, last_elo = analysis.rating_trend[-1]
                delta = last_elo - first_elo
                report_file.write(
                    f"- Rating trend: {first_elo} ({first_date.strftime('%Y-%m-%d')}) -> {last_elo} ({last_date.strftime('%Y-%m-%d')}) ({delta:+d})\n"
                )

            report_file.write("\n## Punti di forza (aperture migliori)\n")
            write_opening_table(report_file, "Come Bianco", analysis.best_openings("white"))
            write_opening_table(report_file, "Come Nero", analysis.best_openings("black"))

            report_file.write("\n## Punti deboli (aperture peggiori)\n")
            write_opening_table(report_file, "Come Bianco", analysis.worst_openings("white"))
            write_opening_table(report_file, "Come Nero", analysis.worst_openings("black"))

            report_file.write("\n## Perché perdi\n")
            write_termination_table(report_file, "Cause delle sconfitte", analysis.loss_termination_counts)
            write_termination_table(report_file, "Cause delle vittorie (confronto)", analysis.win_termination_counts)

            report_file.write(f"\n## Partite perse in meno di {args.short_loss_ply_threshold // 2} mosse\n\n")
            if not analysis.short_losses:
                report_file.write("_Nessuna sconfitta rapida rilevata: buon segno, non stai cadendo in trappole d'apertura._\n")
            else:
                report_file.write("| Partita | Data | Mosse | Apertura |\n")
                report_file.write("|---------|------|-------|----------|\n")
                for game in analysis.short_losses:
                    report_file.write(
                        f"| [link]({game.link}) | {game.start_time.strftime('%Y-%m-%d %H:%M')} | {game.num_moves // 2} | {game.opening_name} |\n"
                    )

        print(f"Weakness report written to {args.output}")
