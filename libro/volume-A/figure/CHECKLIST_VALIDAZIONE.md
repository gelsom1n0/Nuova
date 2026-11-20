# Checklist di validazione clinica dei tracciati e degli schemi – Volume A

Da usare in una **revisione indipendente** (cardiologo o infermiere esperto in elettrocardiografia) prima
che una figura entri nel libro. Il revisore lavora sul file PNG/SVG della figura (o sulla prova di stampa)
e registra l'esito in `MANIFEST.csv`, colonne `stato_validazione` e `note_revisore`.

## Stati ammessi
| Stato | Significato |
|---|---|
| `da_validare` | stato iniziale di **tutte** le figure |
| `validato` | il revisore conferma diagnosi, morfologia e didascalia |
| `da_correggere` | errore correggibile (parametro del simulatore, didascalia, derivazione) – descrivere in `note_revisore` |
| `scartato` | figura da non usare (motivo in `note_revisore`) |

`genera_manifest.py` conserva questi due campi quando rigenera il MANIFEST. Con `build_A.py --bozza`
le figure non validate mostrano lo stato in didascalia; il report di build elenca sempre le figure da validare.

## Controlli comuni a ogni tracciato
- [ ] **Carta**: 25 mm/s e 10 mm/mV dichiarati; impulso di calibrazione alto 10 mm a scala reale (o riduzione dichiarata in didascalia).
- [ ] **Derivazioni**: etichette corrette; per MIT-BIH «MLII» = II modificata da Holter (non è una II standard); per CUDB la derivazione non è specificata.
- [ ] **Didascalia**: descrive solo ciò che si vede; etichetta «tracciato didattico simulato» oppure «tracciato reale – fonte – licenza».
- [ ] **Leggibilità in B/N** sulla prova di stampa: tracciato distinguibile dalla griglia; nessun dettaglio diagnostico perso.
- [ ] **Coerenza con il testo** che cita la figura (valori di frequenza, intervalli, derivazioni nominate).

## Gruppo «ritmo» (sinusale, tachi/bradi, FA, flutter, TSV, TV, torsione, FV, asistolia)
- [ ] **Frequenza** (atriale e ventricolare) coerente con la didascalia (metodo dei 1500 / dei 6 secondi).
- [ ] **Regolarità RR**: regolare / regolarmente irregolare / irregolarmente irregolare come dichiarato.
- [ ] **Onde P**: presenti/assenti; morfologia (sinusale positiva in II); rapporto P:QRS.
- [ ] **Onde atriali patologiche**: onde f della FA (irregolari, nessuna linea isoelettrica); onde F del flutter (dente di sega, ~300/min, negative in II/III/aVF nel tipico, rapporto di conduzione esatto).
- [ ] **QRS**: stretto (< 0,12 s) o largo; complessi uguali (monomorfi) o variabili.
- [ ] **TV**: QRS larghi regolari; segni di dissociazione AV se dichiarati.
- [ ] **Torsione di punta**: QT lungo nei battiti di base, innesco, fusi di ampiezza con inversione di polarità.
- [ ] **FV**: nessun complesso organizzato; distinguere FV fine da asistolia e da artefatto.
- [ ] **Asistolia**: assenza di QRS (e P se dichiarato); nessuna FV fine nascosta.

## Gruppo «extrasistoli»
- [ ] **Prematurità** rispetto al ciclo di base.
- [ ] **ESA**: P prematura di morfologia diversa; QRS stretto; pausa non compensatoria.
- [ ] **ESG**: assenza di P precedente o P retrograda (negativa in II) con PR corto o dopo il QRS.
- [ ] **ESV**: QRS ≥ 0,12 s, bizzarro, senza P precedente; T discordante; pausa compensatoria piena (se dichiarata).
- [ ] **Bigeminismo**: alternanza regolare 1:1 normale/extrasistole con accoppiamento fisso.

## Gruppo «blocchi» (BAV)
- [ ] Ogni **P identificata** (anche quelle nascoste in T o QRS) e rapporto P:QRS dichiarato.
- [ ] **1° grado**: PR > 0,20 s costante, conduzione 1:1.
- [ ] **Mobitz I**: allungamento progressivo del PR, P bloccata, PR più corto dopo la pausa; battiti raggruppati.
- [ ] **Mobitz II**: PR costante prima e dopo la P bloccata.
- [ ] **2:1**: indicato come «2° grado 2:1» (non classificabile Mobitz I/II dal solo tracciato).
- [ ] **3° grado**: P e QRS indipendenti (PR variabile), frequenza atriale > ventricolare, tipo di scappamento (stretto/largo).
- [ ] PTB-XL non distingue Mobitz I e II nella voce `2AVB`: il revisore deve **classificare** il tipo o scartare.

## Gruppo «morfologia_normale»
- [ ] Asse frontale normale (−30°/+90°); P sinusale; PR 0,12–0,20 s; QRS < 0,12 s; QTc nei limiti.
- [ ] Progressione dell'onda R V1→V6 con transizione V3–V4; q settali piccole in I, aVL, V5–V6.
- [ ] ST isoelettrico; T positive in I, II, V3–V6 e negativa in aVR.

## Gruppo «morfologia_conduzione» (BBD, BBS, WPW)
- [ ] **BBD**: QRS ≥ 0,12 s; rsR'/rSR' in V1–V2; S larga in I, aVL, V6; ST-T discordanti in V1–V3.
- [ ] **BBS**: QRS ≥ 0,12 s; R larga/intaccata in I, aVL, V5–V6 senza q; QS o rS in V1–V3; discordanza appropriata.
- [ ] **Brugada** (Brugada-HUCA, 100 Hz): tipo 1 = sopraslivellamento del punto J ≥ 2 mm con ST «a tenda»
      (coved) e T negativa in V1 e/o V2; distinguere dal tipo «a sella», non diagnostico. Licenza CC BY-SA.
- [ ] **WPW**: PR corto (< 0,12 s), onda delta, QRS slargato, alterazioni secondarie della ripolarizzazione (la misura automatica del PR non è affidabile: controllo manuale).

## Gruppo «morfologia_ipertrofia»
- [ ] Criteri di voltaggio dichiarati (es. Sokolow-Lyon SV1 + RV5/V6 ≥ 3,5 mV; R aVL ≥ 1,1 mV) verificati a mano.
- [ ] Alterazioni di «strain» se citate in didascalia.

## Gruppo «ischemia» (STEMI simulati, infarti reali PTB-XL)
- [ ] **Derivazioni con ST sopraslivellato** e **speculari** corrispondono al territorio dichiarato.
- [ ] Misura dello ST al punto J (o J+60 ms) rispetto alla linea PR; soglie secondo le definizioni correnti (età/sesso per V2–V3).
- [ ] **PTB-XL**: le etichette di infarto (AMI, ASMI, IMI, LMI…) **non indicano necessariamente un infarto acuto** (vedi `infarction_stadium1` nei metadati): la didascalia non deve dire «STEMI acuto» se il tracciato mostra esiti (onde Q, T negative) senza sopraslivellamento.
- [ ] Onde Q patologiche: durata ≥ 0,04 s o profondità significativa, in derivazioni contigue.

## Gruppo «elettroliti»
- [ ] **Iperpotassiemia**: T alte, appuntite, a base stretta; nei gradi avanzati P appiattite, PR lungo, QRS largo.
- [ ] **Ipopotassiemia**: T piatte, onda U evidente (non confondere QU con QT), ST sottoslivellato lieve.
- [ ] **Ipercalcemia**: QT corto per accorciamento del tratto ST.
- [ ] **Ipocalcemia**: QT lungo per allungamento del tratto ST con T di durata normale.
- [ ] La didascalia precisa che l'ECG **non sostituisce** il dosaggio dell'elettrolita.

## Gruppo «pacemaker»
- [ ] Spike visibili e attribuiti alla camera giusta (atriale/ventricolare).
- [ ] **Cattura**: ogni spike seguito dalla depolarizzazione corrispondente (P o QRS largo).
- [ ] Morfologia del QRS stimolato coerente con la sede (apice VD: tipo BBS, asse superiore).
- [ ] Ritardo AV (DDD) e frequenza di stimolazione coerenti con la didascalia.
- [ ] Negli spike simulati l'ampiezza è **volutamente esagerata** per la stampa: segnalarlo se il testo lo richiede.

## Gruppo «schemi»
- [ ] Correttezza fisiologica (fasi del potenziale d'azione, sequenza del ciclo di Wiggers, valori di pressione indicativi).
- [ ] Geometria del sistema esassiale e delle derivazioni corretta (angoli, polarità).
- [ ] Posizioni degli elettrodi precordiali (spazi intercostali e linee di repere).
- [ ] Nessuna somiglianza con figure di libri esistenti.

## Note specifiche sui tracciati simulati
- Sono **puliti per costruzione**: non mostrano artefatti, variabilità o rumore reali. Per l'esercizio di
  riconoscimento in condizioni realistiche va affiancato almeno un tracciato reale per gruppo.
- `affidabilita_modello` nel MANIFEST: `alta` (logica del ritmo standard e morfologia di base),
  `media` (morfologia ricostruita da principi fisiopatologici: verificare con particolare attenzione),
  `schematica` (FV, torsione di punta: modello fenomenologico; usare preferibilmente il reale).
- Ogni JSON in `sim/out/` contiene i parametri usati, le misure automatiche e la sequenza degli eventi
  (tempi di P, QRS, spike): il revisore può verificare un valore senza misurarlo a mano.
