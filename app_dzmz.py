from dzmz import app, db
from dzmz.models import Card


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Card": Card}
