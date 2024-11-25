from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from models import db, Saldo, Magazyn, Historia
import logging
from datetime import datetime

# Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moja_baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super_tajny_klucz"


# baza danych
db.init_app(app)

#  Alembic
alembic = Alembic()
alembic.init_app(app)

# Funkcje
def wczytaj_saldo():
    saldo = Saldo.query.first()
    app.logger.info(f"Aktualne saldo: {saldo.wartosc if saldo else 'brak salda'}")
    if saldo:
        return saldo.wartosc
    else:
        nowe_saldo = Saldo(wartosc=0.0)
        db.session.add(nowe_saldo)
        db.session.commit()
        return 0.0


def zapisz_saldo(nowe_saldo):
    saldo = Saldo.query.first()
    if saldo:
        saldo.wartosc = nowe_saldo
    else:
        saldo = Saldo(wartosc=nowe_saldo)
        db.session.add(saldo)
    db.session.commit()


def wczytaj_magazyn():
    magazyn = Magazyn.query.all()
    app.logger.info(f"Wczytano magazyn: {magazyn}")
    return magazyn

def zapisz_magazyn(nazwa, ilosc, cena=None, zmniejsz=False):
    produkt = Magazyn.query.filter_by(nazwa=nazwa).first()
    if produkt:
        if zmniejsz:
            produkt.ilosc -= ilosc
            if produkt.ilosc < 0:
                produkt.ilosc = 0  # saldo nie moze być ujemne
        else:
            produkt.ilosc += ilosc
        if cena:
            produkt.cena = cena
        logging.info(f'Zaktualizowano produkt: {produkt.nazwa}, ilość: {produkt.ilosc}, cena: {produkt.cena}')
    else:
        if not zmniejsz:  # Dodaje produkt tylko w przypadku zakupu
            produkt = Magazyn(nazwa=nazwa, ilosc=ilosc, cena=cena)
            db.session.add(produkt)
            logging.info(f'Dodano nowy produkt: {produkt.nazwa}, ilość: {produkt.ilosc}, cena: {produkt.cena}')
    db.session.commit()


def zapisz_historie(operacja):
    nowa_operacja = Historia(operacja=operacja, timestamp=datetime.utcnow())
    db.session.add(nowa_operacja)
    db.session.commit()


# Ustawienie nagłówka Content-Type na UTF-8
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
        # formularz
        nazwa = request.form.get('nazwa')
        cena = request.form.get('cena')
        ilosc = request.form.get('ilosc')

        # Logowanie danych z formularza
        app.logger.info(f"Odebrano formularz: nazwa={nazwa}, cena={cena}, ilosc={ilosc}")

        # Walidacja danych wejściowych
        try:
            cena = float(cena)
            ilosc = int(ilosc)
        except ValueError:
            app.logger.error("Nieprawidłowe dane wejściowe! Cena lub ilość nie są liczbami.")
            flash("Nieprawidłowe dane wejściowe!", 'error')
            return redirect('/zakup')

        # Sprawdzenie salda
        saldo = wczytaj_saldo()
        koszt = cena * ilosc
        if koszt > saldo:
            flash("Brak wystarczających środków na koncie.", 'error')
            app.logger.warning(f"Za mało środków na zakup: saldo={saldo}, koszt={koszt}")
        else:
            saldo -= koszt
            zapisz_saldo(saldo)
            zapisz_magazyn(nazwa, ilosc, cena)
            zapisz_historie(f"Zakup: {nazwa}, {ilosc} szt. po {cena} PLN")
            flash(f"Zakupiono {ilosc} szt. produktu {nazwa}.", 'success')
            app.logger.info(f"Zakup zrealizowany: nazwa={nazwa}, ilosc={ilosc}, cena={cena}, nowe saldo={saldo}")

    # Załaduj magazyn i loguj jego stan
    produkty = wczytaj_magazyn()
    app.logger.info(f"Produkty w magazynie po zakupie: {produkty}")
    return render_template('zakup.html', produkty=produkty)


# Strona sprzedaży
@app.route('/sprzedaz', methods=['GET', 'POST'])
def sprzedaz():
    if request.method == 'POST':
        try:
            # Pobierz dane z formularza
            nazwa = request.form.get('nazwa')
            cena = float(request.form.get('cena'))
            ilosc = int(request.form.get('ilosc'))

            # Znajdź produkt w magazynie
            produkt = Magazyn.query.filter_by(nazwa=nazwa).first()

            if not produkt:
                flash(f"Produkt o nazwie '{nazwa}' nie istnieje w magazynie.", 'error')
                return redirect('/sprzedaz')

            if produkt.ilosc < ilosc:
                flash(f"Brak wystarczającej ilości produktu '{nazwa}' w magazynie.", 'error')
                return redirect('/sprzedaz')

            # Aktualizuj magazyn
            produkt.ilosc -= ilosc
            if produkt.ilosc == 0:
                db.session.delete(produkt)  # Usuń produkt, jeśli ilość wynosi 0
            db.session.commit()

            # Oblicz przychód i aktualizuj saldo
            przychod = cena * ilosc
            saldo = wczytaj_saldo() + przychod
            zapisz_saldo(saldo)

            # Zapisz operację w historii
            zapisz_historie(f"Sprzedaż: {nazwa}, {ilosc} szt. po {cena} PLN")

            flash(f"Sprzedano {ilosc} szt. produktu '{nazwa}' za {przychod} PLN.", 'success')

        except ValueError:
            flash("Nieprawidłowe dane w formularzu. Upewnij się, że cena i ilość są poprawne.", 'error')
        except Exception as e:
            app.logger.error(f"Błąd podczas sprzedaży: {e}")
            flash("Wystąpił nieoczekiwany błąd. Spróbuj ponownie.", 'error')

    # Pobierz aktualny stan magazynu
    magazyn = wczytaj_magazyn()
    return render_template('sprzedaz.html', produkty=[p.nazwa for p in magazyn])


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
    historia = Historia.query.order_by(Historia.timestamp).all()
    return historia

@app.route('/historia')
@app.route('/historia/<int:start>/<int:koniec>')
def historia(start=0, koniec=None):
    historia = Historia.query.order_by(Historia.timestamp).all()

    if koniec is None or koniec > len(historia):
        koniec = len(historia)

    if start < 0 or start >= koniec:
        flash(f'Niepoprawny zakres, proszę wybrać zakres od 0 do {len(historia)-1}', 'error')
        return render_template('historia.html', history=[])

    historia_zakres = historia[start:koniec]
    return render_template('historia.html', history=historia_zakres)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Baza danych została zainicjalizowana.")
    app.run(debug=True)

