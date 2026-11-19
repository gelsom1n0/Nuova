# Parte 8 (8.1–8.7) – Registro di verifica e punti aperti

Data di lavoro: 19 novembre 2026. Base: tomo «Basi di farmacologia clinica» (revisione del 13/11/2026, vedi `libro/tomo/REVISIONE.md`); nessun errore già corretto dal revisore è stato reintrodotto.

## Verificato in questa sessione
| Punto | Esito | Fonte |
|---|---|---|
| Tutti i nomi commerciali delle tabelle 8.2–8.7 | Presenti come «Autorizzata» nell'elenco AIFA (`confezioni.csv`, scaricato il 19/11/2026) | AIFA-OD |
| Nuovi nomi inseriti: Toradiur, Diuresix (torasemide); Cleviprex (clevidipina); Aldomet (metildopa); Kerendia (finerenone); Corvert (ibutilide); Brinavess (vernakalant); Vazkepa (icosapent etile); Confidex (PCC); Konakion (vitamina K); Eparina Vister | Autorizzati (stato amministrativo, non commercializzazione) | AIFA-OD |
| Pre-trattamento di routine con P2Y12 non raccomandato in NSTE-ACS con strategia invasiva precoce (classe III; IIb se non prevista) | Confermato da sintesi ESC e revisioni | ESC 2023 ACS, «Essential messages»; PMC11012418 |
| Ibutilide tra le opzioni di cardioversione farmacologica (ESC 2024 FA) | Confermato da sintesi secondaria | epocrates.com/e/guideline/01_24 |

## Da verificare (segnati «da verificare» nel testo)
1. **Vernakalant**: indicazione, classe di raccomandazione e controindicazioni nell'ESC 2024 FA non confermate (la ricerca non ha restituito il testo).
2. **Finerenone**: indicazioni autorizzate in Italia oltre alla malattia renale cronica con diabete di tipo 2 (eventuale scompenso con FE conservata): leggere l'RCP.
3. **ESC 2026 scompenso** (HFrEF FE < 50%, intervalli di titolazione): testo integrale non letto, solo sintesi secondarie (già aperto in DA_VERIFICARE.md).
4. **Dissezione aortica**: FC ≈ 60/min e PAS ≤ 120 mmHg (ESC 2024), solo la FC confermata (già aperto).
5. **Amiodarone in arresto**: tempistica della seconda dose nell'ERC 2025 (già aperto).
6. **FA post-operatoria 20–40%**: ordine di grandezza non verificato su fonte primaria (già aperto).
7. **Nota AIFA 97** (data di efficacia dell'aggiornamento 17/6/2026) e **Nota AIFA 13** (revisioni successive al 2019): già aperte.
8. **Metoprololo succinato** (solo tartrato nell'elenco; sale del «Metoprololo Aurobindo»): già aperto.
9. **Impronte ECG** (sezioni «Impronta sull'ECG») e **note cliniche**: contenuti di elettrocardiografia e fisiologia consolidati, scritti per questo libro; non derivati da una fonte singola. Vanno riletti da un cardiologo/infermiere esperto (in particolare la pausa da ticagrelor, gli effetti ECG della classe Ic e dell'adenosina).
10. **Dosi residue** (anche didattiche) di 8.4, 8.6 e 8.7: stesso controllo raccomandato in DA_VERIFICARE.md, sezione C.

## Adattamenti rispetto al tomo
- Aggiunte per ogni classe: «Impronta sull'ECG», 3–5 note cliniche descrittive (Situazione · Cosa si vede · Cosa si fa · Il farmaco, in due righe · Occhio infermieristico), un mnemonico/regola, un «Errore classico»; riquadri `sbar` in 8.2, 8.4, 8.6; `autotest` in 8.1.
- Rimosse le dosi pronte dell'esmololo e del labetalolo EV; nessuna dose numerica per i farmaci ad alto rischio EV oltre a quelle delle linee guida di rianimazione già verificate dal revisore.
- Rimossi i rimandi a «Parte N»: sostituiti da «sezione 8.x» solo dove indispensabile.
- Nuove molecole: torasemide, clevidipina (tabella), metildopa, finerenone, ibutilide, vernakalant, icosapent etile.
