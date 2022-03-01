from turtle import update
from flask import render_template, redirect, request, url_for
from dzmz import app
from dzmz.models import Card
from sqlalchemy import desc
from dzmz.randomselect import randomizer

from dzmz.scoring import update_scores


@app.route("/")
@app.route("/index")
def index():
    pair = randomizer()
    return render_template("index.html", pair=pair)


@app.route("/rank")
@app.route("/ranking")
def ranking():
    cards = Card.query.order_by(desc("rating")).all()
    return render_template("rankings.html", title="Rankings", cards=cards)


@app.route("/vote/<int:cardzero_id>-<int:cardone_id>", methods=["POST", "GET"])
def record_vote(cardzero_id, cardone_id):
    cardzero = Card.query.filter_by(id=cardzero_id).first()
    cardone = Card.query.filter_by(id=cardone_id).first()
    if request.form["result"] == "card0win":
        update_scores(winner=cardzero, loser=cardone)
    elif request.form["result"] == "card1win":
        update_scores(winner=cardone, loser=cardzero)
    else:
        update_scores(ties=[cardzero, cardone])
    return redirect(url_for("index"))
