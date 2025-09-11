# Imports
from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
from flask_scss import Scss
from models import Kweek, LiquidCultuur
import os
from dotenv import load_dotenv

# Load dotenv
load_dotenv()

app = Flask(__name__)
Scss(app)


# Get password and secret key from .env
password = os.getenv("DB_PASSWORD")
secret_key = os.getenv("SECRET_KEY")

app.config['SECRET_KEY'] = 'test'

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://root:{password}@localhost/dnd_mushrooms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_liquid_culture", methods=["POST","GET"])
def add_liquid_culture():
    if request.method == "POST":
        try:
            nieuwe_kweek = Kweek()
            db.session.add(nieuwe_kweek)
            db.session.commit()

            soort = request.form.get("soort")
            kenmerk = request.form.get("kenmerk")
            kweekID = nieuwe_kweek.uniekeID
            # innoculatiedatum has default-value
            nieuwe_liquidcultuur = LiquidCultuur(
                soort = soort,
                kenmerk = kenmerk,
                kweekID = kweekID
            )
            db.session.add(nieuwe_liquidcultuur)
            db.session.commit()

            flash('Nieuwe liquid culture succesvol toegevoegd!')
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Er is een fout opgetreden: {e}")
            return redirect(url_for('add_liquid_culture'))

    return render_template("add_liquid_culture.html")

# @app.route('/add_grain_spawn', methods=["POST", "GET"])
# def add_grain_spawn():
#     if request.method == "POST":

if __name__ == "__main__":
    with app.app_context():
        db.create_all();
    app.run(debug=True)
