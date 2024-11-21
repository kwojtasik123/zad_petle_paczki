import os
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
    """Wczytuje stan magazynu z pliku."""
    if os.path.exists(MAGAZYN_FILE):
        with open(MAGAZYN_FILE, "r", encoding="utf-8") as file:
            return eval(file.read())  # Konwersja z tekstu na dict
    return {}


def zapisz_magazyn(magazyn):
    """Zapisuje stan magazynu do pliku."""
    with open(MAGAZYN_FILE, "w", encoding="utf-8") as file:
        file.write(str(magazyn))


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
            zapisz_historie(f"Zakup: {nazwa}, {ilosc} szt. po {cena} PLN")
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
            zapisz_historie(f"Sprzedaż: {nazwa}, {ilosc} szt. po {cena} PLN")
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
            zapisz_historie(f"Zmiana salda: {zmiana} PLN")
            flash(f"Saldo zostało zaktualizowane o {zmiana} PLN.", 'success')
        except ValueError:
            flash("Podano nieprawidłową wartość.", 'error')
    saldo = wczytaj_saldo()
    return render_template('saldo.html', saldo=saldo)

# Strona historii operacji
def load_history():
    with open('data/historia.txt', 'r') as file:
        return file.readlines()

@app.route('/historia')
@app.route('/historia/<int:start>/<int:koniec>')
def historia(start=0, koniec=None):
    history = load_history()

    # Ustawienie wartości domyślnych dla 'start' i 'koniec'
    if koniec is None:
        koniec = len(history)  # Jeżeli 'koniec' nie jest podany, pokaż wszystkie linie od 'start'

    # Sprawdzenie poprawności zakresu
    if start < 0 or koniec > len(history) or start >= koniec:
        flash(f'Błędny zakres. Dostępne linie to 1-{len(history)}.', 'error')
        # Zwrócenie wszystkich dostępnych operacji
        return render_template('historia.html', history=history)

    # Wyciągnięcie odpowiedniego zakresu
    selected_history = history[start:koniec]

    return render_template('historia.html', history=selected_history)

if __name__ == '__main__':
    app.run(debug=True)


