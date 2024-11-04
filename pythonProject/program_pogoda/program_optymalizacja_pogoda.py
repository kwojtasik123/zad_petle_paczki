#zoptymalizuj kod z poprzedniego zadania z pogodą.

#Utwórz klasę WeatherForecast, która będzie służyła do odczytywania i zapisywania pliku
#a także odpytywania API.

#Obiekt klasy WeatherForecast dodatkowo musi poprawnie implementować cztery
#metody:
 #__setitem__
# __getitem__
 #__iter__
 #items
#Wykorzystaj w kodzie poniższe zapytania:

#weather_forecast[date] da odpowiedź na temat pogody dla podanej daty
#weather_forecast.items() zwróci generator tupli w formacie (data, pogoda) dla już zapisanych rezultatów przy wywołaniu
#weather_forecast to iterator zwracający wszystkie daty, dla których znana jest pogoda

import requests
import json
from datetime import datetime, timedelta

class WeatherForecast:
    FILE_NAME = "dane_pogoda.json"
    LATITUDE = "51.1000"  # Szerokość geograficzna dla Wrocławia
    LONGITUDE = "17.0333"  # Długość geograficzna dla Wrocławia

    def __init__(self):
        self.odczytaj_z_pliku()

    def odczytaj_z_pliku(self):
        try:
            with open(self.FILE_NAME, 'r') as plik:
                self.data = json.load(plik)
        except FileNotFoundError:
            self.data = {}

    def zapisz_do_pliku(self):
        with open(self.FILE_NAME, 'w') as plik:
            json.dump(self.data, plik)

    def __setitem__(self, date, weather):
        self.data[date] = weather
        self.zapisz_do_pliku()

    def __getitem__(self, date):
        return self.data.get(date, None)

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return self.data.items()

    def pobierz_dane(self, date):
        API_url = f"https://api.open-meteo.com/v1/forecast?latitude={self.LATITUDE}&longitude={self.LONGITUDE}&daily=rain_sum&timezone=Europe%2FWarsaw&start_date={date}&end_date={date}"
        response = requests.get(API_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def sprawdz_opady(self, date):
        dane = self.pobierz_dane(date)
        if dane:
            suma_opadow = dane['daily']['rain_sum'][0]
            if suma_opadow > 0.0:
                return "Bedzie padac"
            elif suma_opadow == 0.0:
                return "Nie bedzie padac"
        return "Nie wiem"

def main():
    weather_forecast = WeatherForecast()

    data_pogoda = input("Podaj datę w formacie YYYY-MM-DD: ")
    if not data_pogoda:
        current_date = datetime.now()
        next_date = current_date + timedelta(days=1)
        data_pogoda = next_date.strftime('%Y-%m-%d')

    wynik = weather_forecast[data_pogoda]
    if wynik is None:
        wynik = weather_forecast.sprawdz_opady(data_pogoda)
        weather_forecast[data_pogoda] = wynik

    print(f"Prognoza na {data_pogoda}: {wynik}")

if __name__ == "__main__":
    main()
