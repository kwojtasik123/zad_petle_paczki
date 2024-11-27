from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from models import db, Pracownik, Punkty, Historia
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moja_baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super_tajny_klucz"

db.init_app(app)


# Funkcje pomocnicze
def wczytaj_pracownikow():
    return Pracownik.query.all()

def przyznaj_punkty(pracownik_id, ilosc):
    if ilosc <= 0:
        raise ValueError("Ilość punktów musi być większa niż zero.")

    pracownik = Pracownik.query.get(pracownik_id)
    if not pracownik:
        raise ValueError("Pracownik nie istnieje.")

    nowe_punkty = Punkty(pracownik_id=pracownik_id, ilosc=ilosc, data=datetime.utcnow())
    db.session.add(nowe_punkty)
    db.session.commit()
    zapisz_historie(f"Przyznano {ilosc} punktów dla {pracownik.imie} {pracownik.nazwisko}.")

def zapisz_historie(operacja):
    nowa_operacja = Historia(operacja=operacja, timestamp=datetime.utcnow())
    db.session.add(nowa_operacja)
    db.session.commit()

def pracownicy_bez_punktow_przez_miesiace(miesiace):
    """
    Zwraca listę pracowników, którzy nie dostali punktów przez ostatnie `miesiace`.
    """
    granica = datetime.utcnow() - relativedelta(months=miesiace)
    return Pracownik.query.filter(~Pracownik.punkty.any(Punkty.data >= granica)).all()

def pracownicy_z_najmniejsza_liczba_punktow(limit=5):
    """
    Zwraca listę pracowników z najmniejszą liczbą punktów.
    """
    pracownicy = db.session.query(
        Pracownik.id, Pracownik.imie, Pracownik.nazwisko,
        db.func.sum(Punkty.ilosc).label('suma_punktow')
    ).outerjoin(Punkty).group_by(Pracownik.id).order_by('suma_punktow').limit(limit).all()

    return pracownicy

# Endpointy
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        imie = request.form.get('imie')
        nazwisko = request.form.get('nazwisko')
        pensja = request.form.get('pensja')
        data_zatrudnienia = request.form.get('data_zatrudnienia')

        try:
            pensja = float(pensja)
            data_zatrudnienia = datetime.strptime(data_zatrudnienia, '%Y-%m-%d').date()

            nowy_pracownik = Pracownik(imie=imie, nazwisko=nazwisko,
                                       pensja=pensja, data_zatrudnienia=data_zatrudnienia)
            db.session.add(nowy_pracownik)
            db.session.commit()
            flash(f"Dodano pracownika: {imie} {nazwisko}", 'success')
        except Exception as e:
            flash(f"Błąd: {e}", 'error')

    pracownicy = wczytaj_pracownikow()
    if not pracownicy:
        flash("Brak pracowników w bazie danych. Dodaj pierwszego pracownika!", "info")
    return render_template('index.html', pracownicy=pracownicy)


@app.route('/przyznaj_punkty', methods=['GET', 'POST'])
def przyznaj_punkty_view():
    if request.method == 'POST':
        pracownik_id = request.form.get('pracownik_id')
        ilosc = request.form.get('ilosc')

        try:
            ilosc = int(ilosc)
            przyznaj_punkty(pracownik_id, ilosc)
            flash(f"Przyznano {ilosc} punktów.", 'success')
        except Exception as e:
            flash(f"Błąd: {e}", 'error')

    pracownicy = wczytaj_pracownikow()
    return render_template('przyznaj_punkty.html', pracownicy=pracownicy)


@app.route('/historia')
def historia():
    historia = Historia.query.order_by(Historia.timestamp.desc()).all()
    return render_template('historia.html', historia=historia)


@app.route('/rekomendacje', methods=['GET', 'POST'])
def rekomendacje():
    miesiace = request.args.get('miesiace', default=6, type=int)  # Domyślnie 6 miesięcy
    pracownicy_bez_punktow = pracownicy_bez_punktow_przez_miesiace(miesiace)
    najmniej_punktow = pracownicy_z_najmniejsza_liczba_punktow()

    return render_template(
        'rekomendacje.html',
        pracownicy_bez_punktow=pracownicy_bez_punktow,
        najmniej_punktow=najmniej_punktow,
        miesiace=miesiace
    )
@app.route('/pracownik/<int:pracownik_id>')
def szczegoly_pracownika(pracownik_id):
    pracownik = Pracownik.query.get_or_404(pracownik_id)
    return render_template('szczegoly_pracownika.html', pracownik=pracownik)

@app.after_request
def after_request(response):
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy wszystkie tabele w bazie danych
    app.run(debug=True)
