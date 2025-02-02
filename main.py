
ukoly = ["Úkol 1 - Uklidit", "Úkol 2 - Vytřít"]

def pridat_ukol():
    nazev_ukolu = str(input("Zadejte název úkolu: "))
    popis_ukolu = str(input("Zadejte popis úkolu: "))
    ukol_s_popisem =  f"{nazev_ukolu} - {popis_ukolu}"
    ukoly.append(ukol_s_popisem)
    print(f"Úkol '{nazev_ukolu}' byl přidán.\n")


def zobrazit_ukoly():
    if len(ukoly) == 0:
        print("Seznam úkolů je prázdný. Začněte přidáním úkolu volbou č. 1.\n")
    else:
        print(f"\nSeznam úkolů:")
        for (index, ukol) in enumerate(ukoly, start=1):
            print(f"{index}. {ukol}")
        print("")


def odstranit_ukol():
    if len(ukoly) == 0:
        print("Seznam úkolů je prázdný. Začněte přidáním úkolu volbou č. 1.\n")
    else:
        print(f"\nSeznam úkolů:")
        for (index, ukol) in enumerate(ukoly, start=1):
            print(f"{index}. {ukol}")
        print("")

    user_choice = input("Zadejte číslo úkolu, který chcete odstranit: ")
    try:
        user_choice_int = int(user_choice)
        if user_choice_int in range(len(ukoly)+1):
            # user_choice_int -= 1
            print(f"Odstranil jsem položku '{ukoly[user_choice_int-1]}' ze seznamu úkolů.\n")
            ukoly.pop(user_choice_int-1)

        else:
            print("Zadal jsi číslo mimo rozsah seznamu úkolů.\n")
    except ValueError:
        print("Nezadal jsi číselnou hodnotu.\n")



def hlavni_menu():
    global task_run
    print("Správce úkolů - Hlavní menu")
    print("1. Přidat nový úkol")
    print("2. Zobrazit všechny úkoly")
    print("3. Odstranit úkol")
    print("4. Konec programu")
    user_choice = input("Vyberte možnost 1-4: ")
    try:
        user_choice_int = int(user_choice)
        if 1 <= user_choice_int <= 4:
            if user_choice_int == 1:
                pridat_ukol()
            if user_choice_int == 2:
                zobrazit_ukoly()
            if user_choice_int == 3:
                odstranit_ukol()
            if user_choice_int == 4:
                print("Díky za použití mého programu. Ukončuji program.")
                task_run = False
        else:
            print("Vyber číslo mezi 1 a 4.\n")
    except ValueError:
        print("Nezadal si platné číslo.\n")

task_run = True
while task_run:
    hlavni_menu()

