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

#Dodatkowe zadanie:
#Saldo konta oraz magazyn.txt mają zostać zapisane do pliku tekstowego, a przy kolejnym uruchomieniu programu
# ma zostać odczytany. Zapisać należy również historię operacji (przegląd), która powinna być rozszerzana
# przy każdym kolejnym uruchomieniu programu.

#program księgowy

from utils import (wczytaj_saldo, zapisz_saldo,
wczytaj_magazyn, zapisz_magazyn, wczytaj_historie, zapisz_historie)

print(f"(Obecne saldo.txt wynosi {wczytaj_saldo()} a oto stan magazynu: {wczytaj_magazyn()})")
print("Oto dostępne komendy: \n SALDO \n SPRZEDAZ \n ZAKUP \n KONTO \n LISTA \n MAGAZYN"
      "\n PRZEGLAD \n KONIEC \n Wpisz jedna z dostepnych komend")

#moje zmienne
magazyn=wczytaj_magazyn()
konto =wczytaj_saldo()
historia=[] #zapisywana historia

while True:
    komenda = input("Wpisz komende: ").upper()
    print(f"Wpisałes komende: {komenda}")
    if komenda == "KONIEC":
        print("zakonczenie programu")
        break

    elif komenda == "SALDO":
        kwota = int(input("Podaj kwote do dodania lub odjecia: "))
        konto += kwota
        historia.append((f"SALDO - dodano kwote {kwota}"))
        # Zapisz saldo.txt przed zakończeniem programu
        zapisz_saldo(konto)


    elif komenda == "SPRZEDAZ":
        produkt = input("Podaj nazwę produktu: ")
        cena = int(input("Podaj cenę produktu: "))
        liczba = int(input("Podaj liczbę sztuk produktu: "))

        if produkt in magazyn and magazyn[produkt]['liczba'] >= liczba:
            magazyn[produkt]['liczba'] -= liczba
            konto += cena * liczba
            historia.append((f"SPRZEDAZ, sprzedano {produkt}, w cenie {cena}, liczba sztuk {liczba}"))

            if magazyn[produkt]['liczba'] == 0: #jeśli wykupuję ostatnią sztukę produktu
                del magazyn[produkt]

        else:
            print("Nie ma wystarczajacej ilości produktu w magazynie.")

    elif komenda == "ZAKUP":
        produkt = input("Podaj nazwę produktu: ")
        cena = int(input("Podaj cenę produktu: "))
        liczba = int(input("Podaj liczbę sztuk produktu: "))

        if cena * liczba <= konto: #sprawdzam stan konta
            #jeśli produkt jest w magazynie, zwiększam liczbę
            if produkt in magazyn:
                magazyn[produkt]['liczba'] += liczba
            else:
                #jeśli go nie ma, dodaję nowy produkt
                magazyn[produkt] = {'cena': cena, 'liczba': liczba}
            konto -= cena * liczba
            zapisz_magazyn(magazyn)
            historia.append((f"ZAKUP : zakupiono {produkt}, ilosc sztuk: {liczba} w cenie {cena}"))
        else:
            print("Niewystarczajace srodki na koncie.")

    elif komenda == "KONTO":
        print(f"Aktualne saldo.txt wynosi: {konto}")

    elif komenda == "LISTA":
        if magazyn:
            print("Oto stan magazynu: ")
            for (produkt, info) in magazyn.items():
                print(f" -{produkt} : liczba: {info['liczba']} sztuk, cena: {info['cena']} ")
        else:
            print("magazyn.txt jest pusty")
    elif komenda == "MAGAZYN":
        print(f"Oto stan magazynu:{wczytaj_magazyn()}")
        produkt = input("Podaj nazwę produktu: ")
        if produkt in magazyn:
            print(
                f"Produkt: {produkt}, Cena: {magazyn[produkt]['cena']}, Ilość: {magazyn[produkt]['liczba']}")
        else:
            print("Produkt nie znajduje się w magazynie.")
    elif komenda == "PRZEGLAD":
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
        print("Nieznana komenda. Sprobuj ponownie.")

zapisz_saldo(konto)
zapisz_magazyn(magazyn)
zapisz_historie(historia)
