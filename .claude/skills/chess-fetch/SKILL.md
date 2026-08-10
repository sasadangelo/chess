---
name: chess-fetch
description: Scarica/aggiorna le partite chess.com dell'utente (rapid, blitz, daily) in sasadangelo.pgn. Usare quando l'utente chiede di aggiornare, scaricare, sincronizzare o rinfrescare le proprie partite prima di un'analisi.
---

# Chess Fetch

Aggiorna il file `sasadangelo.pgn` alla radice del repo con le partite più recenti da chess.com, per tutti e tre i time control seguiti dall'utente: rapid, blitz, daily.

## Perché non basta un singolo `gamegrab.py` senza filtri

`gamegrab.py` scrive in modalità overwrite (`open(output_file, 'w')`), quindi una singola chiamata senza `--time-class` prende semplicemente le ultime N partite di qualsiasi tipo — se l'utente ha giocato molto rapid di recente, blitz e daily restano scoperti. Per garantire copertura di tutti e tre i time control bisogna scaricarli separatamente e poi unirli.

## Procedura

1. Scarica separatamente ciascun time control in file temporanei (usa lo scratchpad, non `/tmp` del sistema se disponibile un percorso di scratch):
   ```
   python3 gamegrab.py --time-class=rapid --outfile=<scratch>/rapid.pgn --num-games=200 sasadangelo
   python3 gamegrab.py --time-class=blitz --outfile=<scratch>/blitz.pgn --num-games=200 sasadangelo
   python3 gamegrab.py --time-class=daily --outfile=<scratch>/daily.pgn --num-games=200 sasadangelo
   ```
2. Concatena i tre file in `sasadangelo.pgn` (sovrascrivendo il file esistente):
   ```
   cat <scratch>/rapid.pgn <scratch>/blitz.pgn <scratch>/daily.pgn > sasadangelo.pgn
   ```
3. Verifica il risultato contando le partite per time control, ad es.:
   ```
   grep -c '\[Event' sasadangelo.pgn
   grep -o '\[TimeControl "[^"]*"\]' sasadangelo.pgn | sort | uniq -c
   ```
4. Riporta all'utente quante partite sono state scaricate per ciascun time control e da quando (data della partita più vecchia/più recente).

Se l'utente ha un username chess.com diverso da `sasadangelo`, adatta username e nome file di conseguenza (il resto della pipeline — `report.py`, `weakness_report.py` — assume `<username>.pgn`).
