"""Models for Pixly app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# DEFAULT_IMAGE = 'https://tinyurl.com/demo-cupcake'

def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)

class Image(db.Model):
    """Class for a cupcake."""

    __tablename__ = "images"

    image_id = db.Column(
        db.String(200),
        primary_key=True,
    )

    filename = db.Column(
        db.String(100),
        nullable=False,
    )

    file_extension = db.Column(
        db.String(10),
        nullable=False,
    )

    make = db.Column(
        db.String(50),
        nullable=True
    )

    model = db.Column(
        db.String(50),
        nullable=True
    )