import imp
from flask import render_template, flash, redirect, url_for
from dzmz import app
from dzmz.models import Card
from sqlalchemy import desc
import random


@app.route("/")
@app.route("/index")
def index():
    cards = Card.query.all()
    pair = random.sample(cards, 2)
    return render_template("index.html", pair=pair)


@app.route("/rank")
@app.route("/ranking")
def ranking():
    cards = Card.query.order_by(desc("rating")).all()
    return render_template("rankings.html", title="Rankings", cards=cards)
