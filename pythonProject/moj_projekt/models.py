from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Pracownik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(50), nullable=False)
    nazwisko = db.Column(db.String(50), nullable=False)
    data_zatrudnienia = db.Column(db.DateTime, nullable=False)
    pensja = db.Column(db.Float, nullable=False)
    podwyzka = db.Column(db.DateTime, nullable=True)
    punkty = db.relationship('Punkty', backref='pracownik', lazy=True)

class Punkty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pracownik_id = db.Column(db.Integer, db.ForeignKey('pracownik.id'), nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operacja = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
