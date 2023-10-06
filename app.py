import logging

from database_director import Director
from flask import Flask, render_template

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
director = Director()
db = director.create_database()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
