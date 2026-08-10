# Salvatore D'Angelo Chess

The goal of this project is to create a software that help me to improve in Chess. The core of this software is the Chess Gym a HTML, CSS, and Javascript website where I can train myself with Opening, Tacticts, End Games, etc. This project contains also my recent games organized by openings updated monthly automatically via GitHub actions. Finally, it contains also all my Lichess study in PDF format. Lichess is a Chess platform that allows you to create study plan of your Chess games. I use it to collect all my studies about openings, end games, tacticts, and so on. Once this studies are ready I will convert them in PDF using this project.

## My Chess Gym

Go to the following [link](https://sasadangelo.github.io/chess) to find my Chess Gym.

## My Chess Studies

Go to the following pages to see my recent studies and exercises:
* [My Chess Studies](docs/study.md).
* [My Exercises](docs/exercises.md).

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
* [Rapid Games (White)](docs/REPORT_Rapid_White.md).
* [Rapid Games (Black)](docs/REPORT_Rapid_Black.md).
* [Daily Games](docs/REPORT_Standard.md).
* [Daily Games (White)](docs/REPORT_Standard_White.md).
* [Daily Games (Black](docs/REPORT_Standard_Black.md).

## Weakness analysis and study plan

Beyond the win/loss report above, this project includes a lightweight (no chess engine) weakness analysis: win rate per opening and color, prevailing cause of loss (checkmate vs timeout vs resignation, from chess.com's `Termination` header), games lost in very few moves, and rating trend. Generate it with:

```
python3 weakness_report.py --user sasadangelo --num-games 200 --time-control rapid --output docs/WEAKNESS_REPORT_Rapid.md
```

(`--time-control` accepts `rapid`, `blitz`, `bullet`, `standard` for daily games.)

Three Claude Code skills wrap this workflow end to end:
* **chess-fetch** — refreshes `sasadangelo.pgn` with the latest rapid/blitz/daily games from chess.com.
* **chess-weakness-report** — regenerates the weakness reports for each time control and summarizes the key findings.
* **chess-study-plan** — turns the weakness reports into a prioritized study plan in `docs/STUDY_PLAN.md`, linking each weakness to existing [studies](docs/study.md) and [exercises](docs/exercises.md) or flagging new ones to create.

## Tactics Gym

The [Chess Gym](https://sasadangelo.github.io/chess/chessgame/index.html) also includes a **Tactics Gym** (`chessgame/tactics.html`): puzzles generated directly from my own games with Stockfish, not a generic puzzle set. It finds the moves where I lost the most material (mostly in lost games, where the [study plan](docs/STUDY_PLAN.md) shows blunders concentrate), tags each one with a difficulty (Facile/Media/Difficile, based on how large the mistake was) and a rough tactical category (Forchetta, Pezzo Appeso, Scoperta, Matto Mancato, or a generic fallback), and serves them one at a time in random order — the same puzzle never repeats twice in a row — so I can't just memorize a fixed sequence. Each puzzle links back to the original game for context.

Regenerate the puzzle pool (requires `brew install stockfish` locally, and takes 20-40 minutes over hundreds of games):

```
python3 extract_puzzles.py --user sasadangelo --output chessgame/data/tactics_puzzles.csv
```

Or via the **chess-tactics-puzzles** skill, which wraps this and reports the resulting category/difficulty breakdown.

## Endgame library

`chessgame/data/end_games.csv` also includes hand-transcribed positions from Jeremy Silman's *Complete Endgame Course*, starting with the "Class E (1000-1199)" chapter — matching my current rapid/daily rating — covering minor-piece-vs-queen technique, king opposition, and rook-pawn endgames.

## Allenamento giornaliero (ripetizione spaziata)

`chessgame/training.html` combina endgame e puzzle tattici in un'unica sessione quotidiana, in stile Anki: ogni elemento (endgame o puzzle) ha una propria pianificazione a ripetizione spaziata (algoritmo SM-2 semplificato, `chessgame/js/srs.js`) — se lo sbagli torna a distanza di un giorno, se lo risolvi bene l'intervallo cresce (1 giorno, poi 6, poi via via più lungo). Ogni giorno vengono proposti solo gli elementi "dovuti" (mai visti, o con data di ripasso scaduta), fino a un massimo configurabile per endgame e per puzzle, mescolati in ordine casuale.

Per gli endgame (giocati liberamente in sandbox contro Stockfish, senza una sequenza di mosse "corretta" univoca) il successo è rilevato automaticamente confrontando l'esito reale della partita con l'`Objective` (`Win`/`Draw`) di quella posizione — colonna aggiunta a `chessgame/data/end_games.csv` valutando ogni FEN con Stockfish a profondità 22 (`label_endgame_objectives.py`; per posizioni con così pochi pezzi equivale in pratica a un tablebase). Per i puzzle tattici il segnale è già nativo (mossa corretta al primo tentativo, dopo un tentativo sbagliato, o soluzione mostrata).

**Limite noto**: lo stato della ripetizione spaziata vive solo in `localStorage` del browser usato — nessuna sincronizzazione tra dispositivi diversi, scelta deliberata per non introdurre un backend su un sito oggi completamente statico (GitHub Pages).

Per rigenerare la colonna `Objective` dopo aver aggiunto nuovi endgame:
```
python3 label_endgame_objectives.py          # dry-run, stampa un report da controllare
python3 label_endgame_objectives.py --apply  # scrive la colonna nel CSV
```

## Roadmap

A future `chess-engine-analysis` skill will extend the weakness report itself with Stockfish-based move-by-move blunder detection (today's weakness report works from game metadata only — opening, result, termination reason, move count — not engine evaluation; that gap is now partly covered by the Tactics Gym above, but not yet folded back into `docs/WEAKNESS_REPORT_*.md`).
