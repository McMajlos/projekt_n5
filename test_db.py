import pytest
import mysql.connector
from main import (
    pridat_ukol,
    aktualizovat_ukol,
    odstranit_ukol,
    zobrazit_ukoly,
    zobrazit_vsechny_ukoly,
)


@pytest.fixture(scope="function")
def db_setup():
    """
    Fixture pro připojení k databázi a nastavení testovacího prostředí.
    """
    # Připojení k databázi
    conn = mysql.connector.connect(
        host="localhost", user="root", password="engeto", database="engeto_test"
    )
    cursor = conn.cursor()

    # Vytvořeni testovaci tabulky
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(50),
            popis VARCHAR(500),
            stav VARCHAR(100) DEFAULT 'Nezahájeno',
            datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()

    # Předání připojení a kurzoru testům
    yield conn, cursor

    # Úklid po testech: Smazání tabulky
    cursor.execute("DROP TABLE IF EXISTS ukoly")
    conn.commit()

    # Uzavření připojení
    cursor.close()
    conn.close()


def test_pridat_ukol(db_setup):
    # Přidání úkolu do databáze
    conn, cursor = db_setup
    pridat_ukol(conn, nazev_ukolu="Ukol1", popis_ukolu="Popis1")
    cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Ukol1'")
    result = cursor.fetchone()
    assert result is not None, "Záznam nebyl vložen do tabulky."
    assert result[1] == "Ukol1", "Název úkolu není správný."
    assert result[2] == "Popis1", "Popis úkolu není správný."


def test_pridat_prazdny_nazev_ukol(db_setup):
    # Přidání úkolu s prázdným názvem
    conn, cursor = db_setup
    pridat_ukol(conn, nazev_ukolu="", popis_ukolu="Popis1")
    cursor.execute("SELECT COUNT(*) FROM ukoly")
    count = cursor.fetchone()[0]
    assert count == 0, "Tabulka by měla být prázdná."


def test_pridat_ukol_s_dlouhym_nazvem(db_setup):
    # Přidání úkolu s dlouhým názvem
    conn, cursor = db_setup
    with pytest.raises(ValueError, match="Název úkolu je příliš dlouhý"):
        pridat_ukol(conn, nazev_ukolu="x" * 51, popis_ukolu="Popis1")


def test_zobrazit_probihajici_ukoly(db_setup):
    conn, cursor = db_setup
    # Přidání úkolů
    for i in range(0, 5):
        pridat_ukol(conn, nazev_ukolu=f"Ukol{i}", popis_ukolu=f"Popis{i}")

    aktualizovat_ukol(conn, id_ukolu=1, novy_stav="Probíhá")
    # Zobrazení úkolů se stavem "Probíhá"
    cursor.execute("SELECT * FROM ukoly where stav = 'Probíhá'")
    ukoly = cursor.fetchall()
    assert len(ukoly) == 1, "Nesprávný počet úkolů."
    # Zobrazení všech úkolů
    cursor.execute("SELECT * FROM ukoly")
    vsechny_ukoly = cursor.fetchall()
    assert len(vsechny_ukoly) == 5, "Nesprávný počet úkolů."
    # Zobrazení úkolů, které nejsou "Probíhá"
    cursor.execute("SELECT * FROM ukoly WHERE stav != 'Probíhá'")
    ukoly_neprobihaji = cursor.fetchall()
    assert len(ukoly_neprobihaji) == 4, "Nesprávný počet úkolů."


def test_zobrazit_vsechny_ukoly_prazdna_tabulka(db_setup):
    conn, cursor = db_setup
    # Zobrazení úkolů v prázdné tabulce
    with pytest.raises(
        ValueError, match="Žádné úkoly nebyly nalezeny. Databáze je prázdná!"
    ):
        zobrazit_vsechny_ukoly(conn)


def test_aktualizovat_ukol(db_setup):
    conn, cursor = db_setup
    # Přidání úkolu pro aktualizaci
    pridat_ukol(conn, nazev_ukolu="Ukol1", popis_ukolu="Popis1")
    # Aktualizace úkolu
    aktualizovat_ukol(conn, id_ukolu=1, novy_stav="Probíhá")
    # Ověření aktualizace
    cursor.execute("SELECT * FROM ukoly WHERE id = 1")
    result = cursor.fetchone()
    assert result[3] == "Probíhá", "Stav úkolu nebyl aktualizován správně."
    assert result[1] == "Ukol1", "Název úkolu nebyl správně zachován."
    assert result[2] == "Popis1", "Popis úkolu nebyl správně zachován."
    assert result[4] is not None, "Datum vytvoření úkolu by mělo být nastaveno."


def test_aktualizovat_neexistujici_ukol(db_setup):
    conn, cursor = db_setup
    # Pokus o aktualizaci neexistujícího úkolu
    with pytest.raises(ValueError, match="Úkol s ID 999 neexistuje"):
        aktualizovat_ukol(conn, id_ukolu=999, novy_stav="Dokončeno")


def test_odstranit_ukol(db_setup):
    conn, cursor = db_setup
    # Přidání úkolu pro odstranění
    pridat_ukol(conn, nazev_ukolu="Ukol1", popis_ukolu="Popis1")
    # Odstranění úkolu
    odstranit_ukol(conn, id_ukolu=1)
    # Ověření odstranění
    cursor.execute("SELECT COUNT(*) FROM ukoly WHERE id = 1")
    count = cursor.fetchone()[0]
    assert count == 0, "Úkol nebyl odstraněn."
    # Ověření, že tabulka je prázdná
    cursor.execute("SELECT COUNT(*) FROM ukoly")
    count = cursor.fetchone()[0]


def test_odstranit_neexistujici_ukol(db_setup):
    conn, cursor = db_setup
    # Pokus o odstranění neexistujícího úkolu
    with pytest.raises(ValueError, match="Úkol s ID 999 neexistuje"):
        odstranit_ukol(conn, id_ukolu=999)
