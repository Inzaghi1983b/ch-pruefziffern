"""UID (Unternehmens-Identifikationsnummer) pruefen und formatieren.

Regel: Eine UID besteht aus dem Praefix ``CHE`` und 9 Ziffern. Die neunte Ziffer ist die
Pruefziffer. Die ersten 8 Ziffern werden mit den Gewichten 5, 4, 3, 2, 7, 6, 5, 4
multipliziert, die Summe S gebildet und die Pruefziffer als ``(11 - S) mod 11`` berechnet.
Ergibt sich 10 als Pruefziffer, ist die Nummer ungueltig.

Quellen: eCH-0097 (UID), CH Core UIDB-Identifier.
"""

from __future__ import annotations

_PRAEFIX = "CHE"
_GEWICHTE = (5, 4, 3, 2, 7, 6, 5, 4)
_TRENNZEICHEN = "-."


def _ziffern(text: str) -> str | None:
    """Liefert die 9 Ziffern der UID oder ``None``, wenn die Eingabe nicht der Form entspricht."""
    if not isinstance(text, str):
        return None
    normalisiert = "".join(
        zeichen for zeichen in text if not zeichen.isspace() and zeichen not in _TRENNZEICHEN
    ).upper()
    if len(normalisiert) != len(_PRAEFIX) + 9 or not normalisiert.startswith(_PRAEFIX):
        return None
    ziffern = normalisiert[len(_PRAEFIX) :]
    if not (ziffern.isascii() and ziffern.isdigit()):
        return None
    return ziffern


def _pruefziffer_stimmt(ziffern: str) -> bool:
    """Prueft die neunte Ziffer gegen die aus den ersten 8 Ziffern berechnete Pruefziffer."""
    summe = sum(
        int(ziffer) * gewicht for ziffer, gewicht in zip(ziffern[:8], _GEWICHTE, strict=True)
    )
    pruefziffer = (11 - summe) % 11
    return pruefziffer != 10 and pruefziffer == int(ziffern[8])


def ist_gueltige_uid(text: str) -> bool:
    """Prueft, ob ``text`` eine gueltige UID ist.

    Bindestriche, Punkte und Leerzeichen werden ignoriert, Gross-/Kleinschreibung ist egal.
    Zusaetze wie ``MWST`` oder ``HR`` machen die Eingabe ungueltig. Die Funktion wirft bei
    ungueltiger Eingabe keine Ausnahme, sondern gibt ``False`` zurueck.
    """
    ziffern = _ziffern(text)
    return ziffern is not None and _pruefziffer_stimmt(ziffern)


def formatiere_uid(text: str) -> str:
    """Gibt die UID in der Standardschreibweise ``CHE-123.456.789`` zurueck.

    Raises:
        ValueError: Wenn ``text`` keine gueltige UID ist.
    """
    ziffern = _ziffern(text)
    if ziffern is None or not _pruefziffer_stimmt(ziffern):
        raise ValueError(f"Ungueltige UID: {text!r}")
    return f"{_PRAEFIX}-{ziffern[:3]}.{ziffern[3:6]}.{ziffern[6:]}"
