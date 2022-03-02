from dzmz import db
from dzmz.models import Pair


def update_scores(winner=None, loser=None, ties=None):
    if winner is None:
        cardzero = ties[0]
        cardzero_k = calc_k_fact(cardzero)
        cardone = ties[1]
        cardone_k = calc_k_fact(cardone)
        cardzero_prime = cardzero.rating + cardzero_k * (
            0.5 - expected_points(cardzero, cardone)
        )
        cardone_prime = cardone.rating + cardone_k * (
            0.5 - expected_points(cardone, cardzero)
        )
        cardzero.rating = cardzero_prime
        cardone.rating = cardone_prime
        cardzero.num_ratings += 1
        cardone.num_ratings += 1
        db.session.commit()
    else:
        winner_k = calc_k_fact(winner)
        loser_k = calc_k_fact(loser)
        winner_prime = winner.rating + winner_k * (1 - expected_points(winner, loser))
        loser_prime = loser.rating + loser_k * (0 - expected_points(loser, winner))
        winner.rating = winner_prime
        winner.num_ratings += 1
        loser.num_ratings += 1
        loser.rating = loser_prime
        db.session.commit()


def expected_points(cardzero, cardone):
    q_zero = 10 ** (cardzero.rating / 400)
    q_one = 10 ** (cardone.rating / 400)
    return q_zero / (q_zero + q_one)


def calc_k_fact(card):
    if card.num_ratings < 30:
        return 40
    elif card.rating < 2400:
        return 20
    else:
        return 10


def make_pair(cardzero, cardone):
    if cardzero.id > cardone.id:
        lower_card = cardone
        upper_card = cardzero
    else:
        lower_card = cardzero
        upper_card = cardone
    p = Pair(
        id=lower_card.id + upper_card.id,
        lower_card=lower_card.id,
        upper_card=upper_card.id,
    )
    db.session.add(p)
    db.session.commit()
    return p


def find_pair(cardzero, cardone):
    if cardzero.id > cardone.id:
        lower_card = cardone
        upper_card = cardzero
    else:
        lower_card = cardzero
        upper_card = cardone
    p = Pair.query.filter_by(id=lower_card.id + upper_card.id).first()
    if p is None:
        p = make_pair(cardzero, cardone)
    return p
