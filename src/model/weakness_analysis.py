from collections import defaultdict
from src.model.games import ResultGame, TerminationReason


class OpeningStat:
    def __init__(self, opening_name):
        self.opening_name = opening_name
        self.total = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def add(self, result):
        self.total += 1
        if result == ResultGame.WIN:
            self.wins += 1
        elif result == ResultGame.LOSE:
            self.losses += 1
        else:
            self.draws += 1

    @property
    def win_rate(self):
        return self.wins * 100 / self.total if self.total else 0.0


class WeaknessAnalysis:
    """Aggrega segnali sulle debolezze di un giocatore senza usare un motore scacchistico:
    risultato per apertura/colore, causa di sconfitta (termination) e partite perse in poche mosse."""

    def __init__(self, game_collection, username, min_sample=5, short_loss_ply_threshold=30):
        self.username = username
        self.games = game_collection.games
        self.min_sample = min_sample
        self.short_loss_ply_threshold = short_loss_ply_threshold

        self.opening_stats_white = self.__compute_opening_stats(color="white")
        self.opening_stats_black = self.__compute_opening_stats(color="black")
        self.loss_termination_counts = self.__compute_termination_counts(ResultGame.LOSE)
        self.win_termination_counts = self.__compute_termination_counts(ResultGame.WIN)
        self.short_losses = self.__compute_short_losses()
        self.rating_trend = self.__compute_rating_trend()

    def __user_color(self, game):
        if game.white_player == self.username:
            return "white"
        if game.black_player == self.username:
            return "black"
        return None

    def __compute_opening_stats(self, color):
        stats = defaultdict(lambda: OpeningStat(None))
        for game in self.games:
            if self.__user_color(game) != color:
                continue
            stat = stats[game.opening_name]
            stat.opening_name = game.opening_name
            stat.add(game.result)
        return list(stats.values())

    def worst_openings(self, color, top_n=5):
        stats = self.opening_stats_white if color == "white" else self.opening_stats_black
        eligible = [s for s in stats if s.total >= self.min_sample]
        return sorted(eligible, key=lambda s: (s.win_rate, -s.total))[:top_n]

    def best_openings(self, color, top_n=5):
        stats = self.opening_stats_white if color == "white" else self.opening_stats_black
        eligible = [s for s in stats if s.total >= self.min_sample]
        return sorted(eligible, key=lambda s: (-s.win_rate, -s.total))[:top_n]

    def __compute_termination_counts(self, result):
        counts = defaultdict(int)
        for game in self.games:
            if game.result == result:
                counts[game.termination_reason] += 1
        return dict(counts)

    def __compute_short_losses(self):
        losses = [
            game for game in self.games
            if game.result == ResultGame.LOSE and game.num_moves < self.short_loss_ply_threshold
        ]
        return sorted(losses, key=lambda g: g.num_moves)

    def __compute_rating_trend(self):
        trend = []
        for game in self.games:
            color = self.__user_color(game)
            if color is None:
                continue
            elo = game.white_elo if color == "white" else game.black_elo
            try:
                trend.append((game.start_time, int(elo)))
            except ValueError:
                continue
        return sorted(trend, key=lambda t: t[0])
