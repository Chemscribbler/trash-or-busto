from flask import render_template, redirect, request, url_for
from dzmz import app
from dzmz.models import Card
from sqlalchemy import desc
from dzmz.randomselect import randomizer

from dzmz.scoring import update_scores


@app.route("/")
# @app.route("/index")
def index():
    pair = randomizer()
    return render_template("index.html", pair=pair)


@app.route("/rank")
@app.route("/ranking")
def ranking():
    corp_cards = Card.query.filter_by(side="corp").order_by(desc("rating")).all()
    runner_cards = Card.query.filter_by(side="runner").order_by(desc("rating")).all()

    return render_template(
        "global_rankings.html",
        title="Rankings",
        runner_cards=runner_cards,
        corp_cards=corp_cards,
    )


@app.route("/rank/faction")
@app.route("/rank/factions")
def top_5_factions():
    factions = Card.query.with_entities(Card.faction).distinct().all()
    top_cards = {}
    for faction in factions:
        faction = faction[0]
        top_cards[faction] = (
            Card.query.filter_by(faction=faction)
            .order_by(desc(Card.rating))
            .limit(5)
            .all()
        )
    # print(top_cards)
    return render_template("top_five_rankings.html", title="Rankings", cards=top_cards)


@app.route("/antirank/factions")
def bot_5_factions():
    factions = Card.query.with_entities(Card.faction).distinct().all()
    top_cards = {}
    for faction in factions:
        faction = faction[0]
        top_cards[faction] = (
            Card.query.filter_by(faction=faction).order_by(Card.rating).limit(5).all()
        )
    return render_template("top_five_rankings.html", title="Rankings", cards=top_cards)


@app.route("/rank/<string:faction>")
def faction_rank(faction):
    cards = Card.query.filter_by(faction=faction).order_by(desc(Card.rating)).all()


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
