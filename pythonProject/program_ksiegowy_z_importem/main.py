#Rozbuduj program do zarządzania firmą.
#Wszystkie funkcjonalności (komendy, zapisywanie i czytanie przy użyciu pliku itp.)
#pozostają bez zmian.
#Stwórz clasę Manager, która będzie implementowała dwie kluczowe metody -
#execute i assign. Przy ich użyciu wywołuj poszczególne fragmenty aplikacji.
#Metody execute i assign powinny zostać zaimplementowane zgodnie z
#przykładami z materiałów do zajęć.
#Niedozwolone są żadne zmienne globalne,
#wszystkie dane powinny być przechowywane wewnątrz obiektu Manager.

from utils import (wczytaj_saldo, zapisz_saldo,
                   wczytaj_magazyn, zapisz_magazyn, wczytaj_historie, zapisz_historie)

print(f"(Obecne saldo wynosi {wczytaj_saldo()} a oto stan magazynu: {wczytaj_magazyn()})")
print("Oto dostępne komendy: \n SALDO \n SPRZEDAZ \n ZAKUP \n KONTO \n LISTA \n MAGAZYN"
      "\n PRZEGLAD \n KONIEC \n Wpisz jedna z dostepnych komend")

class Manager:
    def __init__(self):
        self.magazyn = wczytaj_magazyn()
        self.konto = wczytaj_saldo()
        self.historia = []
        self.methods = {}

    def assign(self, action_name):
        def decorator(func):
            self.methods[action_name] = func
            return func
        return decorator

    def execute(self, action):
        action = action.upper()
        if action in self.methods:
            return self.methods[action](self)
        else:
            print(f"Nieznana komenda: {action}")

manager = Manager()

@manager.assign("SALDO")
def saldo(manager):
    kwota = int(input("Podaj kwote do dodania lub odjecia: "))
    manager.konto += kwota
    manager.historia.append((f"SALDO - dodano kwote {kwota}"))
    zapisz_saldo(manager.konto)

@manager.assign("SPRZEDAZ")
def sprzedaz(manager):
    produkt = input("Podaj nazwę produktu: ")
    cena = int(input("Podaj cenę produktu: "))
    liczba = int(input("Podaj liczbę sztuk produktu: "))

    if produkt in manager.magazyn and manager.magazyn[produkt]['liczba'] >= liczba:
        manager.magazyn[produkt]['liczba'] -= liczba
        manager.konto += cena * liczba
        manager.historia.append((f"SPRZEDAZ, sprzedano {produkt}, w cenie {cena}, liczba sztuk {liczba}"))

        if manager.magazyn[produkt]['liczba'] == 0:  # jeśli wykupuję ostatnią sztukę produktu
            del manager.magazyn[produkt]

    else:
        print("Nie ma wystarczajacej ilości produktu w magazynie.")

@manager.assign("ZAKUP")
def zakup(manager):
    produkt = input("Podaj nazwę produktu: ")
    cena = int(input("Podaj cenę produktu: "))
    liczba = int(input("Podaj liczbę sztuk produktu: "))

    if cena * liczba <= manager.konto:  # sprawdzam stan konta
        if produkt in manager.magazyn:
            manager.magazyn[produkt]['liczba'] += liczba
        else:
            manager.magazyn[produkt] = {'cena': cena, 'liczba': liczba}
        manager.konto -= cena * liczba
        zapisz_magazyn(manager.magazyn)
        manager.historia.append((f"ZAKUP : zakupiono {produkt}, ilosc sztuk: {liczba} w cenie {cena}"))
    else:
        print("Niewystarczajace srodki na koncie.")

@manager.assign("KONTO")
def konto(manager):
    print(f"Aktualne saldo wynosi: {manager.konto}")

@manager.assign("LISTA")
def lista(manager):
    if manager.magazyn:
        print("Oto stan magazynu: ")
        for (produkt, info) in manager.magazyn.items():
            print(f" -{produkt} : liczba: {info['liczba']} sztuk, cena: {info['cena']} ")
    else:
        print("magazyn jest pusty")

@manager.assign("MAGAZYN")
def magazyn(manager):
    print(f"Oto stan magazynu:{wczytaj_magazyn()}")
    produkt = input("Podaj nazwę produktu: ")
    if produkt in manager.magazyn:
        print(f"Produkt: {produkt}, Cena: {manager.magazyn[produkt]['cena']}, Ilość: {manager.magazyn[produkt]['liczba']}")
    else:
        print("Produkt nie znajduje się w magazynie.")

@manager.assign("PRZEGLAD")
def przeglad(manager):
    print("Historia operacji:")
    for wpis in manager.historia:
        print(wpis)

while True:
    action = input("Wpisz komende: ").upper()
    print(f"Wpisałes komende: {action}")
    if action == "KONIEC":
        print("zakonczenie programu")
        break
    else:
        manager.execute(action)


