import requests

class ChessPlatform:
    def download(self, username, output_file='games.pgn', time_class=None, color=None, since=None, num_games=None):
        raise NotImplementedError("Subclasses must implement download method")

CHESSCOM_HEADERS = { \
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' \
}

class ChessComPlatform(ChessPlatform):
    def download(self, username, output_file='games.pgn', time_class=None, color=None, since=None, num_games=None):
        print(output_file)
        with open(output_file, 'w') as f:
            url = f"https://api.chess.com/pub/player/{username}/games/archives"
            response = requests.get(url, headers=CHESSCOM_HEADERS)
            print(response.status_code)
            if response.status_code == 200:
                print(url)
                archives = response.json()['archives'][::-1]  # Reverse to start from the latest games
                game_ctr = 0
                for archive_url in archives:
                    if since:
                        archive_year, archive_month = map(int, archive_url.split('/')[-2:])
                        if (archive_year, archive_month) < since:
                            continue
                    print(f"Downloading games from {archive_url}...", flush=True)
                    archive_response = requests.get(archive_url, headers=CHESSCOM_HEADERS)
                    if archive_response.status_code == 200:
                        games = archive_response.json()['games'][::-1]  # Reverse to start from the latest games
                        for game in games:
                            if (time_class is None or game['time_class'] == time_class) and \
                               (color is None or game[color]['username'].lower() == username.lower()):
                                try:
                                    f.write(game['pgn'])
                                    f.write('\n\n')
                                    game_ctr += 1
                                    if num_games and game_ctr >= num_games:
                                        print(f"Downloaded {game_ctr} games.")
                                        return
                                except UnicodeEncodeError:
                                    print('UnicodeEncodeError, skipping game.')
                                    continue
                print(f"Downloaded {game_ctr} games.")
            else:
                print("Failed to fetch game archives")

class LichessPlatform(ChessPlatform):
    def download(self, username, output_file='games.pgn', time_class=None, color=None, since=None, num_games=None):
        # Logic to download games from Lichess platform
        pass  # Placeholder, implement Lichess game download logic here
