from datetime import datetime, timezone
from collections import defaultdict
import enum
import chess.pgn

# Definisci la mappa con codice di apertura come chiave e tupla di (nome apertura, variante apertura) come valore
opening_map = {
    "A00": ("Irregular Openings", "Uncommon Opening"),
    "A01": ("Nimzowitsch-Larsen Attack", "Nimzowitsch-Larsen Variation"),
    "A02": ("Bird's Opening", ""),
    "A03": ("Bird's Opening", "Dutch Variation"),
    "A04": ("Reti Opening", ""),
    "A05": ("Reti Opening", "1...Nf6"),
    "A06": ("Reti Opening", "1...d5"),
    "A07": ("Reti Opening", "King's Indian Attack (Barcza System)"),
    "A08": ("Reti Opening", "King's Indian Attack"),
    "A09": ("Reti Opening", "(properly))"),
    "A10": ("English Opening", "-"),
    "A11": ("English Opening", "Caro-Kann defensive system"),
    "A12": ("English Opening", "Caro-Kann defensive system"),
    "A13": ("English Opening", "1...e6"),
    "A14": ("English Opening", "Neo-Catalan Declined"),
    "A15": ("English Opening", "Anglo-Indian Defence"),
    "A16": ("English Opening", "Anglo-Indian Defence"),
    "A17": ("English Opening", "Hedgehog Defence"),
    "A18": ("English Opening", "Mikenas-Carls Variation"),
    "A19": ("English Opening", "Mikenas-Carls, Sicilian Variation"),
    "A20": ("English Opening", "1...e5"),
    "A21": ("English Opening", "1...e5 2.Nc3"),
    "A22": ("English Opening", "Two Knights Variation"),
    "A23": ("English Opening", "Bremen System, Keres Variation"),
    "A24": ("English Opening", "Bremen System with 1...e5 2.Nc3 Nf6 3.g3 g6"),
    "A25": ("English Opening", "Sicilian Reversed"),
    "A26": ("English Opening", "Closed System"),
    "A27": ("English Opening", "Three Knights System"),
    "A28": ("English Opening", "Four Knights System"),
    "A29": ("English Opening", "Four Knights, Kingside Fianchetto"),
    "A30": ("English Opening", "Symmetrical Defence"),
    "A31": ("English Opening", "Symmetrical, Benoni formation"),
    "A32": ("English Opening", "Symmetrical: 1...c5 2.Nf3 Nf6 3.d4 cxd4 4.Nxd4 e6"),
    "A33": ("English Opening", "Symmetrical: 1...c5 2.Nf3 Nf6 3.d4 cxd4 4.Nxd4 e6 5.Nc3 Nc6"),
    "A34": ("English Opening", "Symmetrical: 1...c5 2.Nc3"),
    "A35": ("English Opening", "Symmetrical: 1...c5 2.Nc3 Nc6"),
    "A36": ("English Opening", "Symmetrical: 1...c5 2.Nc3 Nc6 3.g3"),
    "A37": ("English Opening", "Symmetrical: 1...c5 2.Nc3 Nc6 3.g3 g6 4.Bg2 Bg7 5.Nf3"),
    "A38": ("English Opening", "Symmetrical: 1...c5 2.Nc3 Nc6 3.g3 g6 4.Bg2 Bg7 5.Nf3 Nf6"),
    "A39": ("English Opening", "Symmetrical, Main line"),
    "B00": ("Nimzowitsch Defense", "Scandinavian, Bogoljubov, Vehre Variation"),
    "B01": ("Scandinavian Defense", "Mieses-Kotrč, Main Line, Lasker Variation"),
    "B02": ("Alekhine's Defense", "-"),
    "B03": ("Alekhine's Defense", "3. d4"),
    "B04": ("Alekhine's Defense", "Modern Variation"),
    "B05": ("Alekhine's Defense", "Modern Variation, 4...Bg4"),
    "B07": ("Pirc Defense", "-"),
    "B08": ("Pirc Defense", "Classical Variation"),
    "B09": ("Pirc Defense", "Austrian Attack"),
    "B10": ("Caro-Kann Defense", "-"),
    "B11": ("Caro-Kann Defense", "Two knights, 3...Bg4"),
    "B12": ("Caro-Kann Defense", "-"),
    "B13": ("Caro-Kann Defense", "Exchange Variation"),
    "B14": ("Caro-Kann Defense", "Panov-Botvinnik Attack, 5...e6"),
    "B15": ("Caro-Kann Defense", "Campomanes Attack"),
    "B16": ("Caro-Kann Defense", "Bronstein-Larsen Variation"),
    "B17": ("Caro-Kann Defense", "Steinitz Variation, Smyslov Systems"),
    "B18": ("Caro-Kann Defense", "Classical Variation"),
    "B19": ("Caro-Kann Defense", "Classical, 7...Nd7"),
    "B20": ("Sicilian Defense", "-"),
    "B21": ("Sicilian Defense", "Grand Prix Attack"),
    "B22": ("Sicilian Defense", "Alapin Variation"),
    "B23": ("Sicilian Defense", "Closed, 2.Nc3"),
    "B24": ("Sicilian Defense", "Closed, 2.Nc3 Nc6 3.g3"),
    "B25": ("Sicilian Defense", "Closed, 2.Nc3 Nc6 3.g3 g6 4.Bg2 Bg7 5.d3 d6"),
    "B26": ("Sicilian Defense", "Closed, 6.Be3"),
    "B27": ("Sicilian Defense", "2.Nf3"),
    "B28": ("Sicilian Defense", "O'Kelly Variation"),
    "B29": ("Sicilian Defense", "Nimzovich-Rubinstein Variation"),
    "B30": ("Sicilian Defense", "Open Variation"),
    "B31": ("Sicilian Defense", "Nimzovich-Rossolimo Attack"),
    "B32": ("Sicilian Defense", "Open, Franco-Sicilian Variation"),
    "B33": ("Sicilian Defense", "Open Variation"),
    "B34": ("Sicilian Defense", "Open, Accelerated Dragon, Exchange Variation"),
    "B40": ("Sicilian Defense", "Paulsen-Basman Defense"),
    "C00": ("French Defense", "Normal Variation"),
    "C20": ("King's Pawn Opening", "-"),
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
    "C50": ("Italian Game", "-"),
    "C51": ("Italian Game", "Giuoco Piano, Evans Gambit"),
    "C52": ("Italian Game", "Giuoco Piano, Evans Gambit Accepted, Main Line"),
    "C53": ("Italian Game", "Giuoco Piano, Main Line"),
    "C54": ("Italian Game", "Giuoco Piano, Center Attack"),
    "C55": ("Italian Game", "Two Knights Defense"),
    "C56": ("Italian Game", "Two Knights Defense"),
    "C57": ("Italian Game", "Two Knights Defense"),
    "C58": ("Italian Game", "Two Knights Defense"),
    "C59": ("Italian Game", "Two Knights Defense"),
    "C60": ("Spanish Game", "-"),
    "C61": ("Spanish Game", "Bird's Defense"),
    "C62": ("Spanish Game", "Old Steiniz Defense"),
    "C63": ("Spanish Game", "Schliemann Defence"),
    "C64": ("Spanish Game", "Classical (Cordel) Defence"),
    "C65": ("Spanish Game", "Berlin Defence"),
    "C66": ("Spanish Game", "Berlin Defence"),
    "C67": ("Spanish Game", "Berlin Defence"),
    "C68": ("Spanish Game", "Morphy Defence, Exchange Variation"),
    "C69": ("Spanish Game", "Morphy Defence, Exchange Variation"),
    "C70": ("Spanish Game", "Morphy Defence, Caro Variation"),
    "C71": ("Spanish Game", "Modern Steinitz Defence"),
    "C72": ("Spanish Game", "Modern Steinitz Defence"),
    "C73": ("Spanish Game", "Modern Steinitz Defence"),
    "C74": ("Spanish Game", "Modern Steinitz Defence"),
    "C75": ("Spanish Game", "Modern Steinitz Defence"),
    "C76": ("Spanish Game", "Modern Steinitz Defence"),
    "C77": ("Spanish Game", "Morphy Defense"),
    "C78": ("Spanish Game", "5. O-O"),
    "C79": ("Spanish Game", "Steinitz Defence Deferred (Russian Defence)"),
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

class ResultGame(enum.Enum):
    WIN = 0
    LOSE = 1
    DRAW = 2

class Game:
    def __init__(self, username, game):
        self.game = game
        self.white_player = self.game.headers["White"]
        self.black_player = self.game.headers["Black"]
        self.link = self.game.headers["Link"]
        self.white_elo = self.game.headers["WhiteElo"]
        self.black_elo = self.game.headers["BlackElo"]
        self.start_time = self.__convert_to_local_time(self.game.headers["Date"], self.game.headers["StartTime"])
        self.end_time = self.__convert_to_local_time(self.game.headers["EndDate"], self.game.headers["EndTime"])
        self.time_control = self.__parse_time_control(self.game.headers["TimeControl"])
        self.opening_code = self.game.headers.get("ECO", "A00")
        self.opening_url = self.game.headers.get("ECOUrl", "")
        opening_name, opening_variation = opening_map.get(self.opening_code, ("Unknown Opening", "Unknown Variation"))
        # Assegna il nome e la variante dell'apertura ai campi della tua classe
        self.opening_name = opening_name if opening_name != "Unknown Opening" else self.opening_code
        self.opening_variation = opening_variation if opening_name != "Unknown Variation" else self.opening_code
        if self.game.headers["Result"] == "1/2-1/2":
            self.result = ResultGame.DRAW
        elif (self.white_player == username and self.game.headers["Result"] == "1-0") or (self.black_player == username and self.game.headers["Result"] == "0-1"):
            self.result = ResultGame.WIN
        else:
            self.result = ResultGame.LOSE

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
    def __init__(self, username, num_games=None, time_control=None, color=None):
        self.total_games = 0;
        self.win_games = 0;
        self.lost_games = 0;
        self.draw_games = 0;
        self.games = self.__load_games(username, num_games, time_control, color)
        self.games_by_opening = self.__create_opening_map()

    def __load_games(self, username, num_games=None, time_control=None, color=None):
        games = []
        pgn_file = username + ".pgn"
        with open(pgn_file) as pgn:
            while True:
                chess_game = chess.pgn.read_game(pgn)
                if chess_game is None:
                    break
                game = Game(username, chess_game)
                if ((time_control is None) or \
                    (time_control=="rapid" and game.time_control == TimeControlType.RAPID) or \
                    (time_control=="standard" and game.time_control == TimeControlType.STANDARD)) and \
                   (color is None or \
                    (color == "white" and game.white_player == username) or \
                    (color == "black" and game.black_player == username)):
                    self.total_games+=1
                    if game.result == ResultGame.WIN:
                        self.win_games+=1
                    if game.result == ResultGame.LOSE:
                        self.lost_games+=1
                    if game.result == ResultGame.DRAW:
                        self.draw_games+=1
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
