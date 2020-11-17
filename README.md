<!-- Formatiert mit https://jsonformatter.org/markdown-formatter -->
# CTW 1.0.0

**CSV to wav**

_Das Projekt benutzt semantische Versionierung_

Eine Commandline Utility um beliebige `.csv` Dateien in stark anpassbare `.wav` Audio Dateien umzuwandeln.

##  Inhaltsverzeichniss

- [CTW 1.0.0](#ctw-100)
    - [Inhaltsverzeichniss](#inhaltsverzeichniss)
    - [Installation](#installation)
        - [Binary](#binary)
        - [Python Workspace](#python-workspace)
            - [makefile](#makefile)
            - [Manuell](#manuell)
            - [Ausführen](#ausführen)
    - [Argumente](#argumente)
        - [Positionsabhängige](#positionsabhängige)
        - [Optionale](#optionale)
            - [CSV parser](#csv-parser)
            - [wav Optionen](#wav-optionen)
            - [Programm Optionen](#programm-optionen)

## Installation

### Binary

Unter dem `Releases` Tab auf Github die neuste binary runterladen.
Einfach, jedoch nicht sehr flexibel und nich für GNU Linux zur verfügung.

### Python Workspace

Das Programm benutzt Python 3.9.
Diese Version (und pip) muss vorhanden sein.

#### makefile

`make init`

Das setzt vorraus dass Python 3.9 auf dem path unter dem Namen `python3` zur verfügung steht.
Außerdem, setzt der makefile bash oder zsh o.ä. vorraus um das virtuelle Enviornment zu aktivieren.

---

#### Manuell

1. Virtuelles Envriornment erstellen (optional)
   - `python3 -m venv ./venv`
   - `source "./venv/bin/activate"`
2. pip upgraden und dependencies installieren
   - `pip install --upgrade pip`
   - `pip install -r requirements.txt`

---

#### Ausführen

`python3 ctw.py`

oder

`./ctw.py`

(Bei letzterem Rechte nicht vergessen mit `chmod u+x ctw.py`)

---

## Argumente

Aufbau:

`./ctw.py [OPTIONEN] infile outfile`

### Positionsabhängige

| Name      | Beschreibung                    | Notizen                                                                                |
| --------- | :------------------------------ | :------------------------------------------------------------------------------------- |
| `infile`  | Pfad und Datei der Eingabedatei |                                                                                        |
| `outfile` | Pfad und Datei der Ausgabedatei | Die Datei wird ersetellt und überschreibt bereits existierende Dateien ohne zu fragen! |

### Optionale

#### CSV parser

| Kurz   | Argument      | Beschreibung               | Standard | Notizen                                                                                            |
| ------ | ------------- | :------------------------- | -------- | :------------------------------------------------------------------------------------------------- |
| `-sep` | `--seperator` | CSV Wert Seperator         | `;`      |                                                                                                    |
| `-dec` | `--decimal`   | Kommastellen Zeichen       | `.`      |                                                                                                    |
| `-x`   | `--x-axis`    | CSV Headername der X-Achse | `None`   | Bei `None` wird die erste Spalte automatisch als X-Achse interpretiert.                            |
|        | `--gen-x`     | X-Achse generieren         |          | Jedes Sample wird eine Sekunde zugeordnet. Die Option ist nicht mit `-x` gleichzeitig zu benutzen. |

#### wav Optionen

| Kurz   | Argument            | Beschreibung           | Standard | Notizen                                                                                        |
| ------ | ------------------- | :--------------------- | -------- | :--------------------------------------------------------------------------------------------- |
| `-bps` | `--bits-per-sample` | Bits pro Sample        | `16`     | Mögliche Optionen: `u8`, `16`, `32`, `32f`                                                     |
| `-sr`  | `--samplerate`      | Abtastrate in Hz       | `44100`  | Nur Ganzzahlige Werte                                                                          |
|        | `--bias`            | DC-Offset              | `0.0`    |                                                                                                |
| `-c`   | `--clipping`        | Clipping Methode       | `hard`   | Mögliche Optionen: `hard`, `soft`                                                              |
| `-i`   | `--interpolation`   | Interpolations Methode | `linear` | Mögliche Optionen: `nearest`, `linear`, `quadratic`, `cubic`                                   |
|        | `--multichanel`     | Mono/Mehr Kanäle       |          | Wenn gesetzt werden mehr kanalige (bis 64) wav Dateien erstellt, sonst Mono Dateien pro Spalte |

#### Programm Optionen

| Kurz | Argument      | Beschreibung                         | Standard | Notizen                                    |
| ---- | ------------- | :----------------------------------- | -------- | :----------------------------------------- |
| `-l` | `--log-level` | Ausgabe Level                        | `info`   | Mögliche Optionen: `none`, `info`, `debug` |
| `-p` | `--plugin`    | Pfad und Datei eines Python Packages | `None`   |                                            |

---
