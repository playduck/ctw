<!-- Formatiert mit https://jsonformatter.org/markdown-formatter -->

# CTW 0.2.0-alpha

**CSV to wav**

_Das Projekt benutzt [Semantic Versioning](https://semver.org)_

Eine Commandline Utility um beliebige `.csv` Dateien in stark anpassbare `.wav` Audio Dateien umzuwandeln.

## Inhaltsverzeichnis

- [CTW 0.2.0-alpha](#ctw-020-alpha)
   - [Inhaltsverzeichnis](#inhaltsverzeichnis)
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
   - [Plugins](#plugins)
   - [Interne Funktionsweise](#interne-funktionsweise)
      - [CSV Parsing](#csv-parsing)
      - [Data Handling](#data-handling)
   - [Zukunft](#zukunft)

## Installation

### Binary

Unter dem [`Releases`](https://github.com/playduck/ctw/releases) Tab auf Github die neuste binary runterladen.
Einfach, jedoch nicht sehr flexibel und nicht für GNU Linux zur verfügung.

### Python Workspace

Das Programm benutzt Python 3.9. (frühere Versionen von Python 3 werden wahrscheinlich auch funktionieren.)

#### makefile

`make init`

Das setzt voraus dass Python 3.9 auf dem path unter dem Namen `python3` zur Verfügung steht.
Außerdem, setzt der makefile bash oder zsh o.ä. voraus um das virtuelle Environment zu aktivieren.

---

#### Manuell

```bash
$ git clone https://github.com/playduck/ctw.git
$ python3 -m venv ./venv # virtual env (optional but recommended)
```
```bash
# activate venv, depends on shell
$ source ./venv/bin/activate # bash/zsh
$ venv\Scripts\activate.bat # batch
$ venv\Scripts\Activate.ps1 #ps1
```
Mehr Infos zu anderen Shells [hier](https://docs.python.org/3/library/venv.html)
```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt

$ python ctw.py
```

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

| Name      | Beschreibung                    | Notizen                                                                               |
| --------- | :------------------------------ | :------------------------------------------------------------------------------------ |
| `infile`  | Pfad und Datei der Eingabedatei |                                                                                       |
| `outfile` | Pfad und Datei der Ausgabedatei | Die Datei wird erstellt und überschreibt bereits existierende Dateien ohne zu fragen! |

### Optionale

#### CSV parser

| Kurz   | Argument      | Beschreibung               | Standard | Notizen                                                                                            |
| ------ | ------------- | :------------------------- | -------- | :------------------------------------------------------------------------------------------------- |
| `-sep` | `--seperator` | CSV Wert Separator         | `;`      |                                                                                                    |
| `-dec` | `--decimal`   | Kommastellen Zeichen       | `.`      |                                                                                                    |
| `-x`   | `--x-axis`    | CSV Headername der x-Achse | `None`   | Bei `None` wird die erste Spalte automatisch als x-Achse interpretiert.                            |
|        | `--gen-x`     | x-Achse generieren         |          | Jedes Sample wird eine Sekunde zugeordnet. Die Option ist nicht mit `-x` gleichzeitig zu benutzen. |

#### wav Optionen

| Kurz   | Argument            | Beschreibung           | Standard | Notizen                                                                                            |
| ------ | ------------------- | :--------------------- | -------- | :------------------------------------------------------------------------------------------------- |
| `-bps` | `--bits-per-sample` | Bits pro Sample        | `16`     | Mögliche Optionen: `u8`, `16`, `32`, `32f`                                                         |
| `-sr`  | `--samplerate`      | Abtastrate in Hz       | `44100`  | Nur Ganzzahlige Werte                                                                              |
| `-m`   | `--max`             | Maximal Wert der Daten | `None`   | Bei `None` werden die Daten durch den größten gefundenen Wert geteilt, sonst durch den angegebenen |
|        | `--bias`            | DC-Offset              | `0.0`    |                                                                                                    |
| `-c`   | `--clipping`        | Clipping Methode       | `hard`   | Mögliche Optionen: `hard`, `soft`                                                                  |
| `-i`   | `--interpolation`   | Interpolationsmethode  | `linear` | Mögliche Optionen: `nearest`, `linear`, `quadratic`, `cubic`                                       |
|        | `--multichannel`    | Mono/Mehr Kanäle       |          | Wenn gesetzt werden mehr kanalige (bis 64) wav Dateien erstellt, sonst Mono Dateien pro Spalte     |

#### Programm Optionen

| Kurz | Argument      | Beschreibung                         | Standard | Notizen                                    |
| ---- | ------------- | :----------------------------------- | -------- | :----------------------------------------- |
| `-l` | `--log-level` | Ausgabe Level                        | `info`   | Mögliche Optionen: `none`, `info`, `debug` |
| `-p` | `--plugin`    | Pfad und Datei eines Python Packages | `None`   | Mehrere `-p` Flags sind möglich            |

---

## Beispiele

Beispieldateien stehen unter `./test/data/` zur Verfügung.

Minimum working example:

```bash
./ctw.py ./test/data/data0.csv ./out0.wav
```

Werte als Prozentualer Wert (zwischen -100% und 100%):

```bash
./ctw.py -m 100 ./test/data/data0.csv ./out0.wav
```

Mit Interpolation, soft clipping und generierter x-Achse:

```bash
./ctw.py -i quadratic -c soft --gen-x ./test/data/data1.csv ./out1.wav
```

Mit `template_plugin` und anderem csv Format:

```bash
./ctw.py -p ./test/plugin_template -x "time" -sep "|" -dec "," ./test/data/data2.csv ./out2.wav
```

---

## Plugins

**Momentan sind Plugins nur im interaktiven Modus (keine binary) ausführbar.**

Plugins sind python skripte, die vom Nutzer angegeben werden und die internen Daten während der Ausführung modifizieren können.
Damit können beispielsweise eigene Algorithmen implementiert werden oder die Daten einfach genauer beobachtet werden.

Ein [Beispiel Plugin](./test/plugin_template/__init__.py) steht zur Verfügung.
Die Funktionssignaturen können sich während des Development verändern.
Zu beachten ist, dass importierte Pakete sowohl für ctw.py als auch für das Plugin zur Verfügung stehen.
(Ergo: Entweder Pakete global installieren oder ctw und Plugin in gleichem venv ausführen.)

Mehrere Plugins könnnen gleichzeitig genutzt werden, indem mehrere `-p` flags benutzt werden.
Die Reihenfolge der Plugins ist von der Reihenfolge des Commands abhängig.

**Die Plugin Flag `-p` erwartet ein Python Modul.**
Daher muss der Name des Ordners ohne folgenden Slash angegeben werden.

| ✅ richtig                  | ❌ falsch                    |
| --------------------------- | ---------------------------- |
| `-p ./test/plugin_template` | `-p ./test/plugin_template/` |

Standardmäßig wird `__init__.py` aufgerufen und erwartet, dass die Funktionen global im Modul erreichbar sind.
Das Plugin kann wie jedes andere Python Modul mehrere Dateien und anderes besitzen.
Die erwarteten Funktionen sind:

- `init_hook`
- `read_hook`
- `modify_hook`
- `scale_hook`
- `save_hook`

Als Referenz für Übergabeparameter und erwartete Rückgabetypen siehe das [Beispiel Plugin](./test/plugin_template/__init__.py).

## Interne Funktionsweise

### CSV Parsing

CSV Dateien sollten in der ersten Zeile einen Header haben, welche die Spalten benannte.
Es sollte wenigstens eine Zeile existieren.
Der Delimiter/Seperator und Zehner-Stelle könnnen mit `-sep` und `-dec` respektiv angepasst werden.

Wird keine explizite x-Achse angegeben, wird die erste (Spalte ganz links) als x-Achse verwendet.

Existiert nur eine Spalte, wird ein x-Achse erstellt. Jedes Sample (Y-Wert) wird dann eine Sekunde gegeben.
Diese Option kann auch mit `--gen-x` explizit verwendet werden.

Wird mit `-x` eine x-Achse angegeben, wird diese verwendet.
Die x-Achse muss stetig monoton steigen.

Existieren mehr als drei Spalten (Zwei Spalten mit `--gen-x`), werden weitere Spalten als weitere "Signale" interpretiert.
Im Normalfall werden mehrere .wav Dateien (mit gleicher x-Achse) erstellt.
Ist die `--multichannel` flag gesetz wird versucht die weiteren Signale als weitere Kanäle in eine .wav einzubringen.

### Data Handling

1. Plugin init hook
2. CSV Parsing
3. Plugin read hook
4. Daten Manipulieren
   1. Validieren
      - Alle nvaliden Daten (NaN) werden auf 0 gesetzt
      - Die x-Achse muss streng monoton steigend sein
   2. Normalisieren (Wertemenge auf -1.0 bis 1.0)
      - Die Werte werden durch den mit `-m` angegebenen Wert geteilt, wird kein Wert angegeben, werden sie durch den größten Wert in der Datenmenge (ohne X-Ache) geteilt.
   3. Bias hinzufügen
   4. Interpolieren
      - benutzt die `scipy.interpolate.interp1d` Methode, alle Interpolationsargumente sind valide.
   5. Clipping
      - Daten, die durch die Modifikationen außerhalb des validen Bereichs gekommen sind, werden entweder hard oder soft geclipped. Soft-Clipping verzerrt das Signal, lässt aber mehr werte bestehen.
5. Plugin modify hook
6. Daten Skalieren (Auf angegebenen Datentyp und dessen Reichweite konvertieren)
7. Plugin scale hook
8. wav schreiben
9. Plugin save hook

## Zukunft

Weitere Dokumentation und Features folgen.
In [TODO.md](./TODO.md) befindet sich eine Liste an möglichen Änderungen etc.

---

Robin Prillwitz 2020
