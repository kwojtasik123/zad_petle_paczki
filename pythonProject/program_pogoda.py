#Napisz program, który sprawdzi, czy danego dnia będzie padać.
# Użyj do tego poniższego API. Aplikacja ma działać następująco:

#Program pyta dla jakiej daty należy sprawdzić pogodę.
# Data musi byc w formacie YYYY-mm-dd, np. 2022-11-03.
# W przypadku nie podania daty, aplikacja przyjmie za poszukiwaną datę
# następny dzień.
#Aplikacja wykona zapytanie do API w celu poszukiwania stanu pogody.
#Istnieją trzy możliwe informacje dla opadów deszczu:
#Będzie padać (dla wyniku większego niż 0.0)
#Nie będzie padać (dla wyniku równego 0.0)
#Nie wiem (gdy wyniku z jakiegoś powodu nie ma lub wartość jest ujemna)
#Wyniki zapytań powinny być zapisywane do pliku. Jeżeli szukana data znajduje sie juz
# w pliku, nie wykonuj zapytania do API, tylko zwróć wynik z pliku.
#W URL należy uzupełnić parametry: latitude, longitude oraz searched_date

#https://open-meteo.com/


import requests
import json
from datetime import datetime, timedelta

# Ustawienie lokalizacji
LATITUDE = "51.1000"  # Szerokość geograficzna dla Wrocławia
LONGITUDE = "17.0333"  # Długość geograficzna dla Wrocławia
FILE_NAME = "dane_pogoda.json"

def pobierz_dane(data_pogoda):
    API_url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=rain_sum&timezone=Europe%2FWarsaw&start_date={data_pogoda}&end_date={data_pogoda}"
    response = requests.get(API_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def sprawdz_opady(data_pogoda):
    dane = pobierz_dane(data_pogoda)
    if dane:
        rain_sum = dane['daily']['rain_sum'][0]
        if rain_sum > 0.0:
            return "Bedzie padac"
        elif rain_sum == 0.0:
            return "Nie bedzie padac"
        else:
            return "Nie wiem"
    else:
        return "Nie wiem"

def zapisz_do_pliku(data_pogoda, wynik):
    try:
        with open(FILE_NAME, 'r') as plik:
            dane = json.load(plik)
    except FileNotFoundError:
        dane = {}

    dane[data_pogoda] = wynik

    with open(FILE_NAME, 'w') as plik:
        json.dump(dane, plik)

def odczytaj_z_pliku(data_pogoda):
    try:
        with open(FILE_NAME, 'r') as plik:
            dane = json.load(plik)
        return dane.get(data_pogoda, None)
    except FileNotFoundError:
        return None

def main():
    data_pogoda = input("Podaj datę w formacie YYYY-MM-DD: ")
    if not data_pogoda:
        current_date = datetime.now()
        next_date = current_date + timedelta(days=1)
        data_pogoda = next_date.strftime('%Y-%m-%d')

    wynik = odczytaj_z_pliku(data_pogoda)
    if wynik is None:
        wynik = sprawdz_opady(data_pogoda)
        zapisz_do_pliku(data_pogoda, wynik)

    print(f"Prognoza na {data_pogoda}: {wynik}")

if __name__ == "__main__":
    main()
