import imp
from flask import render_template, flash, redirect, url_for
from dzmz import app
from dzmz.models import Card
from sqlalchemy import desc


@app.route("/")
@app.route("/index")
def index():
    return "Hello World"


@app.route("/rank")
@app.route("/ranking")
def ranking():
    cards = Card.query.order_by(desc("rating")).all()
    return render_template("rankings.html", title="Rankings", cards=cards)
