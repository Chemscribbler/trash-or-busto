from dzmz import app, db
from dzmz.models import Card
from dzmz.card_builder import build_card_db


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Card": Card, "build_card_db": build_card_db}
