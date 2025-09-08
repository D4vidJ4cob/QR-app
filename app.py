from flask import Flask, render_template
from extensions import db
import models

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://root:Tibenater15!@localhost/dnd_mushrooms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tables")
def tables():
    inspector = db.inspect(db.engine)
    return {"tables": inspector.get_table_names()}


if __name__ == "__main__":
    app.run(debug=True)
