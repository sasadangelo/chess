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
