from datetime import datetime, timezone
from collections import defaultdict
import enum
import chess.pgn

# Definisci la mappa con codice di apertura come chiave e tupla di (nome apertura, variante apertura) come valore
opening_map = {
    "A00": ("Irregular Openings", "Uncommon Opening"),
    "A01": ("Nimzowitsch-Larsen Attack", "Nimzowitsch-Larsen Variation"),
    "A15": ("English Opening", "Anglo-Indian, Scandinavian Defense"),
    "A22": ("English Opening", "Two Knights Variation"),
    "B00": ("Nimzowitsch Defense", "Scandinavian, Bogoljubov, Vehre Variation"),
    "B01": ("Scandinavian Defense", "Mieses-Kotrč, Main Line, Lasker Variation"),
    "B02": ("Alekhine's Defense", "Scandinavian Variation"),
    "B07": ("Pirc Defense", "-"),
    "B08": ("Pirc Defense", "Classical Variation"),
    "B15": ("Caro-Kann Defense", "Campomanes Attack"),
    "B17": ("Caro-Kann Defense", "Karpov Variation"),
    "B18": ("Caro-Kann Defense", "Classical Variation"),
    "B30": ("Sicilian Defense", "Open Variation"),
    "B32": ("Sicilian Defense", "Open, Franco-Sicilian Variation"),
    "B33": ("Sicilian Defense", "Open Variation"),
    "B34": ("Sicilian Defense", "Open, Accelerated Dragon, Exchange Variation"),
    "B40": ("Sicilian Defense", "Paulsen-Basman Defense"),
    "C00": ("French Defense", "Normal Variation"),
    "C20": ("King's Pawn Opening", "MacLeod Attack"),
    "C21": ("Center Game", "Accepted Variation"),
    "C22": ("Center Game", "Accepted, Hall Variation"),
    "C23": ("Vienna Game", "Max Lange, Meitner-Mieses Gambit"),
    "C24": ("Bishop's Opening", "Berlin Defense"),
    "C25": ("Vienna Game", "Max Lange, Vienna Gambit"),
    "C26": ("Vienna Game", "Falkbeer, Stanley Variation"),
    "C34": ("King's Gambit", "Accepted Variation, Schallopp Defense"),
    "C40": ("King's Pawn Opening", "King's Knight Variation"),
    "C41": ("Philidor Defense", "Exchange Variation"),
    "C42": ("Petrov's Defense", "Classical, Stafford Gambit"),
    "C44": ("Ponziani", "-"),
    "C45": ("Scotch Game", "-"),
    "C46": ("Three Knights Opening", "-"),
    "C47": ("Four Knights Game", "Scotch Variation"),
    "C48": ("Four Knights Game", "Spanish Variation, Ranken Variation"),
    "C50": ("Italian Game", "Giuoco Piano, Giuoco Pianissimo"),
    "C51": ("Italian Game", "Giuoco Piano, Evans Accepted, McDonnell Defense"),
    "C53": ("Italian Game", "Main Line, Giuoco Pianissimo"),
    "C54": ("Italian Game", "Giuoco Piano Game, Center Attack"),
    "C55": ("Italian Game", "Anti Fried Liver Defense"),
    "C68": ("Spanish Game", "Morphy Defense, Exchange Variation"),
    "C70": ("Spanish Game", "Morphy Defense, Caro Variation"),
    "C77": ("Spanish Game", "Morphy Defense, Anderssen Variation"),
    "D00": ("Queen's Pawn Opening", "Cigorin Variation"),
    "D02": ("London System", "-"),
    "D30": ("Queen's Gambit", "Declined Variation"),
    "D37": ("Queen's Gambit", "Declined, Three Knights, Harrwitz Attack"),
    "D53": ("Queen's Gambit", "Declined, Modern Variation"),
}

class TimeControlType(enum.Enum):
    UNKNOW = 0
    UNLIMITED = 1
    STANDARD = 2
    RAPID = 3
    BLITZ = 4
    BULLET = 5

class Game:
    def __init__(self, game):
        self.game = game
        self.white_player = self.game.headers["White"]
        self.black_player = self.game.headers["Black"]
        self.result = self.game.headers["Result"]
        self.link = self.game.headers["Link"]
        self.white_elo = self.game.headers["WhiteElo"]
        self.black_elo = self.game.headers["BlackElo"]
        self.start_time = self.__convert_to_local_time(self.game.headers["Date"], self.game.headers["StartTime"])
        self.end_time = self.__convert_to_local_time(self.game.headers["EndDate"], self.game.headers["EndTime"])
        self.time_control = self.__parse_time_control(self.game.headers["TimeControl"])
        self.opening_code = self.game.headers["ECO"]
        self.opening_url = self.game.headers["ECOUrl"]
        opening_name, opening_variation = opening_map.get(self.opening_code, ("Unknown Opening", "Unknown Variation"))
        # Assegna il nome e la variante dell'apertura ai campi della tua classe
        self.opening_name = opening_name if opening_name != "Unknown Opening" else self.opening_code
        self.opening_variation = opening_variation if opening_name != "Unknown Variation" else self.opening_code

    def __convert_to_local_time(self, date_str, time_str):
        # Combina data e ora in un unico formato datetime
        date_time_str = f"{date_str}T{time_str}"
        # Converte la stringa in un oggetto datetime
        date_time_utc = datetime.strptime(date_time_str, "%Y.%m.%dT%H:%M:%S")
        # Aggiunge il timezone UTC alla data e ora
        date_time_utc = date_time_utc.replace(tzinfo=timezone.utc)
        # Converte il timezone in quello locale
        date_time_local = date_time_utc.astimezone()
        return date_time_local

    def __parse_time_control(self, str):
        if (str == "600"):
            return TimeControlType.RAPID
        elif (str=="1/86400"):
            return TimeControlType.STANDARD

        self.black_player = self.game.headers["TimeControl"]

class GameCollection:
    def __init__(self, pgn_file, num_games=None, time_control=None):
        self.games = self.__load_games(pgn_file, num_games, time_control)
        self.games_by_opening = self.__create_opening_map()

    def __load_games(self, pgn_file, num_games=None, time_control=None):
        games = []
        with open(pgn_file) as pgn:
            while True:
                chess_game = chess.pgn.read_game(pgn)
                if chess_game is None:
                    break
                game = Game(chess_game)
                if (time_control is None) or \
                    (time_control=="rapid" and game.time_control == TimeControlType.RAPID) or \
                    (time_control=="standard" and game.time_control == TimeControlType.STANDARD):
                    games.append(game)
                if num_games and len(games) > num_games:
                    break
        return games

    def __create_opening_map(self):
        opening_map = defaultdict(list)
        for game in self.games:
            opening_map[game.opening_name].append(game)
        opening_map = dict(sorted(opening_map.items(), key=lambda item: len(item[1]), reverse=True))
        return opening_map

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.games):
            game = self.games[self.index]
            self.index += 1
            return game
        raise StopIteration