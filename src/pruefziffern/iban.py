"""IBAN-Pruefung fuer die Schweiz (CH) und Liechtenstein (LI).

Quelle der Pruefziffer-Regel: ISO 13616 (IBAN). Die ersten vier Zeichen der IBAN
werden ans Ende gestellt, Buchstaben durch Zahlen ersetzt (A=10 bis Z=35) und die
Pruefsumme modulo 97 gebildet; der Rest muss 1 sein.

Laengen und Aufbau: eine CH-/LI-IBAN hat ohne Trennzeichen genau 21 Zeichen,
naemlich 2 Buchstaben (Land), 2 Ziffern (Pruefziffern), 5 Ziffern (Institut) und
12 Ziffern oder Grossbuchstaben (Konto).
"""

from __future__ import annotations

__all__ = ["formatiere_iban", "ist_gueltige_iban"]

_LAENDER = ("CH", "LI")
_BANKKONTO_LAENGE = 12
_IBAN_LAENGE = 21


def _ist_ziffer(zeichen: str) -> bool:
    """True, wenn das Zeichen eine ASCII-Ziffer ist."""
    return "0" <= zeichen <= "9"


def _ist_ziffer_oder_grossbuchstabe(zeichen: str) -> bool:
    """True, wenn das Zeichen eine ASCII-Ziffer oder ein ASCII-Grossbuchstabe ist."""
    return _ist_ziffer(zeichen) or "A" <= zeichen <= "Z"


def _normalisiere(text: object) -> str | None:
    """Leerzeichen entfernen und in Grossbuchstaben umwandeln, sonst None."""
    if not isinstance(text, str):
        return None
    return text.replace(" ", "").upper()


def _pruefe_aufbau(normalisiert: str) -> bool:
    """Prueft Laenge, Laendercode und Zeichenklassen der normalisierten IBAN."""
    if len(normalisiert) != _IBAN_LAENGE:
        return False
    if normalisiert[:2] not in _LAENDER:
        return False
    if not all(_ist_ziffer(zeichen) for zeichen in normalisiert[2:9]):
        return False
    return all(
        _ist_ziffer_oder_grossbuchstabe(zeichen) for zeichen in normalisiert[-_BANKKONTO_LAENGE:]
    )


def _pruefsumme_ist_eins(normalisiert: str) -> bool:
    """Bildet die Modulo-97-Pruefsumme nach ISO 13616."""
    umgestellt = normalisiert[4:] + normalisiert[:4]
    ziffern = "".join(
        zeichen if _ist_ziffer(zeichen) else str(ord(zeichen) - ord("A") + 10)
        for zeichen in umgestellt
    )
    return int(ziffern) % 97 == 1


def ist_gueltige_iban(text: str) -> bool:
    """Prueft, ob ``text`` eine gueltige IBAN aus CH oder LI ist.

    Leerzeichen werden ignoriert, Gross-/Kleinschreibung spielt keine Rolle.
    Jedes andere Zeichen macht die IBAN ungueltig. Bei ungueltiger Eingabe wird
    ``False`` zurueckgegeben, es wird keine Ausnahme ausgeloest.
    """
    normalisiert = _normalisiere(text)
    if normalisiert is None:
        return False
    return _pruefe_aufbau(normalisiert) and _pruefsumme_ist_eins(normalisiert)


def formatiere_iban(text: str) -> str:
    """Gibt die IBAN in Grossbuchstaben als Vierergruppen mit Leerzeichen zurueck.

    Beispiel: ``CH93 0076 2011 6238 5295 7``. Leerzeichen in der Eingabe und
    Gross-/Kleinschreibung werden ignoriert. Bei ungueltiger Eingabe wird
    ``ValueError`` ausgeloest.
    """
    normalisiert = _normalisiere(text)
    if normalisiert is None or not (
        _pruefe_aufbau(normalisiert) and _pruefsumme_ist_eins(normalisiert)
    ):
        raise ValueError(f"Ungueltige IBAN: {text!r}")
    return " ".join(normalisiert[i : i + 4] for i in range(0, len(normalisiert), 4))
