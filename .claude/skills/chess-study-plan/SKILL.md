---
name: chess-study-plan
description: Trasforma i report di debolezza in un piano di studio concreto in docs/STUDY_PLAN.md, collegando ogni debolezza rilevata alle risorse già presenti nel repo (Lichess studies, esercizi) o proponendone di nuove. Usare quando l'utente chiede una strategia/piano di miglioramento, cosa studiare, o su cosa concentrarsi.
---

# Chess Study Plan

Non è uno script: è un compito di sintesi. Leggi i dati e produci un piano prioritizzato e azionabile, non un riassunto generico.

## Input da leggere

1. `docs/WEAKNESS_REPORT_Rapid.md`, `docs/WEAKNESS_REPORT_Blitz.md`, `docs/WEAKNESS_REPORT_Daily.md` (generati dalla skill `chess-weakness-report`; se mancano o sono vecchi, eseguila prima).
2. `docs/study.md` — l'indice degli studi Lichess già disponibili (aperture, tattica, finali).
3. `docs/exercises.md` — esercizi di finale già pronti.
4. `docs/STUDY_PLAN.md` se esiste già, per aggiornarlo invece di ripartire da zero (mantieni cosa ha già iniziato/completato l'utente, se annotato).

## Come collegare debolezze → azioni

Per ogni debolezza ricorrente identificata nei weakness report, individua l'azione più specifica possibile:

- **Apertura specifica con win rate basso** (es. "Two Knights Defense, Nero, 30%") → verifica se esiste già uno studio in `docs/study.md` per quell'apertura/variante: se sì, va ripassato; se no, va segnalato come nuovo studio da creare (l'utente usa Lichess per crearli e poi convertirli in PDF con questo repo).
- **Molte sconfitte per resa** → di solito significa blunder/perdita di materiale in mediogioco: priorità ad allenamento tattico (pattern recognition), non a nuove aperture.
- **Molte sconfitte per scacco matto** → cecità su minacce dirette al re: priorità a esercizi di difesa/calcolo, controllo delle minacce dell'avversario prima di muovere.
- **Molte sconfitte per tempo scaduto** (soprattutto se concentrate in un time control) → non è un problema di forza scacchistica ma di gestione del tempo/velocità decisionale: suggerisci esercizi a tempo o revisione del ritmo di gioco in quel time control specifico, non nuovo materiale di studio.
- **Partite perse in poche mosse** → guarda le aperture coinvolte: se ricorrono, è un buco di repertorio da chiudere con priorità alta (sono i punti persi più "a buon mercato" da recuperare).
- **Finali**: i weakness report attuali non isolano ancora gli errori di finale (serve l'analisi motore, non ancora implementata) — per ora basati sulle partite lunghe perse e su quanto materiale residuo aveva la posizione, se osservabile dal link della partita, altrimenti segnala il finale come area da tracciare meglio in futuro.

## Struttura di `docs/STUDY_PLAN.md`

1. **Priorità immediate** (2-4 voci): le debolezze con impatto maggiore sul win rate complessivo, con azione concreta e link alla risorsa esistente o nota "da creare".
2. **Per time control**: cosa cambia tra rapid/blitz/daily (es. in blitz il problema è il tempo, in daily è la profondità di preparazione d'apertura).
3. **Repertorio aperture**: cosa tenere, cosa sostituire, con riferimento a `docs/study.md`.
4. **Prossima revisione**: quando ripetere l'analisi (suggerisci: dopo altre ~50-100 partite giocate, non a data fissa, perché è il volume di dati che rende l'analisi affidabile).

Scrivi il piano in italiano, conciso e concreto — niente slide motivazionali, solo cosa fare e perché, con riferimento ai numeri reali del weakness report.
