from datetime import datetime
from . import db


class BaseTable(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)
    delete_at = db.Column(db.DateTime, nullable=True)


class User(BaseTable):
    __tablename__ = 'users'

    nickname = db.Column(db.String(30), unique=True, nullable=False)


class Message(BaseTable):
    __tablename__ = 'messages'

    text = db.Column(db.String(50), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(
        'User',
        backref='messages',
        lazy='joined'
    )


db.create_all()
