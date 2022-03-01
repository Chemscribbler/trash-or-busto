import imp
from random import choice, sample
from dzmz.models import Card
from dzmz import db
from random import sample, randint


def randomizer():
    cards = Card.query.all()
    cardzero = sample(cards, 1)[0]
    if cardzero.num_ratings < 10:
        matches = Card.query.filter_by(
            faction=cardzero.faction, type=cardzero.type
        ).all()
    elif cardzero.rating > 1200:
        matches = Card.query.filter(Card.rating >= 800, faction=cardzero.faction).all()
    elif cardzero.rating > 1800:
        matches = Card.query.filter_by(side=cardzero.side).all()
    else:
        if randint(0, 1):
            matches = Card.query.filter_by(faction=cardzero.faction).all()
        else:
            return randomizer()
    cardone = sample(matches, 1)[0]
    if cardone.id == cardzero.id:
        return randomizer()
    return [cardzero, cardone]
