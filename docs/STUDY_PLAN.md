# My Study Plan

Piano di studio basato sui [Weakness Report](WEAKNESS_REPORT_Rapid.md) di rapid ([Rapid](WEAKNESS_REPORT_Rapid.md), [Blitz](WEAKNESS_REPORT_Blitz.md), [Daily](WEAKNESS_REPORT_Daily.md)) generati il 2026-08-11 su 200/200/160 partite. Aggiornato dalla skill `chess-study-plan`.

## Priorità immediate

1. **Tattica di base, non nuove aperture.** Nel 70.8% (rapid) e 87.5% (daily) dei casi perdi per resa, quasi sempre dopo aver perso materiale a metà partita — non per un'apertura sbagliata. In [study.md](study.md) esiste un solo studio tattico (Fork): manca copertura di Pin, Skewer, Discovered Attack, Deflection/Removing the Defender. **Azione**: creare questi 4 studi Lichess (stesso formato di [chess-tactics-fork](https://lichess.org/study/Qqx06eH1)) e allenarli con ripetizione (es. Puzzle Rush giornaliero), non solo lettura passiva.
2. **Gestione del tempo in blitz.** Il 47.6% delle sconfitte in blitz è per tempo scaduto — la causa singola più frequente in assoluto su tutti e tre i time control, e sale al 30.4% anche tra le vittorie (segno che giochi spesso al limite del tempo pure quando vinci). Il rating blitz è salito da 549 a 721 nonostante questo: risolvendo la gestione del tempo il tuo livello reale in blitz è probabilmente più alto di quanto il rating mostri. **Azione**: non è uno studio di teoria, è allenamento a giocare più veloce nelle prime 10-15 mosse note ed evitare di pensare a lungo su posizioni semplici.
3. **Repertorio col Nero contro l'Italian Game.** 31.2% win rate su 16 partite in rapid (contro 64.5% quando la giochi tu da Bianco) — è il divario peggiore per volume di dati. In [study.md](study.md) non c'è uno studio dedicato alla difesa col Nero contro l'Italian Game. **Azione**: creare uno studio "Italian Game — difesa col Nero" (es. Two Knights Defense o Hungarian Defense) prima di continuare a giocarla a memoria.
4. **Il Nero è strutturalmente più debole del Bianco.** Il pattern si ripete su tutti i time control: rapid (Italian 31.2%, Bishop's Opening 16.7%), blitz (Irregular Openings 0% su 6, Spanish Game 16.7%, Ponziani 20%, London System 28.6%), daily (Queen's Gambit 16.7%, Spanish Game 25%). Non è un'apertura isolata da sistemare, è la preparazione col Nero in generale che va rinforzata prima del repertorio col Bianco.

## Per time control

- **Rapid**: la causa dominante è il blunder in mediogioco (70.8% resa). Priorità a tattica, non a teoria d'apertura. Rating in leggero calo nella finestra osservata (1101 → 1082 su ~6 settimane, 27/06–09/08): da ricontrollare alla prossima revisione, il campione temporale è corto.
- **Blitz**: la causa dominante è il tempo (47.6% timeout). È l'unico time control dove il problema non è "cosa sai" ma "quanto veloce lo applichi".
- **Daily**: quasi tutto per resa (87.5%), zero per tempo scaduto (prevedibile, hai giorni per mossa). Con tutto quel tempo a disposizione i blunder indicano probabilmente disattenzione tra una mossa e l'altra (partite riprese a distanza di giorni) più che mancanza di calcolo. Vale la pena riguardare le 5 partite corte perse elencate nel report (es. Ponziani in 8 mosse) per capire se sono errori da "mossa fatta di fretta senza rivedere la posizione".

## Repertorio aperture

- **Mantenere**: Italian Game da Bianco — solido su tutti e tre i time control (64.5% rapid, 58.8% blitz, 45.9% daily su campioni ampi, 31-37 partite).
- **Ripassare con priorità**: [Spanish Game](study.md) col Nero (16.7% blitz, 25% daily) e [London System](study.md) col Nero (28.6% blitz) — gli studi esistono già, vanno solo ripresi.
- **Verificare**: Caro-Kann da Bianco (contro 1...c6) ha risultati incoerenti tra time control (57.1% daily, 40% rapid, 28.6% blitz) — lo studio [caro-kann-defense](../caro-kann-defense.pgn) esiste già; il calo in blitz suggerisce che la linea è troppo lunga da ricordare/applicare a tempo veloce, da snellire.
- **Da creare**: repertorio col Nero contro l'Italian Game (vedi priorità 3).

## Prossima revisione

Non a data fissa: rilancia `chess-fetch` + `chess-weakness-report` dopo altre ~50-100 partite giocate per time control (indicativamente 4-6 settimane al ritmo attuale), poi aggiorna questo piano con `chess-study-plan`. Il trend di rating in daily copre oltre 3 anni di partite eterogenee (2023-03 → 2026-06): alla prossima revisione ha senso guardare solo l'ultimo anno per un segnale più affidabile.
