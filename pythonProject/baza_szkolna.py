#Utwórz program do zarządzania bazą szkolną. Istnieje możliwość tworzenia trzech typów użytkowników (uczeń, nauczyciel, wychowawca) a także zarządzania nimi.
#Po uruchomieniu programu można wpisać jedną z następujących komend: utwórz, zarządzaj, koniec.
#Polecenie "utwórz" - Przechodzi do procesu tworzenia użytkowników.
#Polecenie "zarządzaj" - Przechodzi do procesu zarządzania użytkownikami.
#Polecenie "koniec" - Kończy działanie aplikacji.
#Proces tworzenia użytkowników:
#Należy wpisać opcję, którą chcemy wybrać: uczeń, nauczyciel, wychowawca, koniec.
# Po wykonaniu każdej z opcji (oprócz "koniec") wyświetla to menu ponownie.
#Polecenie "uczeń" - Należy pobrać imię i nazwisko ucznia
# (jako jedna zmienna, można pobrać je jako dwie zmienne, jeżeli zostanie to poprawnie obsłużone) oraz nazwę klasy (np. "3C")
#Polecenie "nauczyciel" - Należy pobrać imię i nazwisko nauczyciela
# (jako jedna zmienna, labo dwie, jeżeli zostanie to poprawnie obsłużone),
# nazwę przedmiotu prowadzonego, a następnie w nowych liniach nazwy klas, które prowadzi nauczyciel, aż do otrzymania pustej linii.
#Polecenie "wychowawca" - Należy pobrać imię i nazwisko wychowawcy
# (jako jedna zmienna, albo dwie, jeżeli zostanie to poprawnie obsłużone), a także nazwę prowadzonej klasy.
#Polecenie "koniec" - Wraca do pierwszego menu.
#Proces zarządzania użytkownikami:

#Należy wpisać opcję, którą chcemy wybrać: klasa, uczen, nauczyciel, wychowawca, koniec.
# Po wykonaniu każdej z opcji (oprócz "koniec") wyświetla to menu ponownie.
#Polecenie "klasa" - Należy pobrać klasę, którą chcemy wyświetlić (np. "3C")
# program ma wypisać wszystkich uczniów, którzy należą do tej klasy, a także wychowawcę tejże klasy.
#Polecenie "uczeń" - Należy pobrać imię i nazwisko uczenia,
# program ma wypisać wszystkie lekcje, które ma uczeń a także nauczycieli, którzy je prowadzą.
#Polecenie "nauczyciel" - Należy pobrać imię i nazwisko nauczyciela,
# program ma wypisać wszystkie klasy, które prowadzi nauczyciel.
#Polecenie "wychowawca" - Należy pobrać imię i nazwisko nauczyciela,
# a program ma wypisać wszystkich uczniów, których prowadzi wychowawca.
#Polecenie "koniec" - Wraca do pierwszego menu.

class Uczen:
    def __init__(self, imie, nazwisko, klasa):
        self.imie=imie
        self.nazwisko=nazwisko
        self.klasa=klasa

    def __str__(self):
        return f"<Uczen: {self.imie}, {self.nazwisko}, klasa: {self.klasa}>"

class Nauczyciel:
    def __init__(self,imie, nazwisko, przedmiot, klasy):
        self.imie=imie
        self.nazwisko=nazwisko
        self.przedmiot=przedmiot
        self.klasy=klasy

    def __str__(self):
        return f"<Nauczyciel: {self.imie}, {self.nazwisko}, przedmiot: {self.przedmiot}, prowadzone klasy: {self.klasy}>"

class Wychowawca:
    def __init__(self, imie, nazwisko, klasa):
        self.imie=imie
        self.nazwisko=nazwisko
        self.klasa=klasa

    def __str__(self):
        return f"<Wychowawca: {self.imie}, {self.nazwisko}, klasa: {self.klasa}>"

def wczytaj_obiekt(typ_obiektu):
    imie = input("Podaj imie: ")
    nazwisko = input("Podaj nazwisko: ")
    if typ_obiektu == "uczen":
        klasa = input("Podaj klase: ")
        return Uczen(imie, nazwisko, klasa)
    elif typ_obiektu == "nauczyciel":
        przedmiot = input("Podaj przedmiot: ")
        klasy = []
        while True:
            klasa = input("Podaj klase (lub zostaw puste aby zakonczyc): ")
            if klasa == "":
                break
            klasy.append(klasa)
        return Nauczyciel(imie, nazwisko, przedmiot, klasy)
    elif typ_obiektu == "wychowawca":
        klasa = input("Podaj klase: ")
        return Wychowawca(imie, nazwisko, klasa)

def menu_glowne():
    """
    pozwoli wyswietlic menu glowne na koniec wykonanego zadania
    :return:
    """
    while True:
        akcja = input("Wybierz jedno z poleceń [utworz, zarzadzaj, koniec] ")

        if akcja == "utworz":
            fun_akcja_utworz()
        elif akcja == "zarzadzaj":
            fun_akcja_zarzadzaj()
        elif akcja == "koniec":
            print("Koniec programu")
            break
        else:
            print("Nieznane polecenie, spróbuj ponownie")

def fun_akcja_utworz():
    """
    funkcja wykonuje opcje z menu Utworz

    """
    while True:
        akcja_utworz = input("Co chcesz utworzyc:[uczen, nauczyciel, wychowawca, koniec] ")

        if akcja_utworz == "koniec":
            break
        elif akcja_utworz == "uczen":
            print("Dodaj ucznia")

            nowy_uczen = wczytaj_obiekt("uczen")
            uczniowie.append(nowy_uczen)

        elif akcja_utworz == "nauczyciel":

            print("Dodaj nauczyciela")
            nowy_nauczyciel = wczytaj_obiekt("nauczyciel")
            nauczyciele.append(nowy_nauczyciel)

        elif akcja_utworz == "wychowawca":
            print("Dodaj wychowawcę")

            nowy_wychowawca = wczytaj_obiekt("wychowawca")
            wychowawcy.append(nowy_wychowawca)

        else:
            print(f"Nie mozna dodac elementu {akcja_utworz}")

        menu_glowne()

def fun_akcja_zarzadzaj():
    while True:
        akcja_zarzadzaj = input("Co chcesz zarządzać: [klasa, uczen, nauczyciel, wychowawca, koniec] ")
        if akcja_zarzadzaj == "koniec":
            break
        elif akcja_zarzadzaj == "klasa":
            klasa = input("Podaj klase: ")
            print(f"Uczniowie w klasie {klasa}:")
            for uczen in uczniowie:
                if uczen.klasa == klasa:
                    print(uczen)
            print(f"Wychowawca klasy {klasa}:")
            for wychowawca in wychowawcy:
                if wychowawca.klasa == klasa:
                    print(wychowawca)
        elif akcja_zarzadzaj == "uczen":
            imie = input("Podaj imie ucznia: ")
            nazwisko = input("Podaj nazwisko ucznia: ")
            print(f"Lekcje ucznia {imie} {nazwisko}:")
            for nauczyciel in nauczyciele:
                if any(uczen.imie == imie and uczen.nazwisko == nazwisko for uczen in uczniowie):
                    print(f"{nauczyciel.przedmiot} prowadzony przez {nauczyciel.imie} {nauczyciel.nazwisko}")
        elif akcja_zarzadzaj == "nauczyciel":
            imie = input("Podaj imie nauczyciela: ")
            nazwisko = input("Podaj nazwisko nauczyciela: ")
            print(f"Klasy prowadzone przez nauczyciela {imie} {nazwisko}:")
            for nauczyciel in nauczyciele:
                if nauczyciel.imie == imie and nauczyciel.nazwisko == nazwisko:
                    print(", ".join(nauczyciel.klasy))
        elif akcja_zarzadzaj == "wychowawca":
            imie = input("Podaj imie wychowawcy: ")
            nazwisko = input("Podaj nazwisko wychowawcy: ")
            print(f"Uczniowie prowadzeni przez wychowawcę {imie} {nazwisko}:")
            for wychowawca in wychowawcy:
                if wychowawca.imie == imie and wychowawca.nazwisko == nazwisko:
                    for uczen in uczniowie:
                        if uczen.klasa == wychowawca.klasa:
                            print(uczen)
        menu_glowne()


uczniowie=[]
nauczyciele=[]
wychowawcy=[]

print("Witaj w programie do obsługi bazy szkolnej")
while True:
        akcja = input("Wybierz jedno z poleceń [utworz, zarzadzaj, koniec] ")
        if akcja == "koniec":
            break
        elif akcja == "utworz":
            fun_akcja_utworz()
        elif akcja == "zarzadzaj":
            fun_akcja_zarzadzaj()
else:
    print(f"Komenda {akcja} nie istnieje.")