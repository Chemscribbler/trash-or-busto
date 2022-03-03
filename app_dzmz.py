from dzmz import app, db
from dzmz.models import Card, Pair
from dzmz.card_builder import build_card_db


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Card": Card, "Pair": Pair, "build_card_db": build_card_db}


if __name__ == "__main__":
    app.run(debug=False)
