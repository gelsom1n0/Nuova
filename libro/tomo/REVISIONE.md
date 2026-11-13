# Registro di revisione – «Basi di farmacologia clinica»

**Revisore:** revisione indipendente (ruolo: revisore in ambito medico-infermieristico) · **Data di tutte le verifiche:** 13 novembre 2026 · **Bozza di partenza:** commit `40cff55` (128 pagine) · **Esito:** `output/interno_KDP.pdf`, 132 pagine.

Legenda esiti: **C** confermata · **K** corretta · **R** rimossa · **V** da verificare (annotata anche in `DA_VERIFICARE.md`).
Fonti abbreviate: vedi `FONTI_VERIFICA.md` (sigle tra parentesi quadre). «AIFA-OD» = elenco ufficiale AIFA delle confezioni autorizzate (dati aperti, `confezioni.csv`, aggiornato al 13/11/2026), usato per tutti i nomi commerciali.

> Metodo. Lettura integrale delle 15 Parti; verifica con ricerca web delle affermazioni a maggior impatto clinico o normativo (linee guida, Note AIFA, Raccomandazioni ministeriali, studi citati, controindicazioni, soglie); verifica sistematica di tutti i nomi commerciali su AIFA-OD. Dove la fonte primaria non era leggibile integralmente si è usata la sintesi di almeno una fonte secondaria qualificata, segnalandolo con **V** quando il dettaglio è rilevante. Le affermazioni di farmacologia di base (meccanismi, equivalenze, calcoli) sono state controllate con la conoscenza consolidata e ricalcolate, senza ricerca dedicata quando non controverse.

## Errori corretti, per gravità

### Gravità alta (potenziale danno al paziente o informazione regolatoria errata)
1. **P4 – Andexanet alfa indicato anche per l'edoxaban** → corretto: l'RCP europeo lo indica solo per apixaban e rivaroxaban; aggiunta l'avvertenza AIFA sull'inefficacia dell'eparina dopo andexanet (rilevante in cardiochirurgia/CEC). [EMA-Ondexxya, AIFA-Ondexxya]
2. **P9 – «Per via EV solo insulina umana rapida»** → corretto: di riferimento l'umana regolare, ma alcuni analoghi rapidi sono autorizzati EV; vietate per via EV le insuline intermedie, lente e premiscelate. [RCP Humalog/NovoRapid/Apidra – conoscenza consolidata]
3. **P9 – Chetoacidosi: insulina con K ≥ 3,3 mmol/L e dose 0,05–0,1 UI/kg/h** → soglia portata a **≥ 3,5 mmol/L** (consenso internazionale 2024) e rimossa la dose numerica (farmaco ad alto rischio). [Consenso crisi iperglicemiche 2024]
4. **P6 – Dronedarone controindicato solo «in NYHA III–IV o recentemente instabile»** → corretto con l'RCP: controindicato in scompenso pregresso o in atto, disfunzione sistolica VS, FA permanente, CrCl < 30, QTc ≥ 500 ms, bradicardia < 50, con dabigatran. [RCP Multaq – AIFA]
5. **P2 – Dissezione aortica: obiettivo FC 60–80 bpm** → corretto a FC ≈ 60 bpm e PAS ≤ 120 mmHg (dettaglio 2024 **V**). [ESC 2024 aorta, sintesi]
6. **P14/P1/P15 – Note AIFA 1 e 48 citate come vigenti** → **abrogate** e sostituite dalla **Nota AIFA N01** (determina n. 238 del 4/3/2026, GU n. 55 del 7/3/2026). [AIFA N01, Quotidiano Sanità]
7. **P9 – Gliflozine e incretine «con piano terapeutico specialistico»** → superato: **Nota AIFA 100** (2022, aggiornata 07/2025) consente la prescrizione anche al MMG. [AIFA Nota 100]
8. **P10 – Ossigeno nell'asma con SpO₂ 94–98%** → corretto a 93–95% nell'adulto (GINA). [GINA, sintesi]
9. **P8 – HES «da evitare»** → autorizzazioni sospese nell'UE (decisione della Commissione europea del 24/5/2022). [EMA-HES]
10. **Dosi pronte all'uso per farmaci ad alto rischio** (regola 7.3 del prompt di scrittura) → rimosse o ricondotte al protocollo: eparina 80 UI/kg + 18 UI/kg/h (P4, mantenuto solo come esercizio di calcolo in P1 con avvertenza), esmololo carico/infusione (P2), amiodarone EV in FA e lidocaina in infusione (P6), magnesio 2 g in 10–15 min, calcio 10 mL in 5–10 min, NaCl 3% 150 mL in 20 min, insulina 10 UI nell'iperpotassiemia (P8), morfina EV 2–3 mg (P12), insulina in CAD (P9). Mantenute, con fonte, le dosi di riferimento delle linee guida di rianimazione (amiodarone 300/150 mg, adrenalina IM 0,5 mg) e l'ordine di grandezza della lidocaina in arresto.
11. **Nomi commerciali non autorizzati in Italia** (AIFA-OD) → rimossi o sostituiti: Reniten→**Enapren**; Diovan (rimosso); Cozaar→**Lortaan**; Atacand→**Ratacand, Blopress**; Zanidip→**Zanedip** (+Lercadip); Liquemin (rimosso: «vari produttori»); Fraxiparina/Fragmin→**Seleparina, Seledie** (dalteparina non autorizzata); Angiox→bivalirudina generica; Integrilin→eptifibatide generica; Tambocor (rimosso); Lipitor (rimosso); Vancocina (autorizzata solo come «Vancocina A.P.»: sostituita con «generici» per chiarezza); Zyvox→**Zyvoxid**; Zithromax→**Zitromax**; Toradol→**Tora-Dol**; Narcan→generici, **Nyxoid, Ventizolve**; Solu-Cortef→**Sofacor**; Solu-Medrol→**Urbason solubile**; Florinef (non autorizzato: importazione); «Teofillina RP» (teofillina orale assente: aminofillina EV, doxofillina/**Ansimar**).
12. **P2 – Metoprololo succinato presentato come disponibile** → nell'AIFA-OD compare solo il tartrato (IR e RP): segnalato; nello scompenso si indirizza verso bisoprololo, carvedilolo, nebivololo.
13. **P6 – Procainamide proposta come farmaco di scelta (WPW, TV stabile)** → non autorizzata in Italia: segnalato, alternative indicate (ibutilide, amiodarone, cardioversione). Idem **nicardipina EV** e **nitroprussiato** (P3: importazione) e **Fab anti-digossina** (P6).

### Gravità media (aggiornamento di linee guida, imprecisioni cliniche)
14. **P2/P3/P15 – Scompenso: ESC 2021/2023 e HFrEF ≤ 40%** → aggiornato alle **linee guida ESC 2026** (HFrEF < 50%, abolita la categoria a FE lievemente ridotta, stadi A–D, quattro classi fondamentali). Aggiunta nota dedicata in P2.
15. **P2 – Beta-bloccanti dopo infarto con FE conservata** → aggiunto **BETAMI-DANBLOCK** (NEJM 2025: riduzione modesta dell'esito composito, guidata dai reinfarti).
16. **P8/P11/P13 – Surviving Sepsis Campaign 2021** → aggiornato alla **SSC 2026** (antibiotico entro 1 h solo in shock/sepsi probabile, entro 3 h nella sepsi possibile; infusione prolungata dei beta-lattamici raccomandata; idrocortisone suggerito con certezza bassa; cristalloidi bilanciati; niente albumina aggiuntiva di routine).
17. **P7 – Dislipidemie ESC/EAS 2019 «con aggiornamenti da verificare»** → aggiornamento mirato **2025** verificato (obiettivi LDL-C invariati, SCORE2/SCORE2-OP, acido bempedoico raccomandato negli intolleranti); aggiunta nota.
18. **P7 – Nota 13 come norma di rimborsabilità per anti-PCSK9** → corretto: anti-PCSK9, inclisiran e acido bempedoico seguono determine specifiche con piano terapeutico; Nota 13 non aggiornata dal 2019 (**V** per eventuale revisione successiva).
19. **P6/P15 – ESC «2020» tachicardie sopraventricolari** → **2019**.
20. **P15 – ESC gravidanza 2018 «da verificare»** → **2025** (pubblicata 29/8/2025).
21. **P3/P15 – Sospensione ACE-i/sartani «24 ore prima»** → ESC 2022: considerare la sospensione **il giorno dell'intervento** nei pazienti senza scompenso, solo per chirurgia non cardiaca.
22. **P4/P15 – Sospensione DOAC 24–72 h** → aggiunto «fino a 96 h e oltre per dabigatran con CrCl ridotta».
23. **P4 – Apixaban: mancava il criterio CrCl 15–29** per la dose ridotta; **fondaparinux**: aggiunta la soglia < 30 mL/min nel trattamento; **enoxaparina**: aggiunta l'equivalenza UI/mg delle confezioni italiane.
24. **P4 – Nota AIFA 97** → aggiornata alla determina 17/6/2026 (abolizione della scheda obbligatoria); segnalata la discrepanza CHA2DS2-VASc (Nota) vs CHA2DS2-VA (ESC 2024).
25. **P9/P15 – SGLT2i «circa 3 giorni»** → «almeno 3 giorni» (ESC 2022), 4 per ertugliflozin.
26. **P11 – Profilassi dell'endocardite** formulata in modo ambiguo («in presenza di protesi… solo ad alto rischio») → riformulata (ESC 2023).
27. **P11 – Fluorochinoloni e aneurisma** → precisata l'avvertenza EMA/AIFA 2018 e le restrizioni 2019.
28. **P11 – Anafilassi «0,5 mL di soluzione 1:1000»** → «0,5 mL della fiala da 1 mg/mL», sede e ripetizione secondo ERC 2025.
29. **P12 – Ketorolac «cicli brevissimi»** → precisato: max 2 giorni iniettabile, 5 giorni orale (NII AIFA 2015).
30. **P12 – ERAS**: citazione resa precisa (ERAS Cardiac Society 2019; consenso con POQI 2023); gabapentinoidi segnalati come evidenza discordante (PROSPECT).
31. **P14 – Ranitidina «ritirata»** → sospesa nell'UE (EMA 2020) per NDMA; **IPP con antitrombotici** limitato ai pazienti ad aumentato rischio di sanguinamento GI (ESC 2023); aggiunto **REVISE** (NEJM 2024).
32. **P5 – Abciximab** elencato tra i farmaci disponibili → non più autorizzato in Italia. Precisata la preferenza per prasugrel nella SCA con PCI (ESC 2023).
33. **P2 – Nebivololo tra le «molecole con prove di mortalità»** → riformulato in «raccomandate» (SENIORS: esito composito).

### Gravità bassa (lingua, terminologia, stile)
34. «laxativi» → **lassativi** (P12, P15); «titrato/i» → **titolato/i**; «opioid-tolleranti» → **tolleranti agli oppioidi**; «ponteggiare» → «attuare un ponte»; «evitamento» → «da evitare»; «a bedtime» → «prima di coricarsi»; «il aztreonam» → «l'aztreonam»; «Ricorrere a emogasanalisi» → «Eseguire l'emogasanalisi»; «attraversano» → «attraversano la placenta»; «sindrome dell'uomo rosso» → «reazione da infusione» (termine attuale); «aumentare… i tendini (rotture)» → «rischio di rottura tendinea».
35. **Interno KDP:** tinta di fondo del riquadro *Nota* `#f1f1f1` (≈ 5%) portata a `#e5e5e5` (10%) in `engine/style_kdp.css`, per il requisito «nessuna tinta sotto il 10%» (unica modifica al motore).

## Registro per classe

| Classe | Affermazione | Esito | Fonte consultata | Data |
|---|---|---|---|---|
| P1 | Cockcroft-Gault e esempio (≈ 35 mL/min) | C (ricalcolato) | formula standard | 13/11/2026 |
| P1 | Esempi di calcolo (42 gtt/min; 21 mL/h; 28,8 mL/h) | C (ricalcolati); eparina riformulata come esercizio | — | 13/11/2026 |
| P1 | Raccomandazioni ministeriali «da verificare» | K: n. 1 e 7 (2008), 12 (2010), 17 (2014), 18 (2018), 19 (2019) | [MinSal-Racc] | 13/11/2026 |
| P1 | Sezioni RCP 4.2–4.9, 6.6 | C | struttura RCP (QRD) | 13/11/2026 |
| P1 | Inibitori CYP2C19 (omeprazolo/esomeprazolo) e clopidogrel | C | RCP Plavix; ESC | 13/11/2026 |
| P2 | Nomi commerciali bisoprololo, carvedilolo, nebivololo, atenololo, propranololo, esmololo, labetalolo, sotalolo | C | AIFA-OD | 13/11/2026 |
| P2 | Landiololo «disponibilità da verificare» | K: autorizzato (Landiobloc) | AIFA-OD | 13/11/2026 |
| P2 | Metoprololo succinato disponibile | K (solo tartrato autorizzato) | AIFA-OD | 13/11/2026 |
| P2 | REDUCE-AMI, ABYSS (NEJM 2024), REBOOT (NEJM 2025, segnale nelle donne) | C | [BB-postMI] | 13/11/2026 |
| P2 | BETAMI-DANBLOCK | K (aggiunto) | [BB-postMI] | 13/11/2026 |
| P2 | Beta-bloccante post-SCA: raccomandato con FE ≤ 40%, giudizio clinico negli altri casi (ESC 2023) | K (aggiunto per completezza) | ESC 2023 ACS – conoscenza consolidata | 13/11/2026 |
| P2 | HFrEF ≤ 40% (ESC 2021/2023) | K → ESC 2026, FE < 50% | [ESC-HF-2026] | 13/11/2026 |
| P2 | Titolazione «ogni 2–4 settimane» | K/V: 1–2 settimane o più; dettaglio ESC 2026 da verificare | [ESC-HF-2026] (sintesi) | 13/11/2026 |
| P2 | POISE (Lancet 2008) | C | conoscenza consolidata | 13/11/2026 |
| P2 | Dissezione aortica FC 60–80 | K (≈ 60; PAS ≤ 120) / V testo 2024 | [ESC-Aorta-2024] | 13/11/2026 |
| P2 | Esmololo carico/infusione numerici | R (rimandati a RCP/protocollo) | regola alto rischio | 13/11/2026 |
| P2 | Glucagone 3–5 mg nell'intossicazione | K (formulazione qualitativa, Centro Antiveleni) | regola alto rischio | 13/11/2026 |
| P3 | Categorie ESC 2024 (< 120/70; 120–139/70–89; ≥ 140/90) e obiettivo 120–129 | C | [ESC-HTN-2024] | 13/11/2026 |
| P3 | Nomi commerciali | K (vedi punto 11); C gli altri | AIFA-OD | 13/11/2026 |
| P3 | Sacubitril/valsartan: 36 h dopo ACE-i | C | RCP Entresto | 13/11/2026 |
| P3 | Furosemide EV ≤ 4 mg/min | C | RCP Lasix | 13/11/2026 |
| P3 | Vasodilatatori EV (nicardipina, nitroprussiato) | K: non autorizzati in Italia; clevidipina (Cleviprex) e urapidil (Ebrantil) autorizzati | AIFA-OD | 13/11/2026 |
| P3 | Sospensione ACE-i/sartani pre-chirurgia | K | [ESC-NCS-2022] | 13/11/2026 |
| P4 | CHA2DS2-VA (ESC 2024) | C | ESC 2024 FA | 13/11/2026 |
| P4 | Nota AIFA 97 | K (determina 17/6/2026) / V data di efficacia | [AIFA-N97] | 13/11/2026 |
| P4 | Criteri riduzione dose DOAC | C; K (apixaban CrCl 15–29) | RCP Eliquis, Xarelto, Lixiana, Pradaxa | 13/11/2026 |
| P4 | Andexanet per edoxaban | K (non indicato) | [EMA-Ondexxya] | 13/11/2026 |
| P4 | Idarucizumab 5 g (2 × 2,5 g) | C | RCP Praxbind | 13/11/2026 |
| P4 | Protamina 1 mg/100 UI, max 50 mg | C | RCP protamina | 13/11/2026 |
| P4 | BRIDGE (NEJM 2015) | C | conoscenza consolidata | 13/11/2026 |
| P4 | ACT in CEC ≥ 400–480 s | C (orientativo, «secondo protocollo») | pratica consolidata | 13/11/2026 |
| P4 | Disponibilità andexanet in Italia | C (autorizzato; determina AIFA 158/2024 nuove confezioni) / V rimborsabilità | [AIFA-Ondexxya] | 13/11/2026 |
| P5 | DAPT 12 mesi in SCA; 6 mesi dopo PCI in CCS | C | ESC 2023 ACS; ESC 2024 CCS | 13/11/2026 |
| P5 | Sospensione pre-CABG ticagrelor 3, clopidogrel 5, prasugrel 7 giorni | C | ESC 2023 | 13/11/2026 |
| P5 | AUGUSTUS (NEJM 2019) | C | conoscenza consolidata | 13/11/2026 |
| P5 | Rinvio chirurgia 6/12 mesi (ESC 2022) | C | [ESC-NCS-2022] | 13/11/2026 |
| P5 | Nomi commerciali (Iscover, Aggrastat, Kengrexal, Persantin…) | C; K Integrilin, abciximab | AIFA-OD | 13/11/2026 |
| P6 | Amiodarone in arresto 300 + 150 mg | C (ERC); V tempistica della seconda dose nel testo ERC 2025 | [ERC-2025], AHA 2025 | 13/11/2026 |
| P6 | Lidocaina 1–1,5 mg/kg | C (ordine di grandezza in arresto) | AHA 2025 | 13/11/2026 |
| P6 | Adenosina 6 → 12 mg | C | ESC 2019 SVT | 13/11/2026 |
| P6 | CAST (NEJM 1991) | C | conoscenza consolidata | 13/11/2026 |
| P6 | Dronedarone controindicazioni | K | [RCP-Multaq] | 13/11/2026 |
| P6 | QTc > 500 ms o ↑ ≥ 60 ms; Bazett ≈ 447 ms | C (ricalcolato) | — | 13/11/2026 |
| P6 | FA post-operatoria 20–40% | C (indicativo) / V | letteratura consolidata | 13/11/2026 |
| P6 | Procainamide, Fab anti-digossina, Tambocor | K (non autorizzati) | AIFA-OD | 13/11/2026 |
| P7 | Obiettivi LDL-C | C (confermati 2025) | [ESC-EAS-2025] | 13/11/2026 |
| P7 | IMPROVE-IT 2015, FOURIER 2017, ODYSSEY 2018, CLEAR 2023, REDUCE-IT 2019, SAMSON 2020 | C | conoscenza consolidata | 13/11/2026 |
| P7 | Nota AIFA 13 | K (ambito) / V testo vigente | [AIFA-N13] | 13/11/2026 |
| P7 | Lipitor | R | AIFA-OD | 13/11/2026 |
| P8 | Composizione cristalloidi; Ca gluconato 1 g ≈ 2,3 mmol; CaCl₂ 1 g ≈ 6,8 mmol; MgSO₄ 2 g ≈ 8 mmol | C (ricalcolati) | stechiometria | 13/11/2026 |
| P8 | KCl periferico ≤ 40 mmol/L e ≤ 10 mmol/h | C (limite di sicurezza diffuso; da allineare al protocollo) | pratica consolidata; Racc. n. 1 | 13/11/2026 |
| P8 | Raccomandazione ministeriale sul KCl | K (n. 1, marzo 2008) | [MinSal-Racc] | 13/11/2026 |
| P8 | NaCl 3% 150 mL/20 min; limite 8–10 mmol/L/24 h | C (linee guida europee 2014); dose rimossa dalle tabelle | conoscenza consolidata | 13/11/2026 |
| P8 | Mantenimento NICE 25–30 mL/kg/die, 1 mmol/kg | C | NICE CG174 | 13/11/2026 |
| P8 | SMART (NEJM 2018); SSC | C; K → SSC 2026 | [SSC-2026] | 13/11/2026 |
| P8 | Iperpotassiemia: insulina 10 UI + glucosio 25 g; calcio | C (ERC 2025/RCUK); dose rimossa dal testo (alto rischio) | [ERC-2025] | 13/11/2026 |
| P8 | HES | K | [EMA-HES] | 13/11/2026 |
| P8 | **Lacuna**: manca la fisiopatologia per singolo disturbo elettrolitico (cause, sintomi, ECG, trattamento di ipo/ipernatriemia, ipo/ipercalcemia, ipo/ipermagnesiemia, ipo/iperfosfatemia) | **Segnalata, non colmata** (su mandato) | — | 13/11/2026 |
| P9 | Soglie ipoglicemia ADA (70/54 mg/dL) | C | ADA Standards of Care | 13/11/2026 |
| P9 | Metformina: no se eGFR < 30, riduzione 30–45 | C | EMA 2016 (RCP) | 13/11/2026 |
| P9 | EMPA-REG 2015, DAPA-HF 2019, EMPEROR-Reduced 2020, SUSTAIN-6, LEADER 2016 | C | conoscenza consolidata | 13/11/2026 |
| P9 | Via EV solo insulina umana | K | RCP analoghi rapidi | 13/11/2026 |
| P9 | CAD: K ≥ 3,3; dose insulina | K / R | [Crisi-iperglic-2024] | 13/11/2026 |
| P9 | Piano terapeutico per incretine/gliflozine | K → Nota 100 | [AIFA-N100] | 13/11/2026 |
| P9 | Glucagone 1 mg IM/SC | C; aggiunto glucagone nasale 3 mg (Baqsimi autorizzato) | AIFA-OD | 13/11/2026 |
| P9 | Obiettivi HbA1c (≈ 7%; 7,5–8,5% nei fragili) | C (orientativi) / V target SID-AMD 49–58 mmol/mol | [SID-AMD] | 13/11/2026 |
| P10 | Nomi commerciali inalatori | C | AIFA-OD | 13/11/2026 |
| P10 | Teofillina RP | K (teofillina orale assente) | AIFA-OD | 13/11/2026 |
| P10 | SpO₂ asma 94–98% | K → 93–95% | [GINA] | 13/11/2026 |
| P10 | Prednisone 40 mg × 5 giorni (BPCO) | C (consolidato) / V testo GOLD 2026–2027 | [GOLD-2026] | 13/11/2026 |
| P10 | Rimborsabilità: piano terapeutico | K → Nota 99 per la BPCO | [AIFA-N99] | 13/11/2026 |
| P11 | Vancomicina ≥ 60 min/g (≤ 10 mg/min); AUC/MIC | C | IDSA/ASHP 2020; RCP | 13/11/2026 |
| P11 | Gentamicina 5–7 mg/kg/die | C | pratica consolidata | 13/11/2026 |
| P11 | Cefazolina 2 g (3 g se ≥ 120 kg), entro 60 min, ripetizione ~4 h, durata ≤ 24–48 h | C (orientativo, protocollo locale) | linee guida di profilassi consolidate | 13/11/2026 |
| P11 | Adrenalina IM 0,5 mg | C | [ERC-2025] | 13/11/2026 |
| P11 | Sepsi entro 1 ora | K (SSC 2026) | [SSC-2026] | 13/11/2026 |
| P11 | Nomi commerciali | K (Zyvoxid, Zitromax, vancomicina generica) | AIFA-OD | 13/11/2026 |
| P12 | Legge 38/2010 (rilevazione in cartella) | C (art. 7) | [L38] | 13/11/2026 |
| P12 | Ketorolac | K (2 gg iniettabile, 5 gg orale) | [AIFA-Ketorolac] | 13/11/2026 |
| P12 | Equianalgesie (morfina os 30 ≈ EV 10 ≈ ossicodone 20; fentanil 100 µg ≈ morfina EV 10; cerotto 25 µg/h ≈ 60 mg/die os) | C (approssimative, riduzione 25–50% nella rotazione) | tabelle consolidate | 13/11/2026 |
| P12 | Naloxone 0,04–0,1 mg titolato | C (antidoto, ordine di grandezza) | pratica consolidata | 13/11/2026 |
| P12 | FANS/COX-2 controindicati dopo CABG | C | RCP celecoxib | 13/11/2026 |
| P12 | Paracetamolo max 3–4 g/die; < 50 kg 15 mg/kg | C | RCP paracetamolo EV | 13/11/2026 |
| P12 | Nomi commerciali | K (Tora-Dol, naloxone) | AIFA-OD | 13/11/2026 |
| P13 | Equivalenze (20 : 5 : 4 : 0,75 mg) | C | tabelle consolidate | 13/11/2026 |
| P13 | Crisi surrenalica: idrocortisone 100 mg EV poi 200 mg/24 h | C | Endocrine Society/ESE | 13/11/2026 |
| P13 | Shock settico: idrocortisone 200 mg/die | C; K → SSC 2026 (certezza bassa) | [SSC-2026] | 13/11/2026 |
| P13 | ADRENAL, APROCCHSS (NEJM 2018); DECS (JAMA 2012); SIRS (Lancet 2015); RECOVERY (NEJM 2021) | C | conoscenza consolidata | 13/11/2026 |
| P13 | Nomi commerciali | K (Sofacor, Urbason solubile, fludrocortisone non autorizzato) | AIFA-OD | 13/11/2026 |
| P14 | Note AIFA 1 e 48 | K → Nota N01 | [AIFA-N01] | 13/11/2026 |
| P14 | Ranitidina | K | EMA 2020 | 13/11/2026 |
| P14 | Soglie trasfusionali ESGE (Hb 7–8; più alta nel cardiopatico); endoscopia entro 24 h | C | ESGE 2021 | 13/11/2026 |
| P14 | Maastricht VI | C (2022) | conoscenza consolidata | 13/11/2026 |
| P14 | Nomi commerciali IPP, antiacidi, procinetici | C | AIFA-OD | 13/11/2026 |
| P15 | Matrice delle interazioni | C (coerente con le Parti 2–14 dopo le correzioni) | revisione incrociata | 13/11/2026 |
| P15 | Tabella peri-operatoria | K (ACE-i/sartani, DOAC, SGLT2i) | [ESC-NCS-2022] | 13/11/2026 |
| P15 | Elenco fonti | K (aggiornato a ESC 2025–2026, SSC 2026, ERC 2025, Note AIFA vigenti) | — | 13/11/2026 |

## Coerenza tra classi (controllo incrociato)
- **Potassiemia** 3,5–5,0 mmol/L; obiettivi peri-cardiochirurgici K ≥ 4,0 mmol/L e Mg ≥ 2,0 mg/dL: uguali in P6, P8, P15. **Magnesio** 0,7–1,0 mmol/L (1,7–2,4 mg/dL): coerente.
- **INR** 2–3 (P4, P15); **ipoglicemia** < 70 mg/dL (P9, P15); **QTc** > 500 ms o ↑ ≥ 60 ms (P6, P15); **LDL-C** < 55 mg/dL nel rischio molto alto (P7, P15).
- **Interazioni reciproche** (beta-bloccanti/non-DHP, clopidogrel/IPP, ticagrelor/simvastatina, amiodarone/warfarin/digossina, potassio/RAAS, calcio/ceftriaxone, linezolid/SSRI): presenti in entrambe le classi coinvolte e nella matrice P15.
- **Tempi di sospensione** antiaggreganti (P5 = P15), DOAC (P4 = P15), SGLT2i (P9 = P15): allineati dopo la revisione.
- **Riquadri «Farmaco ad alto rischio»**: presenti per vasodilatatori/diuretici EV (P3), anticoagulanti (P4), antiaritmici EV (P6), potassio ed elettroliti concentrati (P8), insulina (P9), oppioidi (P12), con doppio controllo, pompa e soglie di allerta; riepilogo in P15.

## Interno KDP
| Controllo | Esito |
|---|---|
| Formato pagina | 432 × 648 pt (6 × 9 in) su tutte le 132 pagine |
| Colore | nessun pixel non neutro (differenza massima tra canali RGB = 0 su rendering di tutte le pagine); tinte minime 10% |
| Font | 8 font, tutti incorporati e in subset (Gelasio; Liberation Serif e DejaVu Serif come fallback per simboli) |
| Immagini raster | nessuna |
| Indice generale e dei principi attivi | 220 voci controllate automaticamente sul PDF: 0 discrepanze |
| Riempimento (`check_fill.py`) | tutte le pagine interne ≥ 80%; ultime pagine di Parte 65–97%; eccezioni accettate: p. 8 (fine dell'indice nei preliminari, 46%) e ultima pagina dell'indice dei principi attivi (58%), che è la pagina finale del libro |
| Titoli orfani a fondo pagina | nessuno rilevato |
| Numero di pagine | **132** (pari, entro 24–828) |
| Margini | interno 0,7 in, esterno 0,5 in, alto/basso 0,75 in; minimo KDP per 24–150 pagine: interno 0,375 in, esterno 0,25 in → conforme |

## Limiti della revisione
- I nomi commerciali sono verificati come **autorizzati** (AIFA-OD), non come effettivamente commercializzati.
- Per ESC 2026 (scompenso), SSC 2026, ERC 2025, GINA e GOLD il testo integrale non era leggibile: si sono usate sintesi secondarie concordanti; i dettagli fini sono marcati **V**.
- Le affermazioni di farmacologia di base e i dati di studi storici sono stati controllati sulla conoscenza consolidata, senza una ricerca dedicata per ciascuno.
- Le classi occupano 7–11 pagine, sotto il target di 10–15 del prompt di scrittura: segnalato, non espanso (su mandato).
