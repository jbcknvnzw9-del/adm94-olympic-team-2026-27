# Aggiornamento dati – ADM 94 Olympic Team (DR4 Lombardia, Girone N, 2026/27)

Fonte di verità dei dati: cartella `data/` di questo repository.
Sito pubblico: `index.html` (generato, non modificare a mano) → https://jbcknvnzw9-del.github.io/adm94-olympic-team-2026-27/
Dashboard Claude (copia di lavoro di Mattia): https://claude.ai/artifact/EnWUE5siQhVw5Kzu6r9Xvb

## File
- `data/risultati_girone.csv` – tutte le partite del girone: giornata,data,casa,ospite,punti_casa,punti_ospite,stato,verificato_il. Stato: `Ufficiale`, `Ufficioso`, `Da giocare`. Giornate: andata 1–11, ritorno 12–22.
- `data/partite.csv` – le 22 partite ADM (colonna `stato` = Ufficioso/Ufficiale per le gare giocate; `squadra_fip` = nome avversario come su FIP).
- `data/tabellini.csv`, `data/tabellini_avversari.csv`, `data/roster.csv` – dai referti (non toccare nel controllo automatico).
- `src/dashboard.html` + `src/*.js` – pagina della dashboard; `tools/build.py` genera `index.html`.

## Controllo FIP automatico (domenica sera)
1. Leggere risultati e classifica del girone su FIP (WebFetch):
   https://fip.it/risultati/?group=campionati-regionali&regione_codice=LO&comitato_codice=RLO&sesso=M&codice_campionato=2DM&codice_fase=1&codice_girone=85815
   La pagina mostra una giornata alla volta: controllare la giornata corrente e quelle precedenti con risultati ancora `Ufficioso` (se serve, chiedere a WebFetch le altre giornate o usare i parametri della pagina).
2. Aggiornare `data/risultati_girone.csv`:
   - nuovi risultati → inserire punteggio, stato `Ufficioso` o `Ufficiale` come indicato da FIP;
   - risultati omologati → stato `Ufficiale` (e stesso stato in `data/partite.csv` per le gare ADM);
   - aggiungere le righe delle nuove giornate se mancano; aggiornare `verificato_il` (data odierna) su tutte le righe controllate.
   - NON inventare dati: se FIP non mostra un dato, lasciarlo invariato.
   - Se un risultato ADM su FIP differisce da `data/partite.csv` (che viene dal referto), NON sovrascrivere: segnalarlo nel riepilogo.
3. Se nulla è cambiato tranne `verificato_il`: aggiornare comunque `verificato_il`, rigenerare e pubblicare (così il sito mostra la data dell'ultima verifica).
4. `python3 tools/build.py`, poi commit e push su `main`.
5. Dashboard Claude: per ogni CSV cambiato, caricarlo come asset sull'artifact (Artifact publish con url + asset:true), poi ArtifactData `update` del documento `datasets/<nome senza .csv>` con `source: {kind:"file", url:<nuovo /_blob/...>, name:<file>}` e `updated: {at:<ISO>, by:"Controllo FIP automatico"}` (leggere prima il documento per la `version`).
6. Riepilogo finale breve in italiano per Mattia: cosa è cambiato (nuovi risultati, omologazioni, differenze), o "nessuna novità".
