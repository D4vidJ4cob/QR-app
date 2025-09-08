# Imports
from flask import Flask, render_template
from extensions import db
from flask_scss import Scss
import models
import os
from dotenv import load_dotenv

# Load dotenv
load_dotenv()

app = Flask(__name__)
Scss(app)

# Get password from .env
password = os.getenv("DB_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://root:{password}@localhost/dnd_mushrooms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 



@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/tables")
# def tables():
#     inspector = db.inspect(db.engine)
#     return {"tables": inspector.get_table_names()}


if __name__ == "__main__":
    app.run(debug=True)
