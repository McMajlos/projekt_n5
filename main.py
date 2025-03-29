import mysql.connector


def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="engeto", database="engeto"
        )
        print("Připojení k databázi bylo úspěšné.")
        return conn, conn.cursor()

    except mysql.connector.Error as err:
        print(f"Chyba při připojování: {err}")


def vytvoreni_tabulky():
    """Vytvoří tabulku 'ukoly', pokud ještě neexistuje."""
    try:
        cursor.execute("SHOW TABLES LIKE 'ukoly'")
        table_exists = cursor.fetchone()

        if table_exists:
            print("Tabulka 'ukoly' již existuje, není potřeba ji vytvářet.")
        else:
            cursor.execute(
                """
                CREATE TABLE ukoly (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nazev VARCHAR(100),
                    popis TEXT,
                    stav ENUM('Nezahájeno','Probíhá','Hotovo'), 
                    datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
            print("Tabulka 'ukoly' byla úspěšně vytvořena.")

    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}")
    finally:
        cursor.close()
        conn.close()


def pridat_ukol():
    """Přidá úkol do databáze. Používám ve funkci hlavni_menu()"""
    while True:
        nazev_ukolu = str(input("Zadejte název úkolu: "))
        if nazev_ukolu.strip() == "":
            print("Název úkolu nemůže být prázdný.")
        else:
            break

    popis_ukolu = str(input("Zadejte popis úkolu: "))
    if popis_ukolu.strip() == "":
        popis_ukolu = "Bez popisu."
        print("Bez popisu.")

    try:
        cursor.execute(
            "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
            (nazev_ukolu, popis_ukolu),
        )
        conn.commit()
        print(f"Úkol '{nazev_ukolu}' byl přidán.")
    except mysql.connector.Error as err:
        print(f"Chyba při vkládání dat: {err}")


def zobrazit_ukoly():
    """Zobrazí úkoly, které mají stav "Dokončeno" nebo "Probíhá"."""
    try:
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


def zobrazit_vsechny_ukoly():
    """Zobrazí všechny úkoly v databázi. Používám ve funkci aktualizovat_ukol(), odstranit_ukol()"""
    try:
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


def aktualizovat_ukol():
    """Aktualizuje stav úkolu v databázi."""
    try:
        cursor.execute("SELECT * FROM ukoly")
        ukoly = cursor.fetchall()

        if len(ukoly) == 0:
            print("Žádné úkoly nebyly nalezeny. Databáze je prázdná!")
            return

        print("")
        print("Zobrazuji všechny úkoly, které jsou v databázi:")
        zobrazit_vsechny_ukoly()

        while True:
            try:
                id_ukolu = int(input("Zadejte ID úkolu, který chcete aktualizovat: "))
            except ValueError:
                print("Neplatný vstup. Zadejte číslo.")
                continue

            cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
            ukol = cursor.fetchone()

            if ukol:
                break 
            else:
                print(f"Úkol s ID {id_ukolu} nebyl nalezen. Zkuste to znovu.")

        while True:
            print("Vyberte nový stav úkolu:")
            print("1. Probíhá")
            print("2. Dokončeno")
            volba = input("Zadejte číslo volby: ")

            if volba == "1":
                novy_stav = "Probíhá"
                break
            elif volba == "2":
                novy_stav = "Dokončeno"
                break
            else:
                print("Neplatná volba. Zkuste to znovu.")

        cursor.execute(
            "UPDATE ukoly SET stav = %s WHERE id = %s",
            (novy_stav, id_ukolu),
        )
        conn.commit()
        print(f"Úkol s ID {id_ukolu} byl aktualizován na stav '{novy_stav}'.")

    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci úkolu: {err}")


def odstranit_ukol():
    """Odstraní úkol z databáze."""
    print("\nZobrazuji všechny úkoly, které jsou v databázi:")
    try:
        cursor.execute("SELECT * FROM ukoly")
        ukoly = cursor.fetchall()

        if len(ukoly) == 0:
            print("Žádné úkoly nebyly nalezeny. Databáze je prázdná!")
            return

        zobrazit_vsechny_ukoly()

        while True:
            try:
                id_ukolu = int(input("Zadejte ID úkolu, který chcete odstranit: "))
            except ValueError:
                print("Neplatný vstup. Zadejte číslo.")
                continue

            cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
            ukol = cursor.fetchone()

            if ukol:
                break
            else:
                print(f"Úkol s ID {id_ukolu} nebyl nalezen. Zkuste to znovu.")

        cursor.execute(
            "DELETE FROM ukoly WHERE id = %s",
            (id_ukolu,),
        )
        conn.commit()
        print(f"Úkol s ID {id_ukolu} byl úspěšně odstraněn.")

    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci úkolu: {err}")


def hlavni_menu():
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
                pridat_ukol()
            if user_choice_int == 2:
                zobrazit_ukoly()
            if user_choice_int == 3:
                aktualizovat_ukol()
            if user_choice_int == 4:
                odstranit_ukol()
            if user_choice_int == 5:
                print("Díky za použití mého programu. Ukončuji program.")
                cursor.close()
                conn.close()
                task_run = False
        else:
            print("Vybral si číslo mimo daný rozsah. Vyber číslo mezi 1 a 4.")
    except ValueError:
        print("Nezadal si platné číslo.")


# Připojení k databázi a vytvoření tabulky
conn, cursor = pripojeni_db()

task_run = True
while task_run:
    hlavni_menu()
