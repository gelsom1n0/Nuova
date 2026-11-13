#!/usr/bin/env python3
"""Seconda passata di espansione: sintesi di fine Parte per saturare le pagine finali."""
import re
from pathlib import Path
VOL = Path(__file__).resolve().parent.parent / "volumi" / "01-betabloccanti"
ADD = {}

ADD[("parte-01.md", "Fisiologia cardiaca essenziale")] = """
### Sintesi della Parte I: dalla fisiologia alla clinica

| Elemento fisiologico | Effetto del blocco β | Conseguenza clinica |
|---|---|---|
| Frequenza sinusale (β1, I<sub>f</sub>) | Riduzione | Meno tachicardia, più diastole, effetto antianginoso |
| Conduzione AV (β1) | Rallentamento | Controllo della frequenza in FA; rischio di blocchi |
| Contrattilità (β1) | Riduzione | Minor consumo di O2; rischio di scompenso se avviato in modo scorretto |
| Renina (β1) | Riduzione | Contributo antipertensivo e antiremodellamento |
| Tono bronchiale (β2) | Aumento del tono con molecole non selettive | Rischio broncospasmo in asma |
| Glicogenolisi e risposta all'ipoglicemia (β2) | Attenuazione | Recupero ritardato, sintomi mascherati |
| Vasodilatazione muscolare (β2) | Ridotta | Estremità fredde, affaticabilità |
| Attività simpatica cronica nello scompenso | Protezione dalla tossicità adrenergica | Beneficio prognostico nell'HFrEF |
| Upregulation recettoriale da blocco cronico | Ipersensibilità alla sospensione | Rebound se interrotto bruscamente |

Questa tabella è il «filo rosso» del manuale: quasi ogni effetto utile e ogni effetto indesiderato dei betabloccanti si può dedurre da una riga di essa. Quando si incontra una nuova situazione clinica, la domanda guida è: quale recettore e quale organo sono coinvolti, e quale ruolo ha il tono simpatico di base?
"""

ADD[("parte-02.md", "Farmacocinetica")] = """
### Implicazioni pratiche per chi assiste

La farmacocinetica non è teoria astratta: stabilisce **quando** controllare il paziente e **che cosa** aspettarsi. Un farmaco a emivita breve richiede più somministrazioni e dà più rischio di rebound; uno a emivita lunga ha effetti prolungati se compare bradicardia. Nel paziente anziano con ridotta clearance o nel nefropatico, il controllo clinico dopo avvio o variazione di dose va posticipato di qualche giorno, perché lo stato stazionario si raggiunge più tardi. Dopo l'inizio di un farmaco inibitore del CYP2D6, la frequenza cardiaca va ricontrollata nei giorni seguenti.
"""

ADD[("parte-04.md", "Altre aritmie")] = """
### Sintesi della Parte IV: forza dell'indicazione (didattica)

| Indicazione | Ruolo del betabloccante | Forza dell'indicazione |
|---|---|---|
| HFrEF | Pilastro della terapia | Forte (classe I, ESC 2021/2023) |
| Post-infarto con FE ridotta | Raccomandato | Forte (ESC 2023) |
| Angina cronica | Opzione di prima linea (con CCB) | Forte per il sintomo (ESC 2024) |
| Controllo frequenza in FA | Prima linea | Forte (ESC 2024) |
| QT lungo, CPVT | Prima linea | Forte (ESC 2022) |
| Post-infarto con FE conservata | Individualizzare | In evoluzione (REDUCE-AMI, REBOOT, ABYSS) |
| Ipertensione senza altre indicazioni | Non prima linea | ESC 2024 |
| Chirurgia non cardiaca | Proseguire se già in terapia; non avviare di routine | ESC 2022, POISE |

La colonna «forza» è una sintesi didattica e non riproduce testualmente le classi di raccomandazione, per le quali si rimanda ai documenti originali.
"""

ADD[("parte-07.md", "Educazione del paziente")] = """
### Piano assistenziale tipo

Una traccia di pianificazione, in stile diagnosi infermieristiche, per un paziente in avvio di betabloccante per scompenso:

| Problema o rischio | Obiettivo | Interventi principali |
|---|---|---|
| Rischio di ridotta gittata cardiaca (bradicardia, ipotensione) | Frequenza e pressione nei limiti concordati | Misurazione prima di ogni dose; ECG se sintomi; segnalazione tempestiva |
| Rischio di cadute (ortostatismo, astenia) | Nessuna caduta | Alzarsi per gradi; ambiente sicuro; verifica dei sintomi al risveglio |
| Rischio di sovraccarico di liquidi | Peso stabile, assenza di edemi | Peso quotidiano; registro; segnalazione per aumento > 2 kg in 3 giorni |
| Rischio di ipoglicemia non riconosciuta (se diabete) | Glicemia nei limiti | Automonitoraggio; insegnare i sintomi che persistono (sudorazione, confusione) |
| Conoscenze insufficienti sul farmaco | Il paziente spiega nome, scopo, segni d'allarme | Educazione con teach-back; materiale scritto |
| Rischio di non aderenza | Assunzione regolare | Organizer; coinvolgere caregiver; pianificare le ricette |

### Rivalutazione

Il piano si rivaluta a ogni visita: il paziente raggiunge la dose prevista? Ha avuto sintomi? Ricorda i messaggi chiave? Gli obiettivi sono ancora adatti? La rivalutazione documentata è parte della continuità assistenziale.
"""

ADD[("parte-10.md", "Caso 3 – Fibrillazione atriale rapida in un paziente con BPCO")] = """
### Casi lampo

!!! nota "Nota – Tre vignette per l'esercitazione"
    **A.** Una donna di 72 anni in terapia con metoprololo e verapamil riferisce vertigini e sincope; frequenza 38 bpm, blocco AV di III grado all'ECG. *Che cosa si sospetta e quali azioni immediate?* (Interazione tra due farmaci rallentanti: avvisare il medico, monitor, atropina, stimolazione; sospensione dei farmaci.)

    **B.** Un uomo di 55 anni diabetico in terapia con insulina e propranololo arriva confuso; sudato, frequenza 74 bpm, glicemia 38 mg/dl. *Perché la tachicardia manca?* (Il betabloccante maschera tachicardia e tremore; la sudorazione rimane; trattare l'ipoglicemia.)

    **C.** Una paziente con asma in terapia con colliri per il glaucoma sviluppa dispnea e sibili. *Quale farmaco sospettare?* (Collirio con timololo: assorbimento sistemico e blocco β2.)

### Come usare i casi per lo studio

Per ogni caso conviene scrivere una risposta in 5 righe, individuare i dati decisivi, formulare il problema principale, elencare tre azioni infermieristiche e due elementi di educazione. Poi confrontare con la discussione. Ripetere dopo qualche settimana senza guardare le note è un modo efficace per fissare i concetti. Quando in futuro si aggiungeranno altre classi di farmaci, questa struttura potrà essere riusata per confronti tra classi.
"""

def main():
    files, n = {}, 0
    for (fname, key), text in ADD.items():
        p = VOL / fname
        t = files.get(fname) or p.read_text(encoding="utf-8")
        marker = f"<!-- exp2:{key} -->"
        if marker in t: files[fname] = t; continue
        m = re.search(r"^## " + re.escape(key) + r"[^\n]*$", t, flags=re.M)
        if not m: print("NON TROVATO:", fname, key); continue
        nxt = re.search(r"^## ", t[m.end():], flags=re.M)
        pos = m.end() + nxt.start() if nxt else len(t)
        t = t[:pos].rstrip("\n") + "\n\n" + marker + "\n" + text.strip("\n") + "\n\n" + t[pos:]
        files[fname] = t; n += 1
    for f, t in files.items(): (VOL / f).write_text(t, encoding="utf-8")
    print("sezioni aggiunte:", n)
if __name__ == "__main__": main()
