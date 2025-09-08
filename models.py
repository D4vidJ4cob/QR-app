from extensions import db
from datetime import date

class Kweek(db.Model):
    __tablename__ = "kweek"

    uniekeID = db.Column(db.Integer, primary_key=True)
    soort = db.Column(db.String(50))

    # Relatie: één Kweek kan meerdere LiquidCultuur hebben
    liquid_cultures = db.relationship('LiquidCultuur', backref='kweek', lazy=True)

class LiquidCultuur(db.Model):
    __tablename__ = "liquidcultuur"

    liquidcultuurID = db.Column(db.Integer, primary_key=True, nullable=False)
    kweekID = db.Column(db.Integer, db.ForeignKey('kweek.uniekeID'), nullable=False)
    innoculatiedatum = db.Column(db.Date, default=date.today)
    kenmerk = db.Column(db.String(50))

class Graanbroed(db.Model):
    __tablename__ = "graanbroed"
    graanbroedID = db.Column(db.Integer, primary_key=True, nullable=False)
    liquidcultuurID = db.Column(db.Integer, db.ForeignKey('liquidcultuur.liquidcultuurID'), nullable=False)
    innoculatiedatum = db.Column(db.Date, default=date.today)
    contaminatie = db.Column(db.String(4))
    geschud = db.Column(db.String(4))

    # Relatie: één LiquidCultuur kan meerdere Graanbroed hebben
    liquidcultuur = db.relationship('LiquidCultuur', backref='graanbroeden', lazy=True)

class Substraat(db.Model):
    __tablename__ = "substraat"

    substraatID = db.Column(db.Integer, primary_key=True, nullable=False)
    graanbroedID = db.Column(db.Integer, db.ForeignKey('graanbroed.graanbroedID'), nullable=False)
    incubatiedatum = db.Column(db.Date, default=date.today)
    innoculatiedatum = db.Column(db.Date, default=date.today)
    contaminatie = db.Column(db.Boolean, default=False)

    # Relatie: één Graanbroed kan meerdere Substraat hebben
    graanbroed = db.relationship('Graanbroed', backref='substraten', lazy=True)