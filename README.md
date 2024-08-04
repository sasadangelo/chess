# Lichess studies in PDF

The goal of this project is to create a software that convert all my Lichess study in PDF format. Lichess is a Chess platform that allows you to create study plan of your Chess games. I use it to collect all my studies about openings, end games, tacticts, and so on.
Once this studies are ready I will convert them in PDF using this project.

## My Chess Studies

### Introduction

1. **What is Chess?**: [Lichess study](https://lichess.org/study/IJpFEM89) | [PDF](studies/what-is-chess.pdf) | [Tex](studies/what-is-chess.tex) | [PGN](studies/what-is-chess.pgn) | [Images](studies/what-is-chess)
2. **Chess Notation**: [Lichess study](https://lichess.org/study/ezdKJ7Di) | [PDF](studies/chess-notation.pdf) | [Tex](studies/chess-notation.tex) | [PGN](studies/chess-notation.pgn) | [Images](studies/chess-notation)

### Openings

1. **Openings Goals and Principles**: [Lichess study](https://lichess.org/study/IreRnAsc) | [PDF](studies/openings_goals_and_principles.pdf) | [Tex](studies/openings_goals_and_principles.tex) | [PGN](studies/openings_goals_and_principles.pgn) | [Images](studies/openings_goals_and_principles)
2. **Italian Game**: [Lichess study](https://lichess.org/study/tVbAc09e) | [PDF](studies/italian_game.pdf) | [Tex](studies/italian_game.tex) | [PGN](studies/italian_game.pgn) | [Images](studies/italian_game)
3. **Spanish Game**: [Lichess study](https://lichess.org/study/Lml6kbni) | [PDF](studies/spanish_game.pdf) | [Tex](studies/spanish_game.tex) | [PGN](studies/spanish_game.pgn) | [Images](studies/spanish_game)
4. **London System**: [Lichess study](https://lichess.org/study/J5o5RnFr) | [PDF](studies/london-system.pdf) | [Tex](studies/london-system.tex) | [PGN](studies/london-system.pgn) | [Images](studies/london-system)
5. **Wayward Queen Attack**: [Lichess study](https://lichess.org/study/ZDzazKo4/azKz8Qpl) | [PDF](studies/wayward-queen-attack.pdf) | [Tex](studies/wayward-queen-attack.tex) | [PGN](studies/wayward-queen-attack.pgn) | [Images](studies/wayward-queen-attack)

### Middle game

#### Tactics

1. **Fork**: [Lichess study](https://lichess.org/study/Qqx06eH1) | [PDF](studies/chess-tactics-fork.pdf) | [Tex](studies/chess-tactics-fork.tex) | [PGN](studies/chess-tactics-fork.pgn) | [Images](studies/chess-tactics-fork)

### End games

1. **Queen vs King End Game**: [Lichess study](https://lichess.org/study/9RJZi3rc) | [PDF](studies/queen_vs_king_endgame.pdf) | [Tex](studies/queen_vs_king_endgame.tex) | [PGN](studies/queen_vs_king_endgame.pgn) | [Images](studies/queen_vs_king_endgame)
2. **Two Rooks vs King End Game**: [Lichess study](https://lichess.org/study/w4XIVyGB) | [PDF](studies/two_rooks_king_end_game.pdf) | [Tex](studies/two_rooks_king_end_game.tex) | [PGN](studies/two_rooks_king_end_game.pgn) | [Images](studies/two_rooks_king_end_game)
3. **Rook vs King End Game**: [Lichess study](https://lichess.org/study/IJ2Eu2as) | [PDF](studies/rook_vs_king_end_game.pdf) | [Tex](studies/rook_vs_king_end_game.tex) | [PGN](studies/rook_vs_king_end_game.pgn) | [Images](studies/rook_vs_king_end_game)
4. **Two Bishops vs King End Game**: [Lichess study](https://lichess.org/study/4MXMBxiS) | [PDF](studies/two-bishops-vs-king-end-game.pdf) | [Tex](studies/two-bishops-vs-king-end-game.tex) | [PGN](studies/two-bishops-vs-king-end-game.pgn) | [Images](studies/two-bishops-vs-king-end-game)
5. **King and Pawn vs King End Game**: [Lichess study](https://lichess.org/study/gHnlsY1u) | [PDF](studies/king-pawn-vs-king-endgame.pdf) | [Tex](studies/king-pawn-vs-king-endgame.tex) | [PGN](studies/king-pawn-vs-king-endgame.pgn) | [Images](studies/king-pawn-vs-king-endgame)

## How to grab your games

Here the instructions to create the statistics of your games:

1. Download the code with the command:
```
git clone https://github.com/sasadangelo/gamegrab
cd gamegrab
```

2. Create a virtual environment and install dependencies:
```
python3 -m venv venv
source venv/bin/activate
```

3. Grab your games from Chess.com:
```
python3 gamegrab.py --num-games=100 --time-class=rapid --outfile=sasadangelo.pgn sasadangelo
```

this command download the recent 100 rapid games of the Chess.com sasadangelo user.

4. Create a report of your games:
```
python3 report.py --num-games=100 --time-class=rapid --outfile=sasadangelo.pgn sasadangelo
```

## My Recent Games

Go to the following pages to see my recent games:
* [Rapid Games](docs/REPORT_Rapid.md).
* [Daily Games](docs/REPORT_Standard.md).
