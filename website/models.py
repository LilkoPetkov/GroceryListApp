from flask_login import UserMixin
from website import db, login_manager


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=70), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    items = db.relationship("Items", backref='owned_user', lazy="dynamic")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))