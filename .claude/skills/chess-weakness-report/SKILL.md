---
name: chess-weakness-report
description: Genera i report di debolezza (aperture migliori/peggiori, cause di sconfitta, partite perse rapidamente, trend rating) per rapid, blitz e daily a partire da sasadangelo.pgn, e ne commenta gli insight principali. Usare quando l'utente chiede di analizzare le proprie partite, capire i propri punti deboli/forti, o vuole un report sui progressi.
---

# Chess Weakness Report

Analisi leggera (nessun motore scacchistico) delle debolezze del giocatore, basata su `weakness_report.py` e `src/model/weakness_analysis.py`.

## Cosa misura

- Win rate per apertura, separato per colore (Bianco/Nero), con soglia minima di campione (default 5 partite) per evitare falsi segnali su aperture rare.
- Causa prevalente di sconfitta (`Termination` di chess.com): scacco matto (cecità tattica), tempo scaduto (gestione del tempo), resa (di solito dopo perdita di materiale/blunder).
- Partite perse in poche mosse (default: meno di 15 mosse piene) — spia di trappole d'apertura o blunder precoci.
- Trend del rating nel periodo coperto dalle partite analizzate.

## Procedura

1. Assicurati che `sasadangelo.pgn` sia ragionevolmente aggiornato (se l'utente non ha specificato altrimenti e sono passate settimane dall'ultimo aggiornamento, considera di suggerire/eseguire prima la skill `chess-fetch`).
2. Lancia il report per ciascun time control disponibile:
   ```
   python3 weakness_report.py --user sasadangelo --num-games 200 --time-control rapid    --output docs/WEAKNESS_REPORT_Rapid.md
   python3 weakness_report.py --user sasadangelo --num-games 200 --time-control blitz    --output docs/WEAKNESS_REPORT_Blitz.md
   python3 weakness_report.py --user sasadangelo --num-games 200 --time-control standard --output docs/WEAKNESS_REPORT_Daily.md
   ```
   (`standard` è il valore usato internamente dal codice per le partite "daily" di chess.com.)
3. Leggi i file generati (non limitarti a dire "fatto"): estrai e commenta all'utente in linguaggio naturale i 3-4 insight più significativi per ciascun time control — es. "il 70% delle tue sconfitte in rapid sono per resa dopo aver perso materiale, probabile blunder in mediogioco piuttosto che problema di apertura", oppure "in blitz perdi spesso per tempo scaduto: è un problema di gestione del tempo, non di forza di gioco".
4. Se un time control ha troppo poche partite per un'analisi affidabile (es. meno di ~15-20), dillo esplicitamente invece di presentare percentuali fuorvianti.

## Note

- I report sono file markdown in `docs/`, coerenti con lo stile dei `REPORT_*.md` già esistenti (generati da `report.py`).
- Questa analisi è "no engine": non individua blunder specifici mossa per mossa né temi tattici precisi. Per quello serve una futura skill basata su Stockfish (roadmap, non ancora implementata).
