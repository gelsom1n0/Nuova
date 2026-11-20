# QC dei tracciati reali

Generato da `select_real.py`. Per ogni candidato con etichetta ad alta confidenza sono state calcolate misure oggettive (`common/ecgmeasure.py`) e confrontate con l'etichetta attesa. I candidati incoerenti sono scartati e **non** compaiono nel MANIFEST. Le misure automatiche hanno precisione ±10–20 ms e non sostituiscono la revisione clinica: tutti i tracciati accettati restano `da_validare`.

| Categoria | Sorgente | Esito | Motivo | FC | RR CV | PR | QRS | QTc |
|---|---|---|---|---|---|---|---|---|
| NORM | PTB-XL ecg_id 3 | accettato | coerente | 64.1 | 0.021 | 144 | 76 | 422 |
| NORM | PTB-XL ecg_id 7 | accettato | coerente | 62.2 | 0.018 | 150 | 92 | 389 |
| NORM | PTB-XL ecg_id 10 | **scartato** | qtc_bazett_ms=326 (atteso 340–465) | 62.4 | 0.075 | 184 | 82 | 326 |
| NORM | PTB-XL ecg_id 14 | accettato | coerente | 76.1 | 0.079 | 136 | 76 | 417 |
| NORM | PTB-XL ecg_id 19 | **scartato** | pr_ms=218 (atteso 110–215); qtc_bazett_ms=323 (atteso 340–465) | 57.6 | 0.082 | 218 | 84 | 323 |
| NORM | PTB-XL ecg_id 21 | accettato | coerente | 73.2 | 0.068 | 166 | 72 | 358 |
| STACH | PTB-XL ecg_id 108 | accettato | coerente | 121.5 | 0.02 | 156 | 72 | 427 |
| STACH | PTB-XL ecg_id 698 | accettato | coerente | 113.2 | 0.007 | 138 | 74 | 385 |
| STACH | PTB-XL ecg_id 887 | accettato | coerente | 103.1 | 0.002 | 140 | 64 | 412 |
| STACH | PTB-XL ecg_id 969 | accettato | coerente | 118.1 | 0.012 | 164 | 78 | 398 |
| SBRAD | PTB-XL ecg_id 2 | accettato | coerente | 46.9 | 0.059 | 198 | 82 | 336 |
| SBRAD | PTB-XL ecg_id 12 | accettato | coerente | 48.2 | 0.049 | 122 | 78 | 364 |
| SBRAD | PTB-XL ecg_id 78 | accettato | coerente | 44.4 | 0.064 | 216 | 82 | 346 |
| SBRAD | PTB-XL ecg_id 225 | accettato | coerente | 59.5 | 0.031 | 190 | 88 | 396 |
| SARRH | PTB-XL ecg_id 37 | accettato | coerente | 57.1 | 0.073 | 112 | 78 | 355 |
| SARRH | PTB-XL ecg_id 98 | accettato | coerente | 64.5 | 0.121 | 244 | 82 | 336 |
| SARRH | PTB-XL ecg_id 122 | accettato | coerente | 62.5 | 0.107 | 160 | 92 | 369 |
| SARRH | PTB-XL ecg_id 149 | accettato | coerente | 70.8 | 0.108 | 164 | 78 | 363 |
| AFIB | PTB-XL ecg_id 4117 | **scartato** | p_presente=True (atteso False) | 137.3 | 0.224 | 300 | 78 | 408 |
| AFIB | PTB-XL ecg_id 8215 | accettato | coerente | 80.2 | 0.134 | None | 88 | 391 |
| AFIB | PTB-XL ecg_id 12542 | **scartato** | p_presente=True (atteso False) | 47.7 | 0.21 | 156 | 86 | 358 |
| AFIB | PTB-XL ecg_id 14221 | accettato | coerente | 65.8 | 0.117 | None | 88 | 404 |
| AFIB | PTB-XL ecg_id 15834 | accettato | coerente | 70.5 | 0.283 | None | 94 | 473 |
| AFIB | PTB-XL ecg_id 20406 | accettato | coerente | 69.9 | 0.31 | None | 80 | 343 |
| AFLT | PTB-XL ecg_id 23 | accettato | coerente | 127.7 | 0.013 | 202 | 80 | 263 |
| AFLT | PTB-XL ecg_id 449 | accettato | coerente | 173.4 | 0.042 | None | 72 | 558 |
| AFLT | PTB-XL ecg_id 1773 | accettato | coerente | 63.9 | 0.279 | None | 86 | 390 |
| AFLT | PTB-XL ecg_id 2430 | **scartato** | fc=47.0 (atteso 50–190) | 47.0 | 0.141 | 120 | 82 | 393 |
| AFLT | PTB-XL ecg_id 2739 | accettato | coerente | 147.8 | 0.013 | 316 | 86 | 417 |
| 1AVB | PTB-XL ecg_id 2509 | accettato | coerente | 88.5 | 0.01 | 346 | 78 | 410 |
| 1AVB | PTB-XL ecg_id 3496 | accettato | coerente | 73.2 | 0.019 | 252 | 80 | 406 |
| 1AVB | PTB-XL ecg_id 3658 | accettato | coerente | 80.6 | 0.044 | 232 | 78 | 394 |
| 1AVB | PTB-XL ecg_id 3948 | accettato | coerente | 68.3 | 0.011 | 234 | 88 | 393 |
| 2AVB | PTB-XL ecg_id 14009 | accettato | pause compatibili con P bloccate (RR max/min ≥ 1,35) | 93.6 | 0.252 | 354 | 72 | 415 |
| 3AVB | PTB-XL ecg_id 8620 | accettato | coerente | 37.4 | 0.005 | None | 170 | 414 |
| CRBBB | PTB-XL ecg_id 621 | **scartato** | qrs_ms=112 (atteso 115–200) | 58.1 | 0.017 | 290 | 112 | 415 |
| CRBBB | PTB-XL ecg_id 903 | accettato | coerente | 85.0 | 0.043 | 172 | 132 | 428 |
| CRBBB | PTB-XL ecg_id 1024 | accettato | coerente | 73.0 | 0.027 | 182 | 118 | 435 |
| CRBBB | PTB-XL ecg_id 1123 | accettato | coerente | 69.1 | 0.013 | 226 | 132 | 434 |
| CRBBB | PTB-XL ecg_id 2034 | accettato | coerente | 78.5 | 0.016 | 166 | 126 | 460 |
| CLBBB | PTB-XL ecg_id 286 | accettato | coerente | 55.1 | 0.035 | None | 150 | 410 |
| CLBBB | PTB-XL ecg_id 338 | accettato | coerente | 75.2 | 0.006 | 226 | 142 | 428 |
| CLBBB | PTB-XL ecg_id 517 | accettato | coerente | 129.9 | 0.166 | 252 | 150 | 453 |
| CLBBB | PTB-XL ecg_id 618 | accettato | coerente | 69.3 | 0.028 | 182 | 134 | 428 |
| LVH | PTB-XL ecg_id 138 | accettato | Sokolow-Lyon 5.00 mV o R aVL 0.12 mV | 92.6 | 0.005 | 178 | 76 | 405 |
| LVH | PTB-XL ecg_id 542 | accettato | Sokolow-Lyon 3.82 mV o R aVL 0.17 mV | 66.8 | 0.027 | 188 | 88 | 378 |
| LVH | PTB-XL ecg_id 1370 | accettato | Sokolow-Lyon 3.61 mV o R aVL 0.82 mV | 66.7 | 0.01 | 206 | 94 | 386 |
| LVH | PTB-XL ecg_id 1451 | accettato | Sokolow-Lyon 5.14 mV o R aVL 0.94 mV | 85.2 | 0.015 | 182 | 108 | 422 |
| AMI | PTB-XL ecg_id 15865 | accettato | coerente | 66.0 | 0.03 | 198 | 100 | 394 |
| AMI | PTB-XL ecg_id 17493 | accettato | coerente | 52.2 | 0.044 | 184 | 84 | 362 |
| ASMI | PTB-XL ecg_id 177 | accettato | coerente | 94.0 | 0.005 | 162 | 94 | 371 |
| ASMI | PTB-XL ecg_id 492 | accettato | coerente | 75.9 | 0.028 | 342 | 84 | 425 |
| ASMI | PTB-XL ecg_id 518 | accettato | coerente | 65.0 | 0.019 | 192 | 80 | 323 |
| ASMI | PTB-XL ecg_id 1278 | accettato | coerente | 102.0 | 0.02 | 144 | 74 | 428 |
| IMI | PTB-XL ecg_id 290 | accettato | coerente | 69.6 | 0.016 | 184 | 80 | 392 |
| IMI | PTB-XL ecg_id 532 | accettato | coerente | 78.3 | 0.014 | None | 98 | 338 |
| IMI | PTB-XL ecg_id 1373 | accettato | coerente | 55.4 | 0.009 | 164 | 84 | 378 |
| IMI | PTB-XL ecg_id 1577 | accettato | coerente | 89.6 | 0.003 | 372 | 72 | 401 |
| LMI | PTB-XL ecg_id 4712 | accettato | coerente | 47.5 | 0.013 | 202 | 96 | 409 |
| LMI | PTB-XL ecg_id 10873 | accettato | coerente | 79.4 | 0.013 | 138 | 82 | 393 |
| PVC | PTB-XL ecg_id 219 | accettato | battito prematuro con pausa | 73.7 | 0.106 | 170 | 94 | 403 |
| PVC | PTB-XL ecg_id 628 | accettato | battito prematuro con pausa | 64.1 | 0.486 | 248 | 156 | 391 |
| PVC | PTB-XL ecg_id 1993 | accettato | battito prematuro con pausa | 72.6 | 0.188 | 166 | 80 | 401 |
| PVC | PTB-XL ecg_id 2910 | accettato | battito prematuro con pausa | 88.6 | 0.185 | 360 | 78 | 391 |
| PAC | PTB-XL ecg_id 4478 | accettato | battito prematuro | 75.6 | 0.226 | None | 84 | 400 |
| PAC | PTB-XL ecg_id 5434 | accettato | battito prematuro | 57.4 | 0.131 | 196 | 104 | 348 |
| PAC | PTB-XL ecg_id 15588 | accettato | battito prematuro | 73.3 | 0.268 | 186 | 76 | 376 |
| PAC | PTB-XL ecg_id 20149 | accettato | battito prematuro | 59.8 | 0.135 | 160 | 94 | 355 |
| PACE | PTB-XL ecg_id 144 | accettato | coerente | 70.4 | 0.008 | 282 | 194 | 507 |
| PACE | PTB-XL ecg_id 1641 | accettato | coerente | 69.9 | 0.04 | None | 198 | 471 |
| PACE | PTB-XL ecg_id 1674 | accettato | coerente | 70.4 | 0.001 | None | 204 | 503 |
| PACE | PTB-XL ecg_id 2090 | accettato | coerente | 72.1 | 0.002 | None | 160 | 469 |
| WPW | PTB-XL ecg_id 2145 | accettato | coerente | 76.9 | 0.04 | None | 112 | 421 |
| WPW | PTB-XL ecg_id 5303 | **scartato** | qrs_ms=88 (atteso 95–200) | 69.6 | 0.041 | 352 | 88 | 343 |
| WPW | PTB-XL ecg_id 6240 | accettato | coerente | 79.4 | 0.023 | 320 | 166 | 455 |
| WPW | PTB-XL ecg_id 9795 | accettato | coerente | 50.7 | 0.017 | 94 | 154 | 401 |
| WPW | PTB-XL ecg_id 9823 | accettato | coerente | 64.0 | 0.012 | 146 | 120 | 426 |
| LAFB | PTB-XL ecg_id 41 | accettato | coerente | 72.6 | 0.013 | 168 | 100 | 381 |
| LAFB | PTB-XL ecg_id 157 | accettato | coerente | 63.2 | 0.027 | 174 | 96 | 412 |
| LAFB | PTB-XL ecg_id 226 | accettato | coerente | 76.9 | 0.008 | 196 | 88 | 401 |
| LAFB | PTB-XL ecg_id 285 | accettato | coerente | 82.8 | 0.015 | 156 | 84 | 385 |
| LPFB | PTB-XL ecg_id 377 | accettato | coerente | 96.8 | 0.018 | 330 | 86 | 414 |
| LPFB | PTB-XL ecg_id 6938 | accettato | coerente | 92.0 | 0.006 | 152 | 88 | 438 |
| LPFB | PTB-XL ecg_id 7419 | accettato | coerente | 82.0 | 0.07 | 184 | 86 | 404 |
| LPFB | PTB-XL ecg_id 16116 | accettato | coerente | 69.0 | 0.028 | 164 | 118 | 386 |
| BIFASC | PTB-XL ecg_id 41 | **scartato** | qrs_ms=100 (atteso 120–200) | 72.6 | 0.013 | 168 | 100 | 381 |
| BIFASC | PTB-XL ecg_id 157 | **scartato** | qrs_ms=96 (atteso 120–200) | 63.2 | 0.027 | 174 | 96 | 412 |
| BIFASC | PTB-XL ecg_id 172 | **scartato** | asse_gradi=-123 (atteso -95–-30) | 79.9 | 0.041 | None | 142 | 425 |
| BIFASC | PTB-XL ecg_id 226 | **scartato** | qrs_ms=88 (atteso 120–200) | 76.9 | 0.008 | 196 | 88 | 401 |
| BIFASC | PTB-XL ecg_id 285 | **scartato** | qrs_ms=84 (atteso 120–200) | 82.8 | 0.015 | 156 | 84 | 385 |
| BIFASC | PTB-XL ecg_id 424 | **scartato** | asse_gradi=-108 (atteso -95–-30); qrs_ms=94 (atteso 120–200) | 71.9 | 0.009 | 168 | 94 | 407 |
| BIFASC | PTB-XL ecg_id 447 | **scartato** | qrs_ms=94 (atteso 120–200) | 77.3 | 0.036 | 190 | 94 | 418 |
| BIFASC | PTB-XL ecg_id 479 | **scartato** | qrs_ms=94 (atteso 120–200) | 66.2 | 0.035 | 148 | 94 | 403 |
| BIFASC | PTB-XL ecg_id 520 | **scartato** | qrs_ms=76 (atteso 120–200) | 88.0 | 0.018 | 172 | 76 | 443 |
| BIFASC | PTB-XL ecg_id 633 | **scartato** | qrs_ms=86 (atteso 120–200) | 69.6 | 0.013 | 158 | 86 | 405 |
| BIFASC | PTB-XL ecg_id 659 | **scartato** | qrs_ms=102 (atteso 120–200) | 56.9 | 0.012 | 164 | 102 | 411 |
| BIFASC | PTB-XL ecg_id 680 | **scartato** | asse_gradi=-126 (atteso -95–-30) | 80.8 | 0.018 | 146 | 124 | 374 |
| BIFASC | PTB-XL ecg_id 786 | **scartato** | qrs_ms=84 (atteso 120–200) | 74.1 | 0.013 | 156 | 84 | 356 |
| BIFASC | PTB-XL ecg_id 789 | **scartato** | qrs_ms=82 (atteso 120–200) | 89.7 | 0.008 | 148 | 82 | 421 |
| BIFASC | PTB-XL ecg_id 871 | accettato | coerente | 85.2 | 0.037 | 202 | 128 | 453 |
| BIFASC | PTB-XL ecg_id 940 | **scartato** | qrs_ms=88 (atteso 120–200) | 68.8 | 0.065 | 206 | 88 | 375 |
| RVH | PTB-XL ecg_id 2417 | accettato | asse 58°, R in V1 0.71 mV | 90.9 | 0.016 | None | 90 | 451 |
| LAO/LAE | PTB-XL ecg_id 6685 | accettato | coerente | 80.0 | 0.022 | 174 | 80 | 386 |
| LAO/LAE | PTB-XL ecg_id 6851 | accettato | coerente | 83.1 | 0.011 | 266 | 86 | 494 |
| LAO/LAE | PTB-XL ecg_id 6926 | accettato | coerente | 73.7 | 0.015 | 150 | 78 | 421 |
| LAO/LAE | PTB-XL ecg_id 9944 | accettato | coerente | 97.7 | 0.009 | 146 | 100 | 434 |
| RAO/RAE | PTB-XL ecg_id 1785 | accettato | coerente | 95.5 | 0.1 | 156 | 70 | 366 |
| RAO/RAE | PTB-XL ecg_id 5231 | accettato | coerente | 83.8 | 0.033 | 160 | 90 | 392 |
| RAO/RAE | PTB-XL ecg_id 8177 | accettato | coerente | 73.2 | 0.037 | 168 | 84 | 411 |
| RAO/RAE | PTB-XL ecg_id 15181 | accettato | coerente | 90.2 | 0.043 | 194 | 76 | 405 |
| SVTAC | — | **NESSUN CANDIDATO** | 0 candidati esaminati, nessuno coerente |  |  |  |  |  |
| VT | MIT-BIH record 203 | **scartato** | escluso dopo ispezione visiva: TV polimorfa su FA con molto rumore: poco leggibile come esempio didattico |  |  |  |  |  |
| VT | MIT-BIH record 205, da 4:53.8 | accettato | FC media 128.3/min; salva confermata dalle annotazioni | 168.8 | 0.361 | 164 | 89 | 554 |
| VT | MIT-BIH record 205, da 24:15.5 | accettato | FC media 120.2/min; salva confermata dalle annotazioni | 154.3 | 0.499 | 139 | 81 | 552 |
| VT | MIT-BIH record 205, da 24:26.1 | accettato | FC media 88.9/min; salva confermata dalle annotazioni | 84.0 | 0.203 | 342 | 156 | 500 |
| BIGEM | MIT-BIH record 119, da 21:31.9 | accettato | coerente | 61.8 | 0.438 | None | 89 | 615 |
| BIGEM | MIT-BIH record 119, da 22:08.9 | accettato | coerente | 64.1 | 0.423 | None | 122 | 666 |
| BIGEM | MIT-BIH record 119, da 24:45.2 | accettato | coerente | 64.9 | 0.401 | None | 125 | 679 |
| MIT_AFIB | MIT-BIH record 201, da 0:00.4 | accettato | coerente | 84.0 | 0.15 | None | 83 | 395 |
| MIT_AFIB | MIT-BIH record 201, da 7:57.5 | accettato | coerente | 114.9 | 0.462 | None | 78 | 638 |
| MIT_AFIB | MIT-BIH record 201, da 26:36.7 | accettato | coerente | 108.0 | 0.227 | None | 75 | 477 |
| MIT_AFL | MIT-BIH record 202, da 25:27.4 | accettato | verifica visiva delle onde F | 130.9 | 0.078 | 289 | 83 | 537 |
| MIT_AFL | MIT-BIH record 203, da 12:39.6 | accettato | verifica visiva delle onde F | 120.0 | 0.274 | None | 119 | 409 |
| MIT_AFL | MIT-BIH record 203, da 13:03.2 | accettato | verifica visiva delle onde F | 126.3 | 0.256 | None | 114 | 419 |
| MIT_BII | MIT-BIH record 231, da 1:37.8 | accettato | coerente | 35.3 | 0.02 | 186 | 89 | 379 |
| MIT_BII | MIT-BIH record 231, da 5:33.8 | accettato | coerente | 34.3 | 0.028 | 192 | 86 | 389 |
| MIT_BII | MIT-BIH record 231, da 13:20.0 | accettato | coerente | 35.0 | 0.02 | 175 | 86 | 380 |
| MIT_PACED | MIT-BIH record 102, da 0:00.4 | accettato | coerente | 74.1 | 0.051 | 367 | 119 | 457 |
| MIT_PACED | MIT-BIH record 102, da 2:55.1 | accettato | coerente | 72.5 | 0.032 | 367 | 194 | 482 |
| MIT_PACED | MIT-BIH record 104, da 3:49.3 | accettato | coerente | 73.5 | 0.029 | 372 | 189 | 550 |
| MIT_VFL | MIT-BIH record 207, da 0:35.8 | accettato | flutter ventricolare confermato dalle annotazioni del ritmo; verifica visiva | 136.7 | 0.659 | None | 156 | 633 |
| MIT_VFL | MIT-BIH record 207, da 0:51.9 | accettato | flutter ventricolare confermato dalle annotazioni del ritmo; verifica visiva | 160.0 | 0.619 | None | 58 | 485 |
| MIT_VFL | MIT-BIH record 207, da 3:57.3 | accettato | flutter ventricolare confermato dalle annotazioni del ritmo; verifica visiva | 158.8 | 0.604 | None | 114 | 456 |
| MIT_SVTA | MIT-BIH record 209, da 9:15.9 | accettato | coerente | 154.3 | 0.096 | 211 | 75 | 459 |
| MIT_SVTA | MIT-BIH record 209, da 9:59.6 | accettato | coerente | 156.5 | 0.02 | 103 | 69 | 440 |
| MIT_SVTA | MIT-BIH record 209, da 12:13.8 | accettato | coerente | 156.5 | 0.099 | 189 | 69 | 458 |
| VF | CUDB cu01, da 214.7 s | accettato | ampiezza max 1.86 mV |  |  |  |  |  |
| VF | CUDB cu03, da 466.2 s | accettato | ampiezza max 1.96 mV |  |  |  |  |  |
| VF | CUDB cu04, da 155.8 s | accettato | ampiezza max 1.22 mV |  |  |  |  |  |
| CH_SVT | Chapman JS09908 | accettato | coerente | 215.8 | 0.003 | 148 | 62 | 592 |
| CH_SVT | Chapman JS09913 | accettato | coerente | 190.5 | 0.035 | 156 | 72 | 445 |
| CH_SVT | Chapman JS09916 | accettato | coerente | 155.4 | 0.021 | 222 | 76 | 431 |
| CH_SVT | Chapman JS09917 | accettato | coerente | 178.6 | 0.006 | 200 | 66 | 417 |
| CH_AT | Chapman JS09948 | **scartato** | fc=89.0 (atteso 100–250) | 89.0 | 0.051 | 130 | 76 | 400 |
| CH_AT | Chapman JS09949 | **scartato** | fc=86.2 (atteso 100–250) | 86.2 | 0.115 | 134 | 78 | 429 |
| CH_AT | Chapman JS09955 | **scartato** | fc=70.7 (atteso 100–250) | 70.7 | 0.007 | 170 | 90 | 393 |
| CH_AT | Chapman JS09979 | **scartato** | fc=97.1 (atteso 100–250) | 97.1 | 0.044 | 142 | 74 | 382 |
| CH_AT | Chapman JS10018 | accettato | coerente | 108.7 | 0.011 | 140 | 70 | 417 |
| CH_AT | Chapman JS10027 | **scartato** | fc=93.0 (atteso 100–250) | 93.0 | 0.101 | 118 | 68 | 391 |
| CH_AT | Chapman JS10029 | **scartato** | fc=94.0 (atteso 100–250) | 94.0 | 0.275 | 348 | 76 | 433 |
| CH_AT | Chapman JS10037 | accettato | coerente | 114.9 | 0.01 | 136 | 64 | 390 |
| CH_AT | Chapman JS10040 | **scartato** | fc=78.3 (atteso 100–250) | 78.3 | 0.026 | 106 | 82 | 327 |
| CH_AT | Chapman JS10041 | **scartato** | fc=74.3 (atteso 100–250) | 74.3 | 0.019 | 126 | 82 | 398 |
| CH_AT | Chapman JS10061 | accettato | coerente | 115.4 | 0.009 | 176 | 106 | 413 |
| CH_AT | Chapman JS10065 | **scartato** | fc=82.2 (atteso 100–250) | 82.2 | 0.053 | 114 | 78 | 363 |
| CH_AT | Chapman JS10075 | accettato | coerente | 123.7 | 0.158 | None | 78 | 454 |
| CH_AVRT | Chapman JS10306 | accettato | coerente | 212.8 | 0.002 | 280 | 88 | 591 |
| CH_AVRT | Chapman JS10361 | accettato | coerente | 176.5 | 0.004 | 218 | 72 | 418 |
| CH_AVRT | Chapman JS10449 | accettato | coerente | 145.6 | 0.004 | 254 | 64 | 433 |
| CH_AVRT | Chapman JS10481 | accettato | coerente | 141.5 | 0.007 | 264 | 68 | 409 |
| CH_2AVB1 | Chapman JS12426 | accettato | RR max/min 1.97/1.01 (battiti raggruppati attesi) | 57.5 | 0.269 | 360 | 102 | 366 |
| CH_2AVB1 | Chapman JS12427 | accettato | RR max/min 2.094/0.912 (battiti raggruppati attesi) | 58.9 | 0.308 | None | 76 | 333 |
| CH_2AVB1 | Chapman JS12428 | accettato | RR max/min 1.882/1.01 (battiti raggruppati attesi) | 54.8 | 0.254 | 216 | 78 | 354 |
| CH_2AVB1 | Chapman JS12429 | accettato | RR max/min 1.738/1.032 (battiti raggruppati attesi) | 55.1 | 0.188 | 226 | 100 | 387 |
| CH_3AVB | Chapman JS10683 | **scartato** | derivazione piatta o con dati mancanti |  |  |  |  |  |
| CH_3AVB | Chapman JS12517 | **scartato** | fc=62.0 (atteso 20–60) | 62.0 | 0.004 | 238 | 208 | 335 |
| CH_3AVB | Chapman JS12518 | accettato | coerente | 46.2 | 0.041 | 222 | 160 | 448 |
| CH_3AVB | Chapman JS12519 | accettato | coerente | 46.4 | 0.002 | 292 | 148 | 403 |
| CH_3AVB | Chapman JS12520 | **scartato** | derivazione piatta o con dati mancanti |  |  |  |  |  |
| CH_3AVB | Chapman JS12521 | accettato | coerente | 33.2 | 0.017 | 148 | 114 | 379 |
| CH_3AVB | Chapman JS12523 | accettato | coerente | 52.9 | 0.005 | None | 170 | 366 |
| CH_WPW | Chapman JS02697 | **scartato** | qrs_ms=78 (atteso 95–200) | 101.4 | 0.021 | 148 | 78 | 369 |
| CH_WPW | Chapman JS06083 | accettato | coerente | 58.1 | 0.012 | 324 | 118 | 398 |
| CH_WPW | Chapman JS10729 | **scartato** | derivazione piatta o con dati mancanti |  |  |  |  |  |
| CH_WPW | Chapman JS11155 | accettato | coerente | 105.3 | 0.344 | None | 114 | 577 |
| CH_WPW | Chapman JS22818 | accettato | coerente | 108.7 | 0.023 | 96 | 152 | 415 |
| CH_WPW | Chapman JS24883 | **scartato** | qrs_ms=88 (atteso 95–200) | 51.0 | 0.029 | 358 | 88 | 402 |
| CH_WPW | Chapman JS24884 | accettato | coerente | 57.0 | 0.037 | 132 | 158 | 411 |
| CH_JEB | Chapman JS06588 | accettato | coerente | 60.1 | 0.164 | None | 84 | 390 |
| CH_JEB | Chapman JS09293 | **scartato** | fc=65.1 (atteso 30–65) | 65.1 | 0.205 | 142 | 94 | 444 |
| CH_JEB | Chapman JS22356 | accettato | coerente | 46.9 | 0.112 | 272 | 92 | 448 |
| CH_ERV | Chapman JS00532 | accettato | coerente | 64.5 | 0.036 | 174 | 88 | 344 |
| CH_ERV | Chapman JS00724 | accettato | coerente | 53.6 | 0.047 | 182 | 78 | 401 |
| CH_ERV | Chapman JS01576 | accettato | coerente | 53.1 | 0.012 | 184 | 90 | 361 |
| CH_ERV | Chapman JS02418 | accettato | coerente | 46.1 | 0.035 | 124 | 86 | 380 |
| CH_ABI | Chapman JS06795 | accettato | coerente | 51.0 | 0.147 | 156 | 96 | 365 |
| CH_SAAWR | — | **NESSUN CANDIDATO** | 0 candidati con etichetta unica, nessuno coerente |  |  |  |  |  |
| CH_VB | Chapman JS03908 | accettato | coerente | 54.6 | 0.189 | 124 | 98 | 370 |
| BRUGADA | Brugada-HUCA patient_id 188981 | accettato | ST J+60 in V1/V2 max +0.20 mV | 52.4 | 0.023 | 300 | 150 | 374 |
| BRUGADA | Brugada-HUCA patient_id 428031 | accettato | ST J+60 in V1/V2 max +0.24 mV | 75.0 | 0.008 | None | 110 | 436 |
| BRUGADA | Brugada-HUCA patient_id 852786 | accettato | ST J+60 in V1/V2 max +0.35 mV | 93.8 | 0.031 | 140 | 130 | 400 |

Totale: 150 accettati, 39 scartati, 2 categorie senza candidati.
