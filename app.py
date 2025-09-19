# Imports
from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
from flask_scss import Scss
from models import Kweek, LiquidCultuur, Graanbroed
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
            new_kweek = Kweek()
            db.session.add(new_kweek)
            db.session.commit()

            soort = request.form.get("soort")
            kenmerk = request.form.get("kenmerk")
            kweekID = new_kweek.uniekeID
            # innoculatiedatum has default-value

            new_liquidcultuur = LiquidCultuur(
                soort = soort,
                kenmerk = kenmerk,
                kweekID = kweekID
            )
            db.session.add(new_liquidcultuur)
            db.session.commit()

            flash('New liquid culture succesvol added!')
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"There has been an error: {e}")
            return redirect(url_for('add_liquid_culture'))

    return render_template("add_liquid_culture.html")

@app.route("/liquid_culture/<int:liquidcultuur_id>", methods=["POST","GET"])
def display_liquid_culture(liquidcultuur_id):
    liquid_culture = LiquidCultuur.query.get_or_404(liquidcultuur_id)

    return render_template("display_liquid_culture.html", liquid_culture=liquid_culture)

@app.route('/add_grain_spawn/<int:liquid_culture_id>', methods=["POST", "GET"])
def add_grain_spawn(liquid_culture_id):
    if request.method == "GET":
        return render_template("add_grain_spawn.html", liquid_culture_id=liquid_culture_id)

    if request.method == "POST":
        try:
            contaminatie = request.form.get("contaminatie")
            geschud = request.form.get("geschud")
            liquidcultuurID = liquid_culture_id
            # innoculatiedatum has default-value

            new_grainspawn = Graanbroed(
                contaminatie = contaminatie,
                geschud = geschud,
                liquidcultuurID = liquidcultuurID
            )
            db.session.add(new_grainspawn)
            db.session.commit()

            flash('New grain spawn succesvol added!')
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            flash(f"There has been an error: {e}")
            return redirect(url_for('add_grain_spawn', liquid_culture_id=liquid_culture_id))

@app.route("/grain_spawn/<int:grain_spawn_id>", methods=["POST","GET"])
def display_grain_spawn(grain_spawn_id):
    grain_spawn = Graanbroed.query.get_or_404(grain_spawn_id)

    return render_template("display_grain_spawn.html", grain_spawn=grain_spawn)

if __name__ == "__main__":
    with app.app_context():
        db.create_all();
    app.run(debug=True)