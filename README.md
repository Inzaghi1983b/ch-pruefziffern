# ch-pruefziffern

Pruefziffern fuer Schweizer Kennnummern (IBAN CH/LI, UID). Coding-Agenten setzen Issues autonom um; ein Mensch prueft und merged.
Konventionen: `ai-projects/KONVENTIONEN.md`.

## Ablauf

1. Issue schreiben und Label `agent` setzen.
2. GitHub Agentic Workflows startet den Coding-Agenten (Anbieter: `.github/workflows/shared/anbieter.md`)
   mit Leserechten, Netzwerk-Allowlist und API-Key nur im Proxy.
3. Der Agent setzt das Issue um und fuehrt `ruff` und `pytest` aus (Regeln in `AGENTS.md`).
4. Ein Pruefjob kontrolliert das Ergebnis, danach entsteht ein Draft-Pull-Request.
5. CI (`.github/workflows/ci.yml`) wartet auf den Freigabeklick ("Approve and run") und liefert
   den Pflicht-Check `test`.
6. Ein Mensch prueft, setzt "Ready for review" und merged. Kein automatischer Merge.

## Kostenbremsen

Agent hoechstens 50 AI-Credits (rund 0.50 USD) pro Lauf, Pruefjob 20, alle Laeufe zusammen 200 pro
24 Stunden, hoechstens 30 Minuten. Harte Grenze: Prepaid-Guthaben beim Anbieter.

## Entwicklung lokal

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\ruff check .
.venv\Scripts\pytest
```

## Paralleltest 2026-10-16 (belegt)

Zwei Agenten (Codex + DeepSeek Flash) setzten zwei Issues gleichzeitig um. Beide Labels `agent`
wurden um 17:12:05 UTC gesetzt.

| | IBAN (#1 -> PR #4) | UID (#2 -> PR #3) |
|---|---|---|
| Lauf | 38937844737, 5 min 04 s | 38937845503, 4 min 41 s |
| Agent-Job | 17:13:19-17:15:22 | 17:12:52-17:14:44 |
| Codex-Ausfuehrung | 17:14:04-17:15:08 | 17:13:30-17:14:34 |
| Agent: Anfragen, Eingabe (Cache), Ausgabe | 11, 257 883 (253 312), 6 003 | 12, 291 897 (280 960), 5 879 |
| Pruefjob: Eingabe (Cache), Ausgabe | 70 532 (54 656), 617 | 117 939 (100 864), 1 546 |
| AI-Credits (Agent + Pruefjob) | 1.01 + 0.58 = 1.59 | 1.20 + 0.76 = 1.96 |
| Kosten zum DeepSeek-Preis ausserhalb der Spitzenzeit | rund 0.008 USD | rund 0.010 USD |

- **Ueberlappung:** Agent-Jobs 85 s gleichzeitig, Codex-Ausfuehrung 30 s, Modellantworten 4 s.
  Den Agent-Job serialisiert keine Concurrency-Gruppe; gesperrt wird nur pro Issue und beim kurzen
  Abschluss-Job.
- **Isolation:** zwei Branches mit je einem Bot-Commit auf demselben `main`-Stand, keine gemeinsame
  Datei.
- **Integration:** `git merge-tree` beider PR-Koepfe konfliktfrei; im kombinierten Stand ruff und
  alle Tests gruen. Danach regulaer gemergt, CI auf `main` gruen.
- **Qualitaet:** Ein unabhaengiger Abgleich (360 000 IBAN- und 1 Mio. UID-Faelle) fand keine
  Abweichung. Im Review gefunden und korrigiert: Ein `ss`-Ligaturzeichen (`ß`) wurde durch
  `upper()` zu `SS` und galt in der IBAN als gueltig; Nicht-ASCII ist jetzt ungueltig.
- **Manuell:** zwei CI-Freigaben (per API durch den Repo-Admin) und die Merges.
- **Offen:** Abgleich der Kosten mit der DeepSeek-Abrechnung. Die AI-Credits rechnet gh-aw mit dem
  Spitzenpreis aus dem Frontmatter; die USD-Werte oben sind die Tokens x Listenpreis zur Laufzeit.
