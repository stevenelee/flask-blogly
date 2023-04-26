"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
       db.Integer,
       primary_key=True,
       autoincrement=True)

    first_name = db.Column(
       db.String(50),
       nullable=False)

    last_name = db.Column(
       db.String(50),
       nullable=False)

    image_url = db.Column(
        db.String(255),
        nullable=False,
        default="https://i.pinimg.com/550x/18/b9/ff/18b9ffb2a8a791d50213a9d595c4dd52.jpg"
    )
