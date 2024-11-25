from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Saldo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wartosc = db.Column(db.Float, nullable=False)

class Magazyn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(80), unique=True, nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)
    cena = db.Column(db.Float, nullable=False)

class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operacja = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)