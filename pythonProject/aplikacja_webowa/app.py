import os
import json
from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime

# Pliki danych
SALDO_FILE = "data/saldo.txt"
MAGAZYN_FILE = "data/magazyn.txt"
HISTORIA_FILE = "data/historia.txt"

# Konfiguracja aplikacji
app = Flask(__name__)
app.secret_key = "super_tajny_klucz"

# Funkcje
def wczytaj_saldo():
    """Wczytuje saldo z pliku."""
    if os.path.exists(SALDO_FILE):
        with open(SALDO_FILE, "r", encoding="utf-8") as file:
            return float(file.read().strip())
    return 0.0


def zapisz_saldo(saldo):
    """Zapisuje saldo do pliku."""
    with open(SALDO_FILE, "w", encoding="utf-8") as file:
        file.write(str(saldo))


def wczytaj_magazyn():
    """Wczytuje stan magazynu z pliku JSON."""
    if os.path.exists(MAGAZYN_FILE):
        with open(MAGAZYN_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def zapisz_magazyn(magazyn):
    """Zapisuje stan magazynu do pliku w formacie JSON."""
    with open(MAGAZYN_FILE, "w", encoding="utf-8") as file:
        json.dump(magazyn, file, ensure_ascii=False, indent=4)

def zapisz_historie(operacja):
    """Zapisuje operacje do historii."""
    with open(HISTORIA_FILE, "a", encoding="utf-8") as file:
        file.write(operacja + "\n")


# Ustawienie nagłówka na UTF-8
@app.after_request
def after_request(response):
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response


# Strona główna
@app.route('/')
def index():
    saldo = wczytaj_saldo()
    magazyn = wczytaj_magazyn()
    return render_template('index.html', saldo=saldo, magazyn=magazyn)

# Strona zakupu
@app.route('/zakup', methods=['GET', 'POST'])
def zakup():
    if request.method == 'POST':
        nazwa = request.form.get('nazwa')
        cena = float(request.form.get('cena'))
        ilosc = int(request.form.get('ilosc'))
        koszt = cena * ilosc
        saldo = wczytaj_saldo()
        if koszt > saldo:
            flash("Brak wystarczających środków na koncie.", 'error')
        else:
            saldo -= koszt
            zapisz_saldo(saldo)
            magazyn = wczytaj_magazyn()
            magazyn[nazwa] = magazyn.get(nazwa, 0) + ilosc
            zapisz_magazyn(magazyn)

            # Zapisz historię zakupu
            zapisz_historie(f"ZAKUP: zakupiono {nazwa}, ilość sztuk: {ilosc} w cenie {cena}")
            flash(f"Zakupiono {ilosc} szt. produktu {nazwa}.", 'success')
    magazyn = wczytaj_magazyn()
    return render_template('zakup.html', produkty=magazyn.keys())



# Strona sprzedaży
@app.route('/sprzedaz', methods=['GET', 'POST'])
def sprzedaz():
    if request.method == 'POST':
        nazwa = request.form.get('nazwa')
        cena = float(request.form.get('cena'))
        ilosc = int(request.form.get('ilosc'))
        magazyn = wczytaj_magazyn()
        if nazwa not in magazyn or magazyn[nazwa] < ilosc:
            flash("Brak wystarczającej ilości produktu w magazynie.", 'error')
        else:
            magazyn[nazwa] -= ilosc
            if magazyn[nazwa] == 0:
                del magazyn[nazwa]
            zapisz_magazyn(magazyn)
            przychod = cena * ilosc
            saldo = wczytaj_saldo() + przychod
            zapisz_saldo(saldo)

            # Zapisz historię sprzedaży
            zapisz_historie(f"SPRZEDAŻ: sprzedano {nazwa}, ilość sztuk: {ilosc} w cenie {cena}")
            flash(f"Sprzedano {ilosc} szt. produktu {nazwa}.", 'success')
    magazyn = wczytaj_magazyn()
    return render_template('sprzedaz.html', produkty=magazyn.keys())


# Strona salda
@app.route('/zmiana_salda', methods=['GET', 'POST'])
def zmiana_salda():
    if request.method == 'POST':
        try:
            zmiana = float(request.form.get('zmiana'))
            saldo = wczytaj_saldo() + zmiana
            zapisz_saldo(saldo)

            # Zapisz historię zmiany salda
            if zmiana > 0:
                zapisz_historie(f"SALDO - dodano kwotę {zmiana} PLN")
            else:
                zapisz_historie(f"SALDO - zmniejszono kwotę {zmiana} PLN")
            flash(f"Saldo zostało zaktualizowane o {zmiana} PLN.", 'success')
        except ValueError:
            flash("Podano nieprawidłową wartość.", 'error')
    saldo = wczytaj_saldo()
    return render_template('saldo.html', saldo=saldo)


def load_historia():
    """Wczytuje historię operacji jako listę słowników, obsługując różne formaty zapisu."""
    if not os.path.exists(HISTORIA_FILE):
        print("Brak pliku z historią operacji!")
        return []

    historia = []
    with open(HISTORIA_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Pomijamy puste linie

            print(f"Przetwarzam linię: {line}")  # Debug: co aktualnie parsujemy

            try:
                entry = {"operacja": line}  # Domyślny wpis z pełnym opisem
                parts = line.split(", ")

                # Parsowanie SALDO
                if "SALDO" in line:
                    print("Znaleziono SALDO")  # Debug: wskazuje, że rozpoznano 'SALDO'
                    if "dodano kwotę" in line:
                        parts = line.split("dodano kwotę")
                        try:
                            kwota = float(parts[1].strip())
                            entry = {"operacja": "SALDO", "zmiana": f"+{kwota}"}
                            print(f"Kwota SALDO (dodano): {kwota}")  # Debug: pokazujemy dodaną kwotę
                        except ValueError:
                            print(f"Błąd parsowania kwoty SALDO: {line}")
                    elif "zmniejszono kwotę" in line:
                        parts = line.split("zmniejszono kwotę")
                        try:
                            kwota = float(parts[1].strip())
                            entry = {"operacja": "SALDO", "zmiana": f"-{kwota}"}
                            print(f"Kwota SALDO (zmniejszoną): {kwota}")
                        except ValueError:
                            print(f"Błąd parsowania kwoty SALDO: {line}")

                # Parsowanie ZAKUP
                elif "ZAKUP" in line or "Zakup" in line:
                    print("Znaleziono ZAKUP")  # Debug: wskazuje, że rozpoznano 'ZAKUP'
                    if "Ilość" in line and "Cena" in line:
                        parts = line.split(", ")
                        produkt = parts[0].split(":")[-1].strip()
                        ilosc_str = parts[1].split(":")[-1].strip()
                        cena_str = parts[2].split(":")[-1].replace("PLN", "").strip()

                        try:
                            ilosc = int(ilosc_str)
                            cena = float(cena_str)
                            entry = {
                                "operacja": "ZAKUP",
                                "produkt": produkt,
                                "ilosc": ilosc,
                                "cena": cena
                            }
                            print(f"ZAKUP - produkt: {produkt}, ilość: {ilosc}, cena: {cena}")
                        except ValueError:
                            print(f"Błąd parsowania ZAKUP: Ilość: {ilosc_str}, Cena: {cena_str}")
                            continue  # Jeśli wystąpi błąd, pomijamy tę linię

                # Parsowanie SPRZEDAŻ
                elif "Sprzedano" in line:
                    print("Znaleziono SPRZEDAŻ")  # Debug: wskazuje, że rozpoznano 'SPRZEDAŻ'
                    parts = line.split(", ")
                    if len(parts) >= 2:
                        nazwa = parts[0].split(":")[-1].strip()
                        ilosc_str = parts[1].split()[0]
                        cena_str = parts[1].split("po")[-1].split()[0]

                        try:
                            ilosc = int(ilosc_str)
                            cena = float(cena_str)
                            entry = {
                                "operacja": "SPRZEDAŻ",
                                "produkt": nazwa,
                                "ilosc": ilosc,
                                "cena": cena
                            }
                            print(f"SPRZEDAŻ - produkt: {nazwa}, ilość: {ilosc}, cena: {cena}")
                        except ValueError:
                            print(f"Błąd parsowania SPRZEDAŻ: Ilość: {ilosc_str}, Cena: {cena_str}")
                            continue  # Jeśli wystąpi błąd, pomijamy tę linię

                historia.append(entry)

            except (IndexError, ValueError) as e:
                print(f"Błąd parsowania linii: {line}. Szczegóły: {e}")
                continue

    return historia

@app.route('/historia')
@app.route('/historia/<int:start>/<int:koniec>')
def historia(start=0, koniec=None):
    historia = load_historia()  # Wczytujemy historię
    total = len(historia)

    if koniec is None:
        koniec = total  # Jeśli koniec nie jest podany, ustawiamy go na total

    # Sprawdzamy, czy start i koniec są poprawne
    if start < 0 or koniec > total or start >= koniec:
        flash(f"Błędny zakres. Dostępne linie to 1-{total}.", "error")
        return redirect(url_for('historia', start=0, koniec=min(10, total)))  # Przekierowanie na poprawny zakres

    # Tworzymy wycinek historii, który chcemy pokazać
    selected_historia = historia[start:koniec]
    return render_template('historia.html', historia=selected_historia, total=total)


if __name__ == '__main__':
    app.run(debug=True)
