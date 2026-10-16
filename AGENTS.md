# AGENTS.md - Regeln fuer jeden Coding-Agenten in diesem Repo

Diese Datei gilt unabhaengig vom Agenten (Codex, Claude Code oder andere) und vom Modell.

## Projekt

Kleine Python-Bibliothek, die Schweizer Kennnummern (zum Beispiel IBAN, UID) auf Format und
Pruefziffer prueft und einheitlich formatiert.

- Code: `src/pruefziffern/`, ein Modul pro Kennnummer (z. B. `iban.py`, `uid.py`)
- Tests: `tests/` (pytest), eine Testdatei pro Modul (z. B. `tests/test_iban.py`)
- Python 3.12, nur Standardbibliothek, keine Laufzeit-Abhaengigkeiten
- Datenklasse: oeffentlich-tauglich. Nur oeffentliche Beispielnummern oder selbst berechnete
  Testwerte verwenden.

## Fachregeln

- Eingaben sind `str`. Gross-/Kleinschreibung und die im Issue genannten Trennzeichen werden
  ignoriert.
- Pruef-Funktionen (`ist_gueltige_...`) geben `bool` zurueck und werfen bei ungueltiger Eingabe
  keine Ausnahme.
- Formatier-Funktionen (`formatiere_...`) geben die Standardschreibweise zurueck und loesen bei
  ungueltiger Eingabe `ValueError` aus.
- Die Pruefziffer-Regel steht mit Quelle im Docstring des Moduls.
- `src/pruefziffern/__init__.py` nicht aendern; Aufrufer importieren direkt aus dem Modul
  (`from pruefziffern.iban import ...`). So bleiben parallele Aufgaben in getrennten Dateien.
- Jede oeffentliche Funktion hat Typangaben und einen Docstring.

## Arbeitsablauf

1. Aufgabe aus dem Issue lesen. Unklarheit nicht raten: Annahme im Pull-Request-Text nennen.
2. Nur `src/` und `tests/` aendern. README nur, wenn die Aufgabe es verlangt.
3. Fuer jede neue Funktion Tests schreiben, inklusive Grenzfaelle aus dem Issue.
4. Vor dem Abschluss alle drei Pruefungen ausfuehren und gruen machen:
   - `ruff check .`
   - `ruff format --check .` (bei Bedarf vorher `ruff format .`)
   - `pytest`
5. Bleibt eine Pruefung nach drei Korrekturrunden rot: aufhoeren und den Fehler im
   Pull-Request-Text offen beschreiben, nicht Tests abschwaechen oder loeschen.

## Verboten

- Aenderungen an `.github/`, `AGENTS.md`, `pyproject.toml` oder `requirements-dev.txt`.
- Tests loeschen, ueberspringen oder Erwartungen aufweichen, damit sie gruen werden.
- Neue Abhaengigkeiten, Netzwerkzugriffe, Secrets oder Zugangsdaten im Code.
- Personen- oder Kundendaten, ausser die Datenklasse oben erlaubt sie ausdruecklich.
