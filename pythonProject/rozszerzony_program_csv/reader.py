# Napisz program oparty na klasach i dziedziczeniu, który odczyta wejściowy
# plik, następnie zmodyfikuje go i wyświetli
# w terminalu jego zawartość, a na końcu zapisze w wybranej lokalizacji.

# Uruchomienie programu przez terminal:
# python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2>
# ... <zmiana_n>

# <plik_wejsciowy> - nazwa pliku, który ma zostać odczytany, np. in.csv,
# in.json lub in.txt
# <plik_wyjsciowy> - nazwa pliku, do którego ma zostać zapisana zawartość,
# np. out.csv, out.json, out.txt lub out.pickle
# <zmiana_x> - Zmiana w postaci "x,y,wartosc" - x (kolumna) oraz y (wiersz)
# są współrzędnymi liczonymi od 0, natomiast "wartosc" zmianą która ma trafić na podane miejsce.

# Wymagane formaty: .csv, .json, .txt, .pickle

import sys
import csv
import json
import pickle

if len(sys.argv) < 3:
    print("Usage: python reader.py <input_file> <output_file> <change_1> <change_2> ... <change_n>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
changes = sys.argv[3:]


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        raise NotImplementedError("Metoda load musi być zaimplementowana w klasie dziedziczącej")

    def save(self, data):
        raise NotImplementedError("Metoda save musi być zaimplementowana w klasie dziedziczącej")


class CSVFileHandler(FileHandler):
    def load(self):
        with open(self.file_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            return [row for row in reader]

    def save(self, data):
        with open(self.file_path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)


class JSONFileHandler(FileHandler):
    def load(self):
        with open(self.file_path, "r") as json_file:
            data = json.load(json_file)
            # Konwertuj dane do formatu listy list
            return [[item['item'], item['value1'], item['value2'], item['value3']] for item in data]

    def save(self, data):
        # Konwertuj dane z powrotem do formatu listy słowników
        json_data = [{'item': row[0], 'value1': row[1], 'value2': row[2], 'value3': row[3]} for row in data]
        with open(self.file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)


class TXTFileHandler(FileHandler):
    def load(self):
        with open(self.file_path, "r") as txt_file:
            return txt_file.readlines()

    def save(self, data):
        with open(self.file_path, "w") as txt_file:
            txt_file.writelines(data)


class PickleFileHandler(FileHandler):
    def load(self):
        with open(self.file_path, "rb") as pickle_file:
            return pickle.load(pickle_file)

    def save(self, data):
        with open(self.file_path, "wb") as pickle_file:
            pickle.dump(data, pickle_file)


def apply_changes(data, changes):
    for change in changes:
        row, col, new_value = change.split(",")
        row, col = int(row), int(col)
        data[row][col] = new_value
    return data


def main():
    # sprawdzam rodzaj pliku
    if input_file.endswith('.csv'):
        reader = CSVFileHandler(input_file)
    elif input_file.endswith('.json'):
        reader = JSONFileHandler(input_file)
    elif input_file.endswith('.txt'):
        reader = TXTFileHandler(input_file)
    elif input_file.endswith('.pickle'):
        reader = PickleFileHandler(input_file)
    else:
        print("Nieznany format pliku")
        sys.exit(1)

    data = reader.load()

    # wyswietlam zapisane dane
    print("Zawartosc pliku:")
    for row in data:
        print(row)

    # Zapisuje zmiany
    data = apply_changes(data, changes)

    # Sprawdzam rodzaj pliku, aby zapisac dane
    if output_file.endswith('.csv'):
        writer = CSVFileHandler(output_file)
    elif output_file.endswith('.json'):
        writer = JSONFileHandler(output_file)
    elif output_file.endswith('.txt'):
        writer = TXTFileHandler(output_file)
    elif output_file.endswith('.pickle'):
        writer = PickleFileHandler(output_file)
    else:
        print("Nieznany format pliku")
        sys.exit(1)

    writer.save(data)

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print("Changes applied:")
    for change in changes:
        row, col, new_value = change.split(",")
        print(f"row: {row}, column {col}, new value {new_value}")


if __name__ == "__main__":
    main()
