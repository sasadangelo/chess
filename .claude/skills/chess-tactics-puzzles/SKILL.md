---
name: chess-tactics-puzzles
description: Estrae puzzle tattici da sasadangelo.pgn analizzando le partite (soprattutto quelle perse) con Stockfish, individuando i colpi peggiori e generando chessgame/data/tactics_puzzles.csv usato dalla Tactics Gym. Usare quando l'utente chiede di generare/aggiornare i puzzle tattici dalle proprie partite.
---

# Chess Tactics Puzzles

Genera puzzle "trova la mossa" a partire dagli errori reali dell'utente, per allenare esattamente le debolezze individuate nel weakness report (perdita di materiale in mediogioco).

## Prerequisiti

- Richiede Stockfish installato localmente: `which stockfish`. Se manca, installalo con `brew install stockfish` (macOS) prima di procedere.
- Richiede `sasadangelo.pgn` ragionevolmente aggiornato (skill `chess-fetch`).

## Procedura

1. Verifica che Stockfish sia disponibile (`which stockfish`); se assente, installalo e avvisa l'utente.
2. Lancia l'estrazione:
   ```
   python3 extract_puzzles.py --user sasadangelo --output chessgame/data/tactics_puzzles.csv
   ```
   Di default analizza solo le partite perse (dove si concentrano i blunder, per [docs/STUDY_PLAN.md](../../docs/STUDY_PLAN.md)) a profondità 14, segnalando ogni mossa dell'utente con perdita ≥200 centipawn rispetto alla mossa migliore del motore.
3. **Attenzione ai tempi**: l'analisi di centinaia di partite può richiedere 20-40 minuti. Lancia il comando in background e continua altre attività nel frattempo, oppure avvisa l'utente dell'attesa prevista. Per test rapidi usa `--num-games` e `--time-control` per limitare il campione.
4. Al termine, riporta all'utente quanti puzzle sono stati generati, la distribuzione per categoria (Forchetta, Pezzo Appeso, Scoperta, Matto Mancato, Tattica Generica) e per difficoltà (Facile/Media/Difficile).
5. La Tactics Gym (`chessgame/tactics.html`) legge automaticamente il CSV aggiornato: non serve altro passo.

## Note

- Categoria e difficoltà sono euristiche pragmatiche (vedi commenti in [src/model/puzzle_extraction.py](../../src/model/puzzle_extraction.py)), non un rating di puzzle calibrato: bastano per allenamento randomizzato, non per un confronto scientifico tra puzzle.
- `--include-wins` estende l'analisi anche a partite vinte/patte (occasioni tattiche mancate anche quando si vince) — non usato di default per contenere i tempi.
- Rilanciare periodicamente (dopo aver aggiornato le partite con `chess-fetch`) per tenere il pool di puzzle fresco: il file viene sovrascritto a ogni run.
