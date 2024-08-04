from docopt import docopt
import sys
import os
from src.model.chess_platform import ChessComPlatform

def main(arguments):
    username = arguments['USERNAME']
    outfile = arguments['--outfile'] if arguments['--outfile'] else f'{username}.pgn'
    time_class = arguments['--time-class']
    color = arguments['--color'].lower() if arguments.get('--color') else None
    since = arguments['--since']
    num_games = int(arguments['--num-games']) if arguments['--num-games'] else None

    chess_com = ChessComPlatform()
    chess_com.download(username, outfile, time_class, color, since, num_games)

if __name__ == "__main__":
    doc = """gamegrab.
        Usage:
        gamegrab.py [--time-class=TC] [--outfile=OUTFILE] [--color=COLOR] [--since=YYYYMM] [--num-games=NUMGAMES] USERNAME
        gamegrab.py (-h | --help)

        Options:
        --time-class=TC       Only download games of specified time control.
        --outfile=OUTFILE     Name of outputfile (defaults to USERNAME.pgn).
        --color=COLOR         Download games of specific color.   
        --num-games=NUMGAMES  Download only this many recent games.
        --since=YYYYMM        Only download games on or after given year and month.
        -h --help             Show this screen.

        Arguments:
        USERNAME      username to download games
    """

    arguments = docopt(doc)
    main(arguments)