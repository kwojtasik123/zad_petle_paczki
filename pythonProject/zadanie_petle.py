#Napisz program do obsługi ładowarki paczek.
#Po uruchomieniu, aplikacja pyta ile paczek chcesz wysłać,
#a następnie wymaga podania wagi dla każdej z nich.
#Na koniec działania program powinien wyświetlić w podsumowaniu:
#1. Liczbę paczek wysłanych
#2. Liczbę kilogramów wysłanych
#3. Suma &quot;pustych&quot; - kilogramów (brak optymalnego pakowania).
#Liczba paczek * 20 - liczba #kilogramów wysłanych
#4. Która paczka miała najwięcej &quot;pustych&quot; kilogramów, jaki to był wynik
#Restrykcje:
#Waga elementów musi być z przedziału od 1 do 10 kg.
#Każda paczka może maksymalnie zmieścić 20 kilogramów towaru.
#W przypadku, jeżeli dodawany element przekroczy wagę towaru,
# ma zostać dodany do nowej paczki, a obecna wysłana
#W przypadku podania wagi elementu mniejszej od 1kg lub większej od 10kg
#dodawanie paczek zostaje zakończone i wszystkie paczki są wysłane.
#Wyświetlane jest podsumowanie.

import random
DEBUG = True
# zbieranie informacji o ilości nadawanych paczek
liczba_elementow = int(input("Ile paczek chcesz wysłać?"))

# przechowywanie informacji o zmiennych
suma_paczek = 0
suma_kg_obecnej_paczki = 0
suma_kg_wszystkich_paczek =0
suma_pustych_kg=0
max_waga_paczki = 20
max_pustych_kg=0
suma_pustych_kg_wszystkich_paczek=0
numer_paczki_z_max_pustych_kg=0
print()
# Pętla do zbierania wag paczek
for i in range(liczba_elementow):
    waga = float(input(f"Podaj wagę paczki {i+1}: "))
    if waga <=1 or waga >=10:
        print("podano nieprawidłową wagę paczki. Kończę dodawanie paczek")
        break
#dodaję wagę do paczki
    else:
        suma_kg_obecnej_paczki+=waga
        suma_kg_wszystkich_paczek+=waga
        if suma_kg_obecnej_paczki > max_waga_paczki:
            suma_paczek+=1
            suma_pustych_kg=max_waga_paczki-suma_kg_obecnej_paczki
            suma_pustych_kg_wszystkich_paczek+=suma_pustych_kg
            if suma_kg_obecnej_paczki>max_waga_paczki:
                max_waga_paczki=suma_kg_obecnej_paczki
            if suma_pustych_kg>max_pustych_kg:
                max_pustych_kg=suma_pustych_kg
            numer_paczki_z_max_pustych_kg=suma_paczek
            suma_kg_obecnej_paczki=0

        #dodaj ostatnia paczke, jesli nie byla dodana
        if suma_kg_obecnej_paczki>0:
            suma_paczek+=1
            puste_kg=max_waga_paczki-suma_kg_obecnej_paczki
            suma_pustych_kg_wszystkich_paczek+=puste_kg
            if puste_kg>max_pustych_kg:
                max_pustych_kg=puste_kg
                numer_paczki_z_max_pustych_kg=suma_paczek

print((f"Podsumowanie:\n suma wyslanych paczek wynosi: {suma_paczek}"
      f"\n suma wyslanych kilogramow wynosi {suma_kg_wszystkich_paczek}"
      f"\n numer paczki z najwieksza iloscia pustych kilogramow to"
      f" {numer_paczki_z_max_pustych_kg} i znajduje sie tam {max_pustych_kg} kg"))
