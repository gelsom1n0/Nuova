# Fonti e licenze delle figure – Volume A

Verifica eseguita il **19 novembre 2026** sulle pagine ufficiali di PhysioNet (pagina del progetto e pagina
«view-license» di ciascuna versione). Le licenze vanno ricontrollate prima della stampa definitiva,
perché la licenza è legata alla **versione** della banca dati indicata qui.

## Riepilogo

| Banca dati (versione) | Licenza verificata | Uso nel libro | URL |
|---|---|---|---|
| PTB-XL 1.0.3 | **Creative Commons Attribution 4.0 International (CC BY 4.0)** | consentito, anche commerciale, con attribuzione e indicazione delle modifiche | https://physionet.org/content/ptb-xl/1.0.3/ |
| MIT-BIH Arrhythmia Database 1.0.0 | **Open Data Commons Attribution License v1.0 (ODC-By 1.0)** | consentito con attribuzione | https://physionet.org/content/mitdb/1.0.0/ |
| CU Ventricular Tachyarrhythmia Database (CUDB) 1.0.0 | **ODC-By 1.0** | consentito con attribuzione | https://physionet.org/content/cudb/1.0.0/ |
| Chapman-Shaoxing/Ningbo «A large scale 12-lead ECG database for arrhythmia study» (ecg-arrhythmia) 1.0.0 | **CC BY 4.0** (verificata il 20/11/2026) | consentito con attribuzione e indicazione delle modifiche | https://physionet.org/content/ecg-arrhythmia/1.0.0/ |
| PhysioNet/CinC Challenge 2021 (challenge-2021) 1.0.3 – solo sottoinsiemi Georgia e CPSC | **CC BY 4.0** (verificata il 20/11/2026) | consentito con attribuzione | https://physionet.org/content/challenge-2021/1.0.3/ |
| MIT-BIH Atrial Fibrillation Database 1.0.0 | ODC-By 1.0 (verificata; non ancora usata) | consentito con attribuzione | https://physionet.org/content/afdb/1.0.0/ |
| Long-Term AF Database 1.0.0 | ODC-By 1.0 (verificata; non usata) | — | https://physionet.org/content/ltafdb/1.0.0/ |
| MIT-BIH Malignant Ventricular Ectopy Database (VFDB) 1.0.0 | ODC-By 1.0 (verificata; non usata) | — | https://physionet.org/content/vfdb/1.0.0/ |
| St Petersburg INCART 12-lead Arrhythmia Database 1.0.0 | ODC-By 1.0 (verificata; non usata) | — | https://physionet.org/content/incartdb/1.0.0/ |

Testi di licenza: PTB-XL `LICENSE.txt` nella cartella dei file (CC BY 4.0, scaricato e letto);
ODC-By 1.0: https://physionet.org/content/mitdb/view-license/1.0.0/ (e analoghe per le altre banche).

**Nota sulla natura delle licenze.** CC BY 4.0 e ODC-By 1.0 consentono riproduzione, adattamento e uso
commerciale (quindi anche un libro venduto su KDP) **a condizione dell'attribuzione**. CC BY 4.0 chiede anche
di **indicare se il materiale è stato modificato**: i tracciati sono filtrati (0,5–40 Hz) e ridisegnati su
griglia; lo si dichiara nella didascalia breve e nella pagina delle fonti. ODC-By riguarda il database:
riprodurre singoli estratti ridisegnati è un uso coperto, con attribuzione. Nessuna delle due licenze
implica l'approvazione dell'opera da parte degli autori delle banche dati: non lo si deve suggerire.

## Attribuzioni da riportare nel libro

### In didascalia (forma breve, generata automaticamente da `select_real.py`)
- «Tracciato reale – PTB-XL ecg_id NNNNN (PhysioNet) – CC BY 4.0; filtrato 0,5–40 Hz e ridisegnato»
- «Tracciato reale – MIT-BIH Arrhythmia Database, record NNN (PhysioNet) – ODC-By 1.0; filtrato 0,5–40 Hz e ridisegnato»
- «Tracciato reale – CU Ventricular Tachyarrhythmia Database, record cuNN (PhysioNet) – ODC-By 1.0; filtrato e ridisegnato»

### Nella pagina «Fonti delle figure» (Parte 11), testo completo
Citazioni richieste dalle pagine PhysioNet («When using this resource, please cite…»), copiate dalla pagina ufficiale:

**PTB-XL**
- Wagner, P., Strodthoff, N., Bousseljot, R., Samek, W., & Schaeffter, T. (2022). *PTB-XL, a large publicly available electrocardiography dataset* (version 1.0.3). PhysioNet. RRID:SCR_007345. https://doi.org/10.13026/kfzx-aw45
- Pubblicazione originale: Wagner, P., Strodthoff, N., Bousseljot, R.-D., Kreiseler, D., Lunze, F.I., Samek, W., Schaeffter, T. (2020). PTB-XL: A Large Publicly Available ECG Dataset. *Scientific Data*. https://doi.org/10.1038/s41597-020-0495-6
- Licenza: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ – segnali filtrati e ridisegnati.

**MIT-BIH Arrhythmia Database**
- Moody, G., & Mark, R. (2005). *MIT-BIH Arrhythmia Database* (version 1.0.0). PhysioNet. RRID:SCR_007345. https://doi.org/10.13026/C2F305
- Pubblicazione originale: Moody GB, Mark RG. The impact of the MIT-BIH Arrhythmia Database. *IEEE Eng in Med and Biol* 20(3):45-50 (May-June 2001). (PMID: 11446209)
- Licenza: ODC-By 1.0.

**CU Ventricular Tachyarrhythmia Database**
- Pubblicazione originale: Nolle FM, Badura FK, Catlett JM, Bowser RW, Sketch MH. CREI-GARD, a new concept in computerized arrhythmia monitoring systems. *Computers in Cardiology* 13:515-518 (1986).
- Licenza: ODC-By 1.0.

**Chapman-Shaoxing/Ningbo (ecg-arrhythmia)**
- Zheng, J., Guo, H., & Chu, H. (2022). *A large scale 12-lead electrocardiogram database for arrhythmia study* (version 1.0.0). PhysioNet. RRID:SCR_007345. https://doi.org/10.13026/wgex-er52
- Pubblicazione originale: Zheng, J., Chu, H., Struppa, D., Zhang, J., Yacoub, S.M., El-Askary, H., Chang, A., Ehwerhemuepha, L., Abudayyeh, I., Barrett, A.S., Fu, G., Yao, H., Li, D., Guo, H., & Rakovski, C. (2020). Optimal Multi-Stage Arrhythmia Classification Approach. *Scientific Reports*, 10. https://www.nature.com/articles/s41598-020-59821-7
- Licenza: CC BY 4.0 – segnali filtrati e ridisegnati.

**PhysioNet/Computing in Cardiology Challenge 2021** (se si usano i sottoinsiemi Georgia/CPSC)
- Reyna, M., Sadr, N., Gu, A., Perez Alday, E. A., Liu, C., Seyedi, S., Shah, A., & Clifford, G. (2022). *Will Two Do? Varying Dimensions in Electrocardiography: The PhysioNet/Computing in Cardiology Challenge 2021* (version 1.0.3). PhysioNet. https://doi.org/10.13026/34va-7q14
- Pubblicazione originale: Reyna MA, Sadr N, Perez Alday EA, et al. Will Two Do? Varying Dimensions in Electrocardiography: The PhysioNet/Computing in Cardiology Challenge 2021. 2021 Computing in Cardiology (CinC), Brno, 2021, pp. 1-4. doi: 10.23919/CinC53138.2021.9662687
- Licenza: CC BY 4.0.

**Citazione standard di PhysioNet** (richiesta per tutte le banche dati):
- Pollard, T., Moody, B. E., Lehman, L., Gow, B., Fernandes, C., Xie, C., Johnson, A., Mark, R. G., & Heldt, T. (2026). PhysioNet as a global platform for biomedical research. *Nature Health*. https://doi.org/10.1038/s44360-026-00096-z

> Le citazioni sono riportate come appaiono sulle pagine PhysioNet al 19/11/2026; in particolare la «citazione
> standard» di PhysioNet è cambiata nel 2026 (in precedenza Goldberger et al., *Circulation* 2000): ricontrollare
> prima della stampa.

## Tracciati simulati e schemi
- **Tracciati didattici simulati** (`figure/sim`): generati con codice originale per questo volume
  (`ecgsim.py`); nessun dato di terzi. Etichetta in didascalia: «Tracciato didattico simulato (ID)».
- **Schemi** (`figure/schemi`): disegnati con codice (matplotlib), curve calcolate, nessuna immagine copiata.
  Etichetta: «Schema originale».
- Nessuna figura proviene da libri, atlanti o siti protetti da copyright. Non sono stati consultati né usati
  testi o figure di manuali ECG commerciali. In particolare il manuale di Dale Dubin **non è stato aperto né
  usato** come fonte (decisione del 20/11/2026, coerente con il brief): le lacune sono state colmate con
  banche dati aperte e con il simulatore.

## Font incorporati nel PDF
- Gelasio (SIL Open Font License 1.1) – `engine/fonts/LICENSE-Gelasio-OFL.txt`.
- DejaVu Sans, solo per simboli e lettere greche (licenza Bitstream Vera / DejaVu, libera anche per uso
  commerciale) – `engine/fonts/LICENSE-DejaVu.txt`.
- Testo delle figure: DejaVu Sans convertito in tracciati (nessun font incorporato nelle immagini).

## Regole per aggiungere nuove fonti
1. Verificare la licenza sulla pagina **della versione** usata («view-license»).
2. Usare solo licenze che consentono la riproduzione in un libro commerciale con attribuzione
   (CC BY, ODC-By, CC0, pubblico dominio). **Non** usare: PhysioNet Credentialed Health Data License,
   Restricted Health Data License, CC BY-NC, CC BY-ND, licenze «solo ricerca».
3. Aggiungere qui banca dati, versione, licenza, citazioni e data di verifica.
