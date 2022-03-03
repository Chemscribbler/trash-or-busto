import imp
from math import factorial
from random import choice, sample
from dzmz.models import Card
from dzmz import db
from random import sample, randint


def randomizer():
    cards = Card.query.all()
    cardzero = sample(cards, 1)[0]
    if cardzero.num_ratings < 10:
        if cardzero.type == "identity":
            matches = Card.query.filter_by(type="identity", side=cardzero.side)
        else:
            matches = Card.query.filter_by(
                faction=cardzero.faction, type=cardzero.type
            ).all()
    elif cardzero.rating > 1200:
        if randint(0, 1):
            matches = Card.query.filter(
                Card.rating >= cardzero.rating - 400, Card.faction == cardzero.faction
            ).all()
        else:
            matches = Card.query.filter(
                Card.rating >= cardzero.rating - 400, Card.side == cardzero.side
            ).all()
    else:
        if randint(0, 1):
            matches = Card.query.filter_by(faction=cardzero.faction).all()
        else:
            return randomizer()
    try:
        cardone = sample(matches, 1)[0]
    except Exception as e:
        logger(cardone, e)
        return randomizer()
    if cardone.id == cardzero.id:
        return randomizer()
    return [cardzero, cardone]


def logger(card, error):
    with open("log.txt", "a") as f:
        f.write(f"\n{card}: {error}")
