import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    number = db.Column(db.Integer)

    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'))

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'))
    counter_id = db.Column(db.Integer, db.ForeignKey('counter.id'), nullable=True)

    counter = db.relationship('Counter', backref="tickets")
    queue = db.relationship('Queue', backref="tickets")

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
