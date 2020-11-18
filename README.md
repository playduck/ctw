<!-- Formatiert mit https://jsonformatter.org/markdown-formatter -->
# CTW 0.1.0-alpha

**CSV to wav**

_Das Projekt benutzt [Semantic Versioning](https://semver.org)_

Eine Commandline Utility um beliebige `.csv` Dateien in stark anpassbare `.wav` Audio Dateien umzuwandeln.

##  Inhaltsverzeichiss

- [CTW 0.1.0-alpha](#ctw-010-alpha)
    - [Inhaltsverzeichiss](#inhaltsverzeichiss)
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
    - [Beispiele](#beispiele)
    - [Zukunft](#zukunft)

## Installation

### Binary

Unter dem `Releases` Tab auf Github die neuste binary runterladen.
Einfach, jedoch nicht sehr flexibel und nicht für GNU Linux zur verfügung.

**Momentan auch nicht für Windows verfügbar.**
Die `pyinstaller` binary hat noch irgendwelche Probleme.
In Zukunft soll die binary auch auf Windows funktionieren.
Für Windows wird die Manuelle Installation empfohlen.

### Python Workspace

Das Programm benutzt Python 3.9. (frühere Versionen von Python 3 werden wahrscheinlich auch funktionieren.)

#### makefile

`make init`

Das setzt vorraus dass Python 3.9 auf dem path unter dem Namen `python3` zur verfügung steht.
Außerdem, setzt der makefile bash oder zsh o.ä. vorraus um das virtuelle Environment zu aktivieren.

---

#### Manuell

1. Repository klonen
   - `git clone https://github.com/playduck/ctw.git`
2. Virtuelles Environment erstellen (optional, empfohlen)
   - `python3 -m venv ./venv`
   - Der command um das venv zu aktivieren ist von Shell zu Shell anders:
        - bash/zsh: `source ./venv/bin/activate`
        - cmd.exe: `.\venv\Scripts\activate.bat`
        - powershell: `.\venv\Scripts\Activate.ps1`
        - mehr Infos zu anderen Shells [hier](https://docs.python.org/3/library/venv.html)
3. pip upgraden und dependencies installieren
   - (optional) `pip install --upgrade pip`
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
| `outfile` | Pfad und Datei der Ausgabedatei | Die Datei wird erstellt und überschreibt bereits existierende Dateien ohne zu fragen! |

### Optionale

#### CSV parser

| Kurz   | Argument      | Beschreibung               | Standard | Notizen                                                                                            |
| ------ | ------------- | :------------------------- | -------- | :------------------------------------------------------------------------------------------------- |
| `-sep` | `--seperator` | CSV Wert Separator         | `;`      |                                                                                                    |
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

## Beispiele

Beispieldateien stehen und `./test/data/` zur verfügung.

Minimum working example:
```bash
./ctw.py ./test/data/data0.csv ./out0.wav
```

Mit Interpolation, soft clipping (und impliziert generierter X-Achse):
```bash
./ctw.py -i quadratic -c soft ./test/data/data1.csv ./out1.wav
```

Mit template plugin und anderem csv Format:
```bash
./ctw.py -p ./test/plugin_template -x "time" -sep "|" -dec "," ./test/data/data2.csv ./out2.wav
```

---

## Zukunft

Weitere Dokumentation und Features folgen.
In [TODO.md](./TODO.md) befindet sich eine Liste an möglichen änderungen etc.

---

Robin Prillwitz 2020
