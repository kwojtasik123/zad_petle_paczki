from constants import BAZA_SALDA
from constants import BAZA_MAGAZYNU
from constants import BAZA_HISTORII

def wczytaj_saldo(filepath=BAZA_SALDA):
    """
    Wczytuje saldo.txt z pliku
    """
    with open(filepath, "r") as plik:
        zawartosc_pliku = plik.read()

    return int(zawartosc_pliku)

def zapisz_saldo(konto, filepath=BAZA_SALDA):
    """
    Zapisuje saldo.txt do pliku
    """
    with open(filepath, "w") as plik:
        plik.write(str(konto))

def wczytaj_magazyn(file_path=BAZA_MAGAZYNU):
    """
    Wczytuje stan magazynu z pliku
    """
    magazyn = {}
    with open(file_path, "r") as file:
         for line in file:
            produkt, liczba, cena = line.strip().split(":")
            magazyn[produkt] = {"liczba":liczba, "cena":cena}
    return magazyn

def zapisz_magazyn(magazyn, file_path=BAZA_MAGAZYNU):
    
    """
    Zapisuje stan magazynu do pliku
    """
    with open(file_path, "w") as file:
        for produkt, info in magazyn.items():
            file.write(f"{produkt}:{info["liczba"]}:{info["cena"]}\n")

def wczytaj_historie(file_path=BAZA_HISTORII):
    """
    Wczytuje historię operacji z pliku
    """
    historia = []
    with open(file_path, "r") as file:
        for line in file:
            historia.append(line.strip())

    return historia

def zapisz_historie(historia, file_path=BAZA_HISTORII):
    """
    Zapisuje historię operacji do pliku
    """
    print(historia)
    with open(file_path, "a") as file:
        for wpis in historia:
            file.write(f"{wpis}\n")

