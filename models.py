"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = 'https://tinyurl.com/demo-cupcake'

def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """Class for a cupcake."""

    __tablename__ = "cupcakes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    flavor = db.Column(
        db.String(50),
        nullable=False,
    )

    size = db.Column(
        db.String(50),
        nullable=False,
    )

    rating = db.Column(
        db.Integer,
        nullable=False,
    )

    image = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE,
    )

    def serialize(self):
        """Serialize to a dictionary"""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }
