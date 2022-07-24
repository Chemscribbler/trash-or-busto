from unicodedata import name
from requests import get
from sqlalchemy import exc
from dzmz.models import Card


def build_card_db(db):
    request = get("https://netrunnerdb.com/api/2.0/public/cards")

    for card in request.json()["data"]:
        if card["pack_code"] != "draft" and card["pack_code"] != "tdc":
            try:
                if card["type_code"] == "identity":
                    c = Card(
                        nrdb_key=card["code"],
                        name=card["title"],
                        faction=card["faction_code"],
                        side=card["side_code"],
                        type=card["type_code"],
                    )
                elif card["type_code"] == "agenda":
                    c = Card(
                        nrdb_key=card["code"],
                        name=card["title"],
                        faction=card["faction_code"],
                        side=card["side_code"],
                        cost=card["advancement_cost"],
                        type=card["type_code"],
                    )
                else:
                    c = Card(
                        nrdb_key=card["code"],
                        name=card["title"],
                        faction=card["faction_code"],
                        side=card["side_code"],
                        cost=card["cost"],
                        type=card["type_code"],
                    )
                db.session.add(c)
                db.session.commit()
            except exc.IntegrityError as e:
                # print(f"Card {card['title']} was already imported")
                db.session.rollback()
                update_nrdb_key(c, db=db)
                # break


def update_nrdb_key(card: Card, db):
    q = Card.query.filter_by(name=card.name).first()
    q.nrdb_key = card.nrdb_key
    db.session.commit()
