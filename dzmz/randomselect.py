from random import sample
from dzmz.models import Card
from random import sample, randint


def randomizer():
    cards = Card.query.all()
    cardzero = sample(cards, 1)[0]
    # Low card ratings
    if cardzero.num_ratings < 10:
        # If Identity only compare with IDs
        if cardzero.type == "identity":
            matches = Card.query.filter_by(type="identity", side=cardzero.side)
        # Match in faction types
        else:
            matches = Card.query.filter_by(
                faction=cardzero.faction, type=cardzero.type
            ).all()
    else:
        if randint(0, 1):
            matches = Card.query.filter(
                Card.rating >= cardzero.rating - 225,
                Card.rating <= cardzero.rating + 225,
                Card.faction == cardzero.faction,
            ).all()
        else:
            matches = Card.query.filter(
                Card.rating >= cardzero.rating - 225,
                Card.rating <= cardzero.rating + 225,
                Card.side == cardzero.side,
            ).all()
    try:
        cardone = sample(matches, 1)[0]
    except Exception:
        return randomizer()
    if cardone.id == cardzero.id:
        return randomizer()
    if cardzero.num_ratings > 20:
        if randint(0, 1):
            return randomizer()
    return [cardzero, cardone]


def logger(card, error):
    with open("log.txt", "a") as f:
        f.write(f"\n{card}: {error}")
