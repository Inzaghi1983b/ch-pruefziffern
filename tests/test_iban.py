import pytest

from pruefziffern.iban import formatiere_iban, ist_gueltige_iban

GUELTIGE_IBANS = [
    "CH9300762011623852957",
    "CH93 0076 2011 6238 5295 7",
    "CH56 0483 5012 3456 7800 9",
    "LI21088100002324013AA",
    "li21 0881 0000 2324 013a a",
]

UNGULTIGE_IBANS = [
    "CH9300762011623852958",  # falsche Pruefziffer
    "CH5604835012345678008",  # falsche Pruefziffer
    "CH930076201162385295",  # zu kurz
    "CH93007620116238529578",  # zu lang
    "",  # leer
    "   ",  # nur Leerzeichen
    "DE89370400440532013000",  # anderes Land, Pruefziffer selbst korrekt
    "CH93007620116238529-7",  # unerlaubtes Zeichen
    "CH93007620 116238529A7",  # Buchstabe statt Ziffer im Institut
    "XX9300762011623852957",  # unbekannter Laendercode
]


@pytest.mark.parametrize("iban", GUELTIGE_IBANS)
def test_ist_gueltige_iban_erkennt_gueltige_ibans(iban: str) -> None:
    assert ist_gueltige_iban(iban) is True


@pytest.mark.parametrize("iban", UNGULTIGE_IBANS)
def test_ist_gueltige_iban_erkennt_ungueltige_ibans(iban: str) -> None:
    assert ist_gueltige_iban(iban) is False


@pytest.mark.parametrize("iban", [None, 1234567890, ["CH9300762011623852957"]])
def test_ist_gueltige_iban_wirft_bei_falschem_typ_keine_ausnahme(iban: object) -> None:
    assert ist_gueltige_iban(iban) is False  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("iban", "erwartet"),
    [
        ("CH9300762011623852957", "CH93 0076 2011 6238 5295 7"),
        ("ch93 0076 2011 6238 5295 7", "CH93 0076 2011 6238 5295 7"),
        ("CH9300762011623852957", "CH93 0076 2011 6238 5295 7"),
        ("LI21088100002324013AA", "LI21 0881 0000 2324 013A A"),
        ("li21088100002324013aa", "LI21 0881 0000 2324 013A A"),
        ("CH56 0483 5012 3456 7800 9", "CH56 0483 5012 3456 7800 9"),
    ],
)
def test_formatiere_iban_gibt_standardschreibweise(iban: str, erwartet: str) -> None:
    assert formatiere_iban(iban) == erwartet


@pytest.mark.parametrize("iban", UNGULTIGE_IBANS)
def test_formatiere_iban_wirft_bei_ungueltiger_iban(iban: str) -> None:
    with pytest.raises(ValueError):
        formatiere_iban(iban)


@pytest.mark.parametrize("iban", [None, 1234567890])
def test_formatiere_iban_wirft_bei_falschem_typ(iban: object) -> None:
    with pytest.raises(ValueError):
        formatiere_iban(iban)  # type: ignore[arg-type]
