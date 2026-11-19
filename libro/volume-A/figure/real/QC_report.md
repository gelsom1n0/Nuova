# QC dei tracciati reali

Generato da `select_real.py`. Per ogni candidato con etichetta ad alta confidenza sono state calcolate misure oggettive (`common/ecgmeasure.py`) e confrontate con l'etichetta attesa. I candidati incoerenti sono scartati e **non** compaiono nel MANIFEST. Le misure automatiche hanno precisione ±10–20 ms e non sostituiscono la revisione clinica: tutti i tracciati accettati restano `da_validare`.

| Categoria | Sorgente | Esito | Motivo | FC | RR CV | PR | QRS | QTc |
|---|---|---|---|---|---|---|---|---|
| NORM | PTB-XL ecg_id 3 | accettato | coerente | 64.1 | 0.021 | 144 | 76 | 424 |
| NORM | PTB-XL ecg_id 7 | accettato | coerente | 62.2 | 0.018 | 150 | 92 | 389 |
| NORM | PTB-XL ecg_id 10 | **scartato** | qtc_bazett_ms=326 (atteso 340–465) | 62.4 | 0.075 | 188 | 82 | 326 |
| NORM | PTB-XL ecg_id 14 | accettato | coerente | 76.1 | 0.079 | 136 | 76 | 417 |
| NORM | PTB-XL ecg_id 19 | **scartato** | pr_ms=218 (atteso 110–215); qtc_bazett_ms=323 (atteso 340–465) | 57.6 | 0.082 | 218 | 84 | 323 |
| NORM | PTB-XL ecg_id 21 | accettato | coerente | 73.2 | 0.068 | 164 | 72 | 358 |
| STACH | PTB-XL ecg_id 108 | accettato | coerente | 121.5 | 0.02 | 152 | 72 | 427 |
| STACH | PTB-XL ecg_id 698 | accettato | coerente | 113.2 | 0.007 | 140 | 74 | 387 |
| STACH | PTB-XL ecg_id 887 | accettato | coerente | 103.1 | 0.002 | 140 | 64 | 412 |
| STACH | PTB-XL ecg_id 969 | accettato | coerente | 118.1 | 0.012 | 162 | 78 | 398 |
| SBRAD | PTB-XL ecg_id 2 | accettato | coerente | 46.9 | 0.059 | 198 | 82 | 336 |
| SBRAD | PTB-XL ecg_id 12 | accettato | coerente | 48.2 | 0.049 | 124 | 78 | 364 |
| SBRAD | PTB-XL ecg_id 78 | accettato | coerente | 44.4 | 0.064 | 202 | 82 | 346 |
| SBRAD | PTB-XL ecg_id 225 | accettato | coerente | 59.5 | 0.031 | 196 | 88 | 396 |
| SARRH | PTB-XL ecg_id 37 | accettato | coerente | 57.1 | 0.073 | 112 | 78 | 355 |
| SARRH | PTB-XL ecg_id 98 | accettato | coerente | 64.5 | 0.121 | 240 | 82 | 336 |
| SARRH | PTB-XL ecg_id 122 | accettato | coerente | 62.5 | 0.107 | 154 | 92 | 369 |
| SARRH | PTB-XL ecg_id 149 | accettato | coerente | 70.8 | 0.108 | 158 | 78 | 363 |
| AFIB | PTB-XL ecg_id 4117 | **scartato** | p_presente=True (atteso False) | 137.3 | 0.224 | 300 | 78 | 408 |
| AFIB | PTB-XL ecg_id 8215 | accettato | coerente | 80.2 | 0.134 | None | 90 | 391 |
| AFIB | PTB-XL ecg_id 12542 | **scartato** | p_presente=True (atteso False) | 47.7 | 0.21 | 156 | 86 | 358 |
| AFIB | PTB-XL ecg_id 14221 | accettato | coerente | 65.8 | 0.117 | None | 88 | 404 |
| AFIB | PTB-XL ecg_id 15834 | accettato | coerente | 70.5 | 0.283 | None | 94 | 473 |
| AFIB | PTB-XL ecg_id 20406 | accettato | coerente | 69.9 | 0.31 | None | 80 | 343 |
| AFLT | PTB-XL ecg_id 23 | accettato | coerente | 127.7 | 0.013 | 204 | 78 | 260 |
| AFLT | PTB-XL ecg_id 449 | accettato | coerente | 173.4 | 0.042 | None | 70 | 527 |
| AFLT | PTB-XL ecg_id 1773 | accettato | coerente | 63.9 | 0.279 | None | 86 | 388 |
| AFLT | PTB-XL ecg_id 2430 | **scartato** | fc=47.0 (atteso 50–190) | 47.0 | 0.141 | 120 | 82 | 393 |
| AFLT | PTB-XL ecg_id 2739 | accettato | coerente | 147.8 | 0.013 | 316 | 84 | 417 |
| 1AVB | PTB-XL ecg_id 2509 | accettato | coerente | 88.5 | 0.01 | 346 | 78 | 408 |
| 1AVB | PTB-XL ecg_id 3496 | accettato | coerente | 73.2 | 0.019 | 252 | 80 | 409 |
| 1AVB | PTB-XL ecg_id 3658 | accettato | coerente | 80.6 | 0.044 | 316 | 78 | 396 |
| 1AVB | PTB-XL ecg_id 3948 | accettato | coerente | 68.3 | 0.011 | 228 | 88 | 397 |
| 2AVB | PTB-XL ecg_id 14009 | accettato | pause compatibili con P bloccate (RR max/min ≥ 1,35) | 93.6 | 0.252 | 354 | 72 | 415 |
| 3AVB | PTB-XL ecg_id 8620 | accettato | coerente | 37.4 | 0.005 | None | 170 | 412 |
| CRBBB | PTB-XL ecg_id 621 | **scartato** | qrs_ms=112 (atteso 115–200) | 58.1 | 0.017 | 270 | 112 | 419 |
| CRBBB | PTB-XL ecg_id 903 | accettato | coerente | 85.0 | 0.043 | 172 | 132 | 428 |
| CRBBB | PTB-XL ecg_id 1024 | accettato | coerente | 73.0 | 0.027 | 182 | 118 | 432 |
| CRBBB | PTB-XL ecg_id 1123 | accettato | coerente | 69.1 | 0.013 | 226 | 132 | 434 |
| CRBBB | PTB-XL ecg_id 2034 | accettato | coerente | 78.5 | 0.016 | 166 | 128 | 462 |
| CLBBB | PTB-XL ecg_id 286 | accettato | coerente | 55.1 | 0.035 | 164 | 150 | 412 |
| CLBBB | PTB-XL ecg_id 338 | accettato | coerente | 75.2 | 0.006 | 228 | 144 | 430 |
| CLBBB | PTB-XL ecg_id 517 | accettato | coerente | 129.9 | 0.166 | 252 | 150 | 453 |
| CLBBB | PTB-XL ecg_id 618 | accettato | coerente | 69.3 | 0.028 | 168 | 134 | 428 |
| LVH | PTB-XL ecg_id 138 | accettato | Sokolow-Lyon 5.00 mV o R aVL 0.12 mV | 92.6 | 0.005 | 178 | 76 | 405 |
| LVH | PTB-XL ecg_id 542 | accettato | Sokolow-Lyon 3.83 mV o R aVL 0.17 mV | 66.8 | 0.027 | 194 | 88 | 378 |
| LVH | PTB-XL ecg_id 1370 | accettato | Sokolow-Lyon 3.61 mV o R aVL 0.82 mV | 66.7 | 0.01 | 208 | 94 | 386 |
| LVH | PTB-XL ecg_id 1451 | accettato | Sokolow-Lyon 5.13 mV o R aVL 0.94 mV | 85.2 | 0.015 | 186 | 108 | 422 |
| AMI | PTB-XL ecg_id 15865 | accettato | coerente | 66.0 | 0.03 | 220 | 100 | 394 |
| AMI | PTB-XL ecg_id 17493 | accettato | coerente | 52.2 | 0.044 | 186 | 84 | 362 |
| ASMI | PTB-XL ecg_id 177 | accettato | coerente | 94.0 | 0.005 | 326 | 94 | 373 |
| ASMI | PTB-XL ecg_id 492 | accettato | coerente | 75.9 | 0.028 | 342 | 84 | 425 |
| ASMI | PTB-XL ecg_id 518 | accettato | coerente | 65.0 | 0.019 | 198 | 80 | 323 |
| ASMI | PTB-XL ecg_id 1278 | accettato | coerente | 102.0 | 0.02 | 144 | 74 | 428 |
| IMI | PTB-XL ecg_id 290 | accettato | coerente | 69.6 | 0.016 | 184 | 80 | 390 |
| IMI | PTB-XL ecg_id 532 | accettato | coerente | 78.3 | 0.014 | None | 98 | 338 |
| IMI | PTB-XL ecg_id 1373 | accettato | coerente | 55.4 | 0.009 | 164 | 84 | 378 |
| IMI | PTB-XL ecg_id 1577 | accettato | coerente | 89.6 | 0.003 | 372 | 72 | 401 |
| LMI | PTB-XL ecg_id 4712 | accettato | coerente | 47.5 | 0.013 | 200 | 96 | 409 |
| LMI | PTB-XL ecg_id 10873 | accettato | coerente | 79.4 | 0.013 | 138 | 82 | 393 |
| PVC | PTB-XL ecg_id 219 | accettato | battito prematuro con pausa | 73.7 | 0.106 | 186 | 96 | 403 |
| PVC | PTB-XL ecg_id 628 | accettato | battito prematuro con pausa | 64.1 | 0.486 | 256 | 154 | 498 |
| PVC | PTB-XL ecg_id 1993 | accettato | battito prematuro con pausa | 72.6 | 0.188 | 166 | 80 | 401 |
| PVC | PTB-XL ecg_id 2910 | accettato | battito prematuro con pausa | 88.6 | 0.185 | 300 | 80 | 391 |
| PAC | PTB-XL ecg_id 4478 | accettato | battito prematuro | 75.6 | 0.226 | None | 84 | 400 |
| PAC | PTB-XL ecg_id 5434 | accettato | battito prematuro | 57.4 | 0.131 | 196 | 104 | 350 |
| PAC | PTB-XL ecg_id 15588 | accettato | battito prematuro | 73.3 | 0.268 | 184 | 76 | 376 |
| PAC | PTB-XL ecg_id 20149 | accettato | battito prematuro | 59.8 | 0.135 | 160 | 94 | 355 |
| PACE | PTB-XL ecg_id 144 | accettato | coerente | 70.4 | 0.008 | None | 194 | 507 |
| PACE | PTB-XL ecg_id 1641 | accettato | coerente | 69.9 | 0.04 | None | 196 | 475 |
| PACE | PTB-XL ecg_id 1674 | accettato | coerente | 70.4 | 0.001 | None | 202 | 501 |
| PACE | PTB-XL ecg_id 2090 | accettato | coerente | 72.1 | 0.002 | 292 | 162 | 469 |
| WPW | PTB-XL ecg_id 2145 | accettato | coerente | 76.9 | 0.04 | None | 112 | 421 |
| WPW | PTB-XL ecg_id 5303 | **scartato** | qrs_ms=88 (atteso 95–200) | 69.6 | 0.041 | 352 | 88 | 343 |
| WPW | PTB-XL ecg_id 6240 | accettato | coerente | 79.4 | 0.023 | 320 | 166 | 458 |
| WPW | PTB-XL ecg_id 9795 | accettato | coerente | 50.7 | 0.017 | 94 | 154 | 401 |
| WPW | PTB-XL ecg_id 9823 | accettato | coerente | 64.0 | 0.012 | 146 | 120 | 426 |
| SVTAC | — | **NESSUN CANDIDATO** | 0 candidati esaminati, nessuno coerente |  |  |  |  |  |
| VT | MIT-BIH record 223, da 9:38.5 | accettato | coerente | 109.1 | 0.125 | None | 167 | 539 |
| VT | MIT-BIH record 223, da 17:23.4 | accettato | coerente | 107.5 | 0.149 | None | 136 | 416 |
| BIGEM | MIT-BIH record 119, da 21:31.9 | accettato | coerente | 61.8 | 0.438 | None | 89 | 615 |
| BIGEM | MIT-BIH record 119, da 22:08.9 | accettato | coerente | 64.1 | 0.423 | None | 122 | 666 |
| BIGEM | MIT-BIH record 119, da 24:45.2 | accettato | coerente | 64.9 | 0.401 | None | 125 | 679 |
| MIT_AFIB | MIT-BIH record 201, da 0:00.4 | accettato | coerente | 84.0 | 0.15 | None | 94 | 408 |
| MIT_AFIB | MIT-BIH record 201, da 7:57.5 | accettato | coerente | 114.9 | 0.462 | None | 78 | 638 |
| MIT_AFIB | MIT-BIH record 201, da 26:36.7 | accettato | coerente | 108.0 | 0.227 | None | 78 | 481 |
| MIT_AFL | MIT-BIH record 202, da 25:27.4 | accettato | verifica visiva delle onde F | 130.9 | 0.078 | 289 | 83 | 537 |
| MIT_AFL | MIT-BIH record 203, da 12:39.6 | accettato | verifica visiva delle onde F | 120.0 | 0.274 | None | 100 | 412 |
| MIT_AFL | MIT-BIH record 203, da 13:03.2 | accettato | verifica visiva delle onde F | 126.3 | 0.256 | None | 111 | 415 |
| MIT_BII | MIT-BIH record 231, da 1:37.8 | accettato | coerente | 35.3 | 0.02 | 189 | 86 | 379 |
| MIT_BII | MIT-BIH record 231, da 5:33.8 | accettato | coerente | 34.3 | 0.028 | 189 | 83 | 387 |
| MIT_BII | MIT-BIH record 231, da 13:20.0 | accettato | coerente | 35.0 | 0.02 | 175 | 86 | 380 |
| MIT_PACED | MIT-BIH record 102, da 0:00.4 | accettato | coerente | 74.1 | 0.051 | 367 | 119 | 457 |
| MIT_PACED | MIT-BIH record 102, da 2:55.1 | accettato | coerente | 72.5 | 0.032 | 367 | 194 | 482 |
| MIT_PACED | MIT-BIH record 104, da 3:49.3 | accettato | coerente | 73.5 | 0.029 | 372 | 189 | 553 |
| MIT_SVTA | MIT-BIH record 209, da 9:15.9 | accettato | coerente | 154.3 | 0.096 | 197 | 69 | 468 |
| MIT_SVTA | MIT-BIH record 209, da 9:59.6 | accettato | coerente | 156.5 | 0.02 | None | 69 | 444 |
| MIT_SVTA | MIT-BIH record 209, da 12:13.8 | accettato | coerente | 156.5 | 0.099 | 189 | 69 | 453 |
| VF | CUDB cu01, da 214.7 s | accettato | ampiezza max 1.91 mV |  |  |  |  |  |
| VF | CUDB cu03, da 466.2 s | accettato | ampiezza max 1.9 mV |  |  |  |  |  |
| VF | CUDB cu04, da 155.8 s | accettato | ampiezza max 1.22 mV |  |  |  |  |  |

Totale: 93 accettati, 7 scartati, 1 categorie senza candidati.
