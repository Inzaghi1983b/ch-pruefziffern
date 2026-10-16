import pytest

from pruefziffern.uid import formatiere_uid, ist_gueltige_uid

GUELTIGE_UIDS = [
    "CHE-100.155.212",
    "che100155212",
    "CHE-100.000.070",
]

UNGUELTIGE_UIDS = [
    "CHE-100.155.213",
    "CHE-100.000.160",
    "CHE-100.155.21",
    "CHE-100.155.2120",
    "CHE1001552121",
    "CHF-100.155.212",
    "CHE-100.155.212 MWST",
    "CHE-100.155.212 HR",
    "",
    "   ",
    "CHE",
    "CHE-100.155.21A",
]


@pytest.mark.parametrize("text", GUELTIGE_UIDS)
def test_ist_gueltige_uid_akzeptiert_gueltige_nummern(text):
    assert ist_gueltige_uid(text) is True


@pytest.mark.parametrize("text", UNGUELTIGE_UIDS)
def test_ist_gueltige_uid_lehnt_ungueltige_nummern_ab(text):
    assert ist_gueltige_uid(text) is False


def test_ist_gueltige_uid_ignoriert_leerzeichen_und_grossschreibung():
    assert ist_gueltige_uid(" che 100 155 212 ") is True


def test_ist_gueltige_uid_wirft_bei_fremdem_typ_keine_ausnahme():
    assert ist_gueltige_uid(None) is False
    assert ist_gueltige_uid(100155212) is False


@pytest.mark.parametrize(
    ("text", "erwartet"),
    [
        ("CHE-100.155.212", "CHE-100.155.212"),
        ("che100155212", "CHE-100.155.212"),
        ("che 100 155 212", "CHE-100.155.212"),
        ("CHE-100.000.070", "CHE-100.000.070"),
    ],
)
def test_formatiere_uid_standard(text, erwartet):
    assert formatiere_uid(text) == erwartet


@pytest.mark.parametrize("text", UNGUELTIGE_UIDS)
def test_formatiere_uid_wirft_valueerror(text):
    with pytest.raises(ValueError):
        formatiere_uid(text)
