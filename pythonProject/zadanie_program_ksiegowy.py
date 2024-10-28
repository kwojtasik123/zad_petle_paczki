#opis komend:
#saldo.txt - Program pobiera kwotę do dodania lub odjęcia z konta
#sprzedaż - Program pobiera nazwę produktu, cenę oraz liczbę sztuk.
# Produkt musi znajdować się w magazynie. Obliczenia respektuje względem konta i magazynu
# (np. produkt "rower" o cenie 100 i jednej sztuce spowoduje odjęcie z magazynu produktu
# "rower" oraz dodanie do konta kwoty 100).
#zakup - Program pobiera nazwę produktu, cenę oraz liczbę sztuk. Produkt zostaje dodany do magazynu, jeśli go nie było.
# Obliczenia są wykonane odwrotnie do komendy "sprzedaz". Saldo konta po zakończeniu operacji „zakup” nie może być ujemne.
#konto - Program wyświetla stan konta.
#lista - Program wyświetla całkowity stan magazynu wraz z cenami produktów i ich ilością.
#magazyn.txt - Program wyświetla stan magazynu dla konkretnego produktu. Należy podać jego nazwę.
#przegląd - Program pobiera dwie zmienne „od” i „do”, na ich podstawie wyświetla wszystkie wprowadzone akcje zapisane
# pod indeksami od „od” do „do”. Jeżeli użytkownik podał pustą wartość „od” lub „do”, program powinien wypisać przegląd
# od początku lub/i do końca. Jeżeli użytkownik podał zmienne spoza zakresu, program powinien o tym poinformować
# i wyświetlić liczbę zapisanych komend (żeby pozwolić użytkownikowi wybrać odpowiedni zakre
#koniec - Aplikacja kończy działanie
#DODATKOWE WYMAGANIA:
#Aplikacja od uruchomienia działa tak długo, aż podamy komendę "koniec".
#Komendy saldo.txt, sprzedaż i zakup są zapamiętywane przez program, aby móc użyć komendy "przeglad".
#Po wykonaniu dowolnej komendy (np. "saldo.txt") aplikacja ponownie wyświetla informację o dostępnych komendach,
# a także prosi o wprowadzenie jednej z nich.
#Zadbaj o błędy, które mogą się pojawić w trakcie wykonywania operacji (np. przy komendzie "zakup" jeśli dla produktu
# podamy ujemną kwotę, aplikacja powinna wyświetlić informację o niemożności wykonania operacji i jej nie wykonać).
# Zadbaj też o prawidłowe typy danych.

#program księgowy
print("Oto dostępne komendy: \n SALDO \n SPRZEDAŻ \n ZAKUP \n KONTO \n LISTA \n MAGAZYN"
      "\n PRZEGLĄD \n KONIEC \n Wpisz jedną z dostępnych komend")

#moje zmienne
stan_magazynu=dict()
konto =0
historia=[] #zapisywana historia

while True:
    komenda = input("Wpisz komendę: ").upper()
    print(f"Wpisałeś komendę: {komenda}")
    if komenda == "KONIEC":
        print("zakończenie programu")
        break

    elif komenda == "SALDO":
        kwota = int(input("Podaj kwotę do dodania lub odjęcia: "))
        konto += kwota
        historia.append((f"SALDO - dodano kwotę {kwota}"))


    elif komenda == "SPRZEDAŻ":
        produkt = input("Podaj nazwę produktu: ")
        cena = int(input("Podaj cenę produktu: "))
        liczba = int(input("Podaj liczbę sztuk produktu: "))

        if produkt in stan_magazynu and stan_magazynu[produkt]['liczba'] >= liczba:
            stan_magazynu[produkt]['liczba'] -= liczba
            konto += cena * liczba
            historia.append((f"SPRZEDAŻ, sprzedano {produkt}, w cenie {cena}, liczba sztuk {liczba}"))

            if stan_magazynu[produkt]['liczba'] == 0: #jeśli wykupuję ostatnią sztukę produktu
                del stan_magazynu[produkt]

        else:
            print("Nie ma wystarczającej ilości produktu w magazynie.")

    elif komenda == "ZAKUP":
        produkt = input("Podaj nazwę produktu: ")
        cena = int(input("Podaj cenę produktu: "))
        liczba = int(input("Podaj liczbę sztuk produktu: "))

        if cena * liczba <= konto: #sprawdzam stan konta
            #jeśli produkt jest w magazynie, zwiększam liczbę
            if produkt in stan_magazynu:
                stan_magazynu[produkt]['liczba'] += liczba
            else:
                #jeśli go nie ma, dodaję nowy produkt
                stan_magazynu[produkt] = {'cena': cena, 'liczba': liczba}
            konto -= cena * liczba
            historia.append((f"ZAKUP : zakupiono {produkt}, ilość sztuk: {liczba} w cenie {cena}"))
        else:
            print("Niewystarczające środki na koncie.")

    elif komenda == "KONTO":
        print(f"Aktualne saldo.txt wynosi: {konto}")

    elif komenda == "LISTA":
        if stan_magazynu:
            print("Oto stan magazynu: ")
            for (produkt, info) in stan_magazynu.items():
                print(f" -{produkt} : liczba: {info['liczba']} sztuk, cena: {info['cena']} ")
        else:
            print("magazyn.txt jest pusty")
    elif komenda == "MAGAZYN":
        produkt = input("Podaj nazwę produktu: ")
        if produkt in stan_magazynu:
            print(
                f"Produkt: {produkt}, Cena: {stan_magazynu[produkt]['cena']}, Ilość: {stan_magazynu[produkt]['liczba']}")
        else:
            print("Produkt nie znajduje się w magazynie.")
    elif komenda == "PRZEGLĄD":
        od = input("Podaj zakres OD (lub zostaw puste): ")
        do = input("Podaj zakres DO (lub zostaw puste): ")
        if od == "":
            od = 0
        else:
            od = int(od)
        if do == "":
            do = len(historia)
        else:
            do = int(do)
        if od < 0 or do > len(historia) or od > do:
            print(f"Nieprawidłowy zakres. Liczba zapisanych komend: {len(historia)}")
        else:
            for i in range(od, do):
                print(historia[i])
    else:
        print("Nieznana komenda. Spróbuj ponownie.")













