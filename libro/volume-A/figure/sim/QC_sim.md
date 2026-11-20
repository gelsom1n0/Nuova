# Controllo automatico dei tracciati simulati

Generato da `genera_sim.py`. Le misure sono calcolate da `common/ecgmeasure.py` sul segnale simulato, come se fosse un tracciato sconosciuto (QRS rilevati, battito mediano, metodo della tangente per il QT). Precisione attesa ±10–20 ms. Il controllo automatico **non sostituisce** la revisione clinica (stato di tutti i tracciati: `da_validare`).

| ID | Titolo | Affidabilità | FC | RR CV | PR ms | QRS ms | QTc ms | P | Esito | Criteri falliti |
|---|---|---|---|---|---|---|---|---|---|---|
| SIM-RS-01 | Ritmo sinusale normale (12 derivazioni) | alta | 71.9 | 0.003 | 154 | 100 | 413 | sì | superato | — |
| SIM-RS-02 | Ritmo sinusale normale (striscia II) | alta | 71.9 | 0.003 | 154 | 100 | 413 | sì | superato | — |
| SIM-RS-03 | Tachicardia sinusale | alta | 125.0 | 0.003 | 141 | 97 | 453 | sì | superato | — |
| SIM-RS-04 | Bradicardia sinusale | alta | 46.0 | 0.002 | 168 | 100 | 382 | sì | superato | — |
| SIM-RS-05 | Aritmia sinusale respiratoria | alta | 66.9 | 0.092 | 155 | 100 | 407 | sì | superato | — |
| SIM-EX-01 | Extrasistole atriale | alta | 72.0 | 0.121 | 154 | 100 | 413 | sì | superato | — |
| SIM-EX-02 | Extrasistole giunzionale | media | 72.0 | 0.135 | 154 | 100 | 413 | sì | superato | — |
| SIM-EX-03 | Extrasistole ventricolare isolata | alta | 72.0 | 0.273 | 154 | 100 | 413 | sì | superato | — |
| SIM-EX-04 | Bigeminismo ventricolare | alta | 36.0 | 0.0 | 167 | 99 | 492 | sì | superato | — |
| SIM-FA-01 | Fibrillazione atriale a risposta ventricolare elevata | media | 106.6 | 0.184 | None | 99 | 442 | no | superato | — |
| SIM-FA-02 | Fibrillazione atriale a risposta controllata | media | 81.6 | 0.191 | None | 99 | 407 | no | superato | — |
| SIM-FL-01 | Flutter atriale con conduzione 2:1 | media | 150.0 | 0.0 | 56 | 96 | 538 | sì | superato | — |
| SIM-FL-02 | Flutter atriale con conduzione 4:1 | media | 75.0 | 0.0 | 54 | 98 | 400 | sì | superato | — |
| SIM-TSV-01 | Tachicardia da rientro nodale (TSV) | media | 182.4 | 0.002 | 201 | 96 | 481 | sì | superato | — |
| SIM-TV-01 | Tachicardia ventricolare monomorfa | media | 170.0 | 0.002 | 190 | 173 | 586 | sì | superato | — |
| SIM-TdP-01 | Torsione di punta | schematica | None | None | None | None | None | no | superato | — |
| SIM-FV-01 | Fibrillazione ventricolare a onde ampie | schematica | 69.2 | 0.585 | None | 234 | 763 | no | superato | — |
| SIM-FV-02 | Fibrillazione ventricolare a onde fini | schematica | 87.4 | 0.588 | None | 152 | 578 | no | superato | — |
| SIM-AS-01 | Asistolia | alta | 17.1 | 0.012 | None | 49 | 72 | no | superato | — |
| SIM-AS-02 | Asistolia ventricolare con onde P | alta | 45.0 | 0.001 | None | 113 | 574 | no | superato | — |
| SIM-BAV-01 | Blocco AV di 1° grado | alta | 70.1 | 0.002 | 293 | 100 | 411 | sì | superato | — |
| SIM-BAV-02 | Blocco AV di 2° grado Mobitz I (Wenckebach 4:3) | alta | 72.3 | 0.237 | 294 | 100 | 413 | sì | superato | — |
| SIM-BAV-03 | Blocco AV di 2° grado Mobitz II (3:2) | alta | 83.8 | 0.344 | 174 | 153 | 442 | sì | superato | — |
| SIM-BAV-04 | Blocco AV di 3° grado con scappamento giunzionale | alta | 45.0 | 0.0 | None | 99 | 379 | no | superato | — |
| SIM-BAV-05 | Blocco AV di 3° grado con scappamento ventricolare | alta | 34.0 | 0.0 | None | 189 | 412 | no | superato | — |
| SIM-BB-01 | Blocco di branca destra | media | 71.9 | 0.003 | 152 | 157 | 434 | sì | superato | — |
| SIM-BB-02 | Blocco di branca sinistra | media | 71.9 | 0.003 | 148 | 174 | 454 | sì | superato | — |
| SIM-PM-01 | Stimolazione atriale (AAI) | media | 70.0 | 0.0 | 174 | 98 | 410 | sì | superato | — |
| SIM-PM-02 | Stimolazione ventricolare (VVI) su FA | media | 60.0 | 0.001 | None | 209 | 461 | no | superato | — |
| SIM-PM-03 | Stimolazione bicamerale (DDD) | media | 70.0 | 0.0 | 124 | 203 | 485 | sì | superato | — |
| SIM-EL-01 | Iperpotassiemia lieve: T appuntite | media | 72.0 | 0.004 | 154 | 100 | 399 | sì | superato | — |
| SIM-EL-02 | Iperpotassiemia grave: QRS largo | media | 71.9 | 0.004 | None | 188 | 434 | no | superato | — |
| SIM-EL-03 | Ipopotassiemia: onda U | media | 72.0 | 0.004 | 164 | 97 | 600 | sì | superato | — |
| SIM-EL-04 | Ipercalcemia: QT corto | media | 72.0 | 0.004 | 154 | 100 | 334 | sì | superato | — |
| SIM-EL-05 | Ipocalcemia: QT lungo | media | 72.0 | 0.004 | 153 | 100 | 527 | sì | superato | — |
| SIM-MI-01 | STEMI anteriore acuto | media | 81.9 | 0.004 | 154 | 102 | 429 | sì | superato | — |
| SIM-MI-02 | STEMI inferiore acuto | media | 81.9 | 0.004 | 154 | 101 | 431 | sì | superato | — |
| SIM-MI-03 | STEMI laterale acuto | media | 81.9 | 0.004 | 153 | 101 | 430 | sì | superato | — |
| SIM-MI-04 | STEMI inferiore in evoluzione (onde Q) | media | 81.9 | 0.004 | 152 | 102 | 432 | sì | superato | — |
| SIM-WPW-01 | Pre-eccitazione ventricolare (WPW) | media | 71.9 | 0.003 | 295 | 151 | 464 | sì | superato | — |
| SIM-PER-01 | Pericardite acuta | media | 91.9 | 0.004 | 214 | 100 | 441 | sì | superato | — |
| SIM-MI-05 | Infarto posteriore acuto (speculare in V1–V3) | media | 79.9 | 0.004 | 153 | 97 | 434 | sì | superato | — |
| SIM-WEL-01 | Pattern di Wellens (tipo B) | media | 69.8 | 0.005 | 153 | 100 | 429 | sì | superato | — |
| SIM-DEW-01 | Pattern di de Winter | media | 85.0 | 0.004 | 153 | 97 | 437 | sì | superato | — |
| SIM-IPO-01 | Ipotermia: onda J di Osborn | media | 44.0 | 0.003 | 213 | 138 | 451 | sì | superato | — |
| SIM-DIG-01 | Effetto digitalico | media | 64.0 | 0.004 | 194 | 99 | 367 | sì | superato | — |
| SIM-PAU-01 | Pausa sinusale con battito di scappamento giunzionale | alta | 70.0 | 0.512 | 154 | 100 | 412 | sì | superato | — |
| SIM-PAU-02 | Pausa sinusale con battito di scappamento ventricolare | alta | 70.0 | 0.838 | 154 | 100 | 410 | sì | superato | — |
| SIM-EX-05 | Extrasistole atriale non condotta | alta | 72.0 | 0.203 | 154 | 100 | 413 | sì | superato | — |
| SIM-EX-06 | Bigeminismo atriale | alta | 86.6 | 0.235 | 170 | 99 | 447 | sì | superato | — |
| SIM-EX-07 | Extrasistoli ventricolari multifocali | media | 75.0 | 0.333 | 154 | 99 | 416 | sì | superato | — |
| SIM-EX-08 | Coppia di extrasistoli ventricolari | media | 75.0 | 0.264 | 154 | 100 | 416 | sì | superato | — |
| SIM-EX-09 | Extrasistole ventricolare con fenomeno R su T | media | 75.0 | 0.264 | 154 | 100 | 416 | sì | superato | — |
| SIM-FB-01 | Blocco fascicolare anteriore sinistro | media | 72.0 | 0.003 | 152 | 110 | 413 | sì | superato | — |
| SIM-FB-02 | Blocco fascicolare posteriore sinistro | media | 71.9 | 0.003 | 154 | 109 | 412 | sì | superato | — |
| SIM-FB-03 | Blocco bifascicolare (BBD + blocco fascicolare anteriore sinistro) | media | 71.9 | 0.003 | 152 | 156 | 434 | sì | superato | — |
| SIM-IP-01 | Ipertrofia ventricolare destra | media | 80.0 | 0.004 | 154 | 108 | 431 | sì | superato | — |
| SIM-IP-02 | Ipertrofia ventricolare sinistra con sovraccarico | media | 70.0 | 0.003 | 157 | 109 | 425 | sì | superato | — |
| SIM-IP-03 | Ingrandimento atriale sinistro (P mitralica) | media | 77.9 | 0.004 | 115 | 99 | 418 | sì | superato | — |
| SIM-IP-04 | Ingrandimento atriale destro (P polmonare) | media | 77.9 | 0.004 | 151 | 100 | 418 | sì | superato | — |
| SIM-TAM-01 | Tachicardia atriale multifocale | media | 110.2 | 0.101 | None | 99 | 443 | no | superato | — |
| SIM-TAM-02 | Pacemaker atriale migrante | media | 70.5 | 0.093 | None | 100 | 411 | no | superato | — |
| SIM-FLV-01 | Flutter ventricolare | schematica | None | None | None | None | None | no | superato | — |
| SIM-TAB-01 | Tachicardia atriale con blocco AV 2:1 | media | 90.0 | 0.001 | 193 | 99 | 429 | sì | superato | — |
| SIM-BAV-06 | Blocco AV di 2° grado avanzato (3:1) | alta | 30.0 | 0.0 | 178 | 156 | 364 | sì | superato | — |
| SIM-MI-06 | Sottoslivellamento ST diffuso con sopraslivellamento in aVR | media | 94.9 | 0.004 | 153 | 95 | 275 | sì | superato | — |
| SIM-LV-01 | Bassi voltaggi | alta | 88.0 | 0.003 | 153 | 99 | 427 | sì | superato | — |

Note: per FV, torsione di punta e alcune extrasistoli le misure globali (FC, QRS mediano) non sono significative e non sono usate come criterio; la verifica è affidata al revisore.
