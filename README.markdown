# Donut SMP Auction Crafting Calculator

Un tool da riga di comando (CLI) sviluppato in Python per calcolare in tempo reale il costo totale di crafting di qualsiasi oggetto di Minecraft basandosi sui prezzi dell'economia del server Donut SMP (donut.auction). 

La vera forza di questo progetto? Nasce per risolvere il problema della recente chiusura dell'API pubblica di Donut SMP. 
Mentre gli altri calcolatori hanno smesso di funzionare, questo script opera in totale indipendenza estraendo i prezzi direttamente dalle pagine web tramite Web Scraping, rendendo di nuovo comodo e automatico il calcolo dei craft per tutti i player.

## Funzionalita' Principali

* Soluzione Post-API: Il programma non ha bisogno dell'API ufficiale per funzionare. Legge in autonomia i dati dal sito simulando un normale utente, garantendo che i calcoli continuino a funzionare nonostante i blocchi lato server.
* Risoluzione ricorsiva delle ricette: Calcola automaticamente l'intero albero di crafting di un oggetto fino ai materiali di base, interfacciandosi con i dataset ufficiali di PrismarineJS.
* Web Scraping in tempo reale: Utilizza Playwright (Chromium headless) per navigare sul sito donut.auction ed estrarre i prezzi minimi aggiornati.
* Multithreading: Implementa un'interfaccia asincrona con barra di caricamento visiva che non blocca l'esecuzione delle richieste di rete.
* Gestione della Cache: Ottimizza i tempi di esecuzione e le risorse di rete memorizzando i prezzi degli oggetti gia' cercati durante la sessione.

## Utilizzo Base (Per chi vuole solo usare il programma)

Se non sei uno sviluppatore e vuoi solo riavere un calcolatore funzionante:
1. Vai nella sezione "Releases" sulla destra di questa pagina GitHub.
2. Scarica l'ultima versione del file `.zip` disponibile.
3. Estrai l'intera cartella contenuta nel file ZIP sul tuo desktop (o dove preferisci).
4. Entra nella cartella estratta, avvia il file `.exe` e segui le istruzioni a schermo. Nessuna configurazione complessa richiesta.

## Installazione per Sviluppatori (Dal codice sorgente)

Per eseguire il codice Python direttamente o per compilarlo, e' necessario avere Python 3.8+ installato.

1. Clona il repository:
   git clone https://github.com/mxrfp/donutSMP-craft-price-founder.git
   cd donutSMP-craft-price-founder

2. Installa le librerie necessarie:
   pip install playwright

3. Installa i browser per Playwright:
   playwright install chromium

4. Avvia lo script principale:
   python nome_del_file.py

## Comandi della CLI e Gestione della Cache

L'applicazione include un sistema di cache per evitare di cercare piu' volte lo stesso oggetto su internet. Di default la cache si svuota a ogni nuova ricerca, ma puo' essere gestita tramite dei comandi appositi.

Attenzione: I comandi vanno inseriti quando viene richiesto il NOME dell'item, non la quantita'.

* --cache c : Svuota completamente la cache corrente.
* --cache k : Dice allo script di mantenere (keep) la cache alla fine della ricerca. Utile se devi cercare di fila piu' oggetti che condividono gli stessi materiali (es. spada di ferro e piccone di ferro).
* --cache !k : Disattiva il mantenimento della cache (ritorna al comportamento di default svuotandola a fine ricerca).
* --cache s : Mostra a schermo il contenuto attuale della cache e i prezzi salvati.
* exit : Chiude il programma in modo sicuro.

## Esempio di esecuzione

----------------------------------------------------------------------------------------------------
                                TROVA PREZZO SU DONUTSMP.AUCTION
----------------------------------------------------------------------------------------------------

[X] Digita il nome dell'item per trovare il prezzo del craft.

----------------------------------------------------------------------------------------------------
Nome dell'item (in inglese) (exit per uscire): diamond pickaxe
Quantita' necessaria di diamond pickaxe (exit per uscire): 1

Cerco prezzo di stick...
|————————————————————| 2.7
Prezzo stick trovato. (0.5$ x 2)

Cerco prezzo di diamond...
|————————————————————| 2.7
Prezzo diamond trovato. (150.0$ x 3)

Prezzo trovato per il craft di diamond pickaxe x 1: 451.0$

## Disclaimer

Questo strumento e' stato creato a scopo puramente didattico, per facilitare i giocatori in seguito alla rimozione delle API. Non e' in alcun modo affiliato, autorizzato o supportato da Donut SMP, donut.auction o Mojang AB. Il software simula semplicemente la normale navigazione web per estrarre informazioni pubbliche.
