from dzmz import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nrdb_key = db.Column(db.String, nullable=False)
    name = db.Column(db.String, index=True, unique=True, nullable=False)
    faction = db.Column(db.String, nullable=False)
    side = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer)
    type = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, default=1500)
    num_ratings = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Card {self.name}>"
