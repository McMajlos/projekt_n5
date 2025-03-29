import mysql.connector


def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="engeto", database="engeto"
        )
        print("=" * 60)
        print("Připojení k databázi bylo úspěšné.")
        return conn
    except mysql.connector.Error as err:
        print(f"Chyba při připojování: {err}")


def vytvoreni_tabulky(conn):
    """Vytvoří tabulku 'ukoly', pokud ještě neexistuje."""
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'ukoly'")
        table_exists = cursor.fetchone()

        if table_exists:
            print("Tabulka 'ukoly' již existuje, není potřeba ji vytvářet.")
            print("=" * 60)
        else:
            cursor.execute(
                """
                CREATE TABLE ukoly (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nazev VARCHAR(50),
                    popis VARCHAR(500),
                    stav VARCHAR(100) DEFAULT 'Nezahájeno', 
                    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
            print("Tabulka 'ukoly' byla úspěšně vytvořena.")
            print("=" * 60)

    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}")


def pridat_ukol(conn, nazev_ukolu, popis_ukolu):
    """Přidá úkol do databáze s již zadanými hodnotami."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
            (nazev_ukolu, popis_ukolu),
        )
        conn.commit()
        print(f"Úkol '{nazev_ukolu}' byl přidán.")
    except mysql.connector.Error as err:
        print(f"Chyba při vkládání dat: {err}")


def zobrazit_ukoly(conn):
    """Zobrazí úkoly, které mají stav 'Nezahájeno' nebo 'Probíhá'."""
    print("")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ukoly WHERE stav = 'Nezahájeno' OR stav = 'Probíhá'"
        )
        vysledky = cursor.fetchall()

        if len(vysledky) == 0:
            print("Žádné úkoly nebyly nalezeny. Databáze je prázdná!")
            return

        data = []
        for radek in vysledky:
            idcko = str(radek[0])
            nazev = str(radek[1])
            popis = str(radek[2])
            stav = str(radek[3])
            datum = radek[4].strftime("%d.%m.%Y %H:%M:%S")
            data.append((idcko, nazev, popis, stav, datum))

        hlavicky = ("ID", "Název", "Popis", "Stav", "Vytvořeno")

        print("")
        print("Zobrazuji úkoly, které mají stav 'Nezahájeno' nebo 'Probíhá':")
        sirky = []
        for sloupec_index in range(len(hlavicky)):
            nejdelsi_delka = len(hlavicky[sloupec_index])
            for radek in data:
                delka_hodnoty = len(radek[sloupec_index])
                if delka_hodnoty > nejdelsi_delka:
                    nejdelsi_delka = delka_hodnoty
            sirky.append(nejdelsi_delka)

        hlavicka_radek = ""
        for nazev_sloupce_index in range(len(hlavicky)):
            hlavicka_radek += (
                hlavicky[nazev_sloupce_index].ljust(sirky[nazev_sloupce_index]) + " | "
            )
        print(hlavicka_radek.rstrip(" | "))

        oddelovac = ""
        for sirka_sloupce in sirky:
            oddelovac += "-" * sirka_sloupce + "-+-"
        oddelovac = oddelovac[:-3]
        print(oddelovac)

        for radek in data:
            radek_text = ""
            for hodnota_index in range(len(radek)):
                radek_text += radek[hodnota_index].ljust(sirky[hodnota_index]) + " | "
            print(radek_text.rstrip(" | "))

    except mysql.connector.Error as chyba:
        print("Chyba při načítání dat:", chyba)


def zobrazit_vsechny_ukoly(conn):
    """Zobrazí všechny úkoly v databázi. Používá se ve funkci aktualizovat_ukol(), odstranit_ukol()."""
    print("")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ukoly")
        vysledky = cursor.fetchall()

        if len(vysledky) == 0:
            print("Žádné úkoly nebyly nalezeny. Databáze je prázdná!")
            return

        data = []
        for radek in vysledky:
            idcko = str(radek[0])
            nazev = str(radek[1])
            popis = str(radek[2])
            stav = str(radek[3])
            datum = radek[4].strftime("%d.%m.%Y %H:%M:%S")
            data.append((idcko, nazev, popis, stav, datum))

        hlavicky = ("ID", "Název", "Popis", "Stav", "Vytvořeno")

        sirky = []
        for sloupec_index in range(len(hlavicky)):
            nejdelsi_delka = len(hlavicky[sloupec_index])
            for radek in data:
                delka_hodnoty = len(radek[sloupec_index])
                if delka_hodnoty > nejdelsi_delka:
                    nejdelsi_delka = delka_hodnoty
            sirky.append(nejdelsi_delka)

        hlavicka_radek = ""
        for nazev_sloupce_index in range(len(hlavicky)):
            hlavicka_radek += (
                hlavicky[nazev_sloupce_index].ljust(sirky[nazev_sloupce_index]) + " | "
            )
        print(hlavicka_radek.rstrip(" | "))

        oddelovac = ""
        for sirka_sloupce in sirky:
            oddelovac += "-" * sirka_sloupce + "-+-"
        oddelovac = oddelovac[:-3]
        print(oddelovac)

        for radek in data:
            radek_text = ""
            for hodnota_index in range(len(radek)):
                radek_text += radek[hodnota_index].ljust(sirky[hodnota_index]) + " | "
            print(radek_text.rstrip(" | "))

    except mysql.connector.Error as chyba:
        print("Chyba při načítání dat:", chyba)


def aktualizovat_ukol(conn, id_ukolu, novy_stav):
    """Aktualizuje stav úkolu v databázi na základě předaného ID a nového stavu."""
    try:
        cursor = conn.cursor()
        # Kontrola, zda úkol s daným ID existuje
        cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
        ukol = cursor.fetchone()
        if not ukol:
            print(f"Úkol s ID {id_ukolu} nebyl nalezen.")
            return

        cursor.execute(
            "UPDATE ukoly SET stav = %s WHERE id = %s",
            (novy_stav, id_ukolu),
        )
        conn.commit()
        print(f"Úkol s ID {id_ukolu} byl aktualizován na stav '{novy_stav}'.")
    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci úkolu: {err}")


def odstranit_ukol(conn, id_ukolu):
    """Odstraní úkol z databáze na základě ID."""
    try:
        cursor = conn.cursor()

        # Kontrola, jestli úkol s daným ID existuje
        cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
        ukol = cursor.fetchone()

        if not ukol:
            print(f"Úkol s ID {id_ukolu} nebyl nalezen.")
            return

        # Smazání úkolu
        cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
        conn.commit()
        print(f"Úkol s ID {id_ukolu} byl úspěšně odstraněn.")

    except mysql.connector.Error as err:
        print(f"Chyba při odstraňování úkolu: {err}")


def hlavni_menu(conn):
    """Hlavní menu programu."""
    global task_run
    print("")
    print("Správce úkolů - Hlavní menu")
    print("1. Přidat nový úkol")
    print("2. Zobrazit úkoly")
    print("3. Aktualizovat úkol")
    print("4. Odstranit úkol")
    print("5. Konec programu")
    user_choice = input("Vyberte možnost 1-5: ")

    try:
        user_choice_int = int(user_choice)
        if 1 <= user_choice_int <= 5:
            if user_choice_int == 1:
                nazev = input("Zadejte název úkolu: ").strip()
                while not nazev:
                    print("Název úkolu nemůže být prázdný.")
                    nazev = input("Zadejte název úkolu: ").strip()

                popis = input("Zadejte popis úkolu: ").strip()
                if not popis:
                    popis = "Bez popisu."
                    print("Používám výchozí hodnotu: 'Bez popisu.'")

                pridat_ukol(conn, nazev, popis)

            elif user_choice_int == 2:
                zobrazit_ukoly(conn)

            elif user_choice_int == 3:
                zobrazit_vsechny_ukoly(conn)

                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM ukoly")
                pocet = cursor.fetchone()[0]

                if pocet == 0:
                    return False

                while True:
                    try:
                        id_ukolu = int(
                            input("Zadejte ID úkolu, který chcete aktualizovat: ")
                        )
                        break
                    except ValueError:
                        print("Neplatný vstup. Zadejte číslo.")

                print("Vyberte nový stav úkolu:")
                print("1. Probíhá")
                print("2. Dokončeno")
                volba = input("Zadejte číslo volby: ")
                if volba == "1":
                    novy_stav = "Probíhá"
                elif volba == "2":
                    novy_stav = "Dokončeno"
                else:
                    print("Neplatná volba. Aktualizace zrušena.")
                    return False

                aktualizovat_ukol(conn, id_ukolu, novy_stav)

            elif user_choice_int == 4:
                zobrazit_vsechny_ukoly(conn)

                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM ukoly")
                pocet = cursor.fetchone()[0]

                if pocet == 0:
                    return False

                while True:
                    try:
                        id_ukolu = int(
                            input("Zadejte ID úkolu, který chcete odstranit: ")
                        )
                        break
                    except ValueError:
                        print("Neplatný vstup. Zadejte číslo.")

                odstranit_ukol(conn, id_ukolu)

            elif user_choice_int == 5:
                print("Díky za použití mého programu. Ukončuji program.")
                conn.close()
                return True
        else:
            print("Vybral sis číslo mimo daný rozsah. Vyber číslo mezi 1 a 5.")
    except ValueError:
        print("Nezadal sis platné číslo.")

    return False


if __name__ == "__main__":
    # Připojení k databázi a vytvoření tabulky
    conn = pripojeni_db()
    if conn is None:
        print("Nepodařilo se připojit k databázi. Ukončuji program.")
        exit(1)

    vytvoreni_tabulky(conn)

    # Spuštění hlavního menu
    while True:
        konec = hlavni_menu(conn)
        if konec:
            conn.close()
            break
