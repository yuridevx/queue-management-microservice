import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_

db = SQLAlchemy()


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    ticketNumber = db.Column(db.Integer, default=0)

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    number = db.Column(db.Integer, default=0)

    queueId = db.Column(db.Integer, db.ForeignKey('queue.id'))

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def update_number(self):
        pass

    def assign_tickets(self):
        is_zero_tickets = db.session.query(
            func.count('*')
        ).select_from(
            Ticket
        ).filter(
            Ticket.counterId == self.id
        ).limit(1).scalar() == 0

        if is_zero_tickets:
            no_counter_ticket = Ticket.query.filter(
                and_(Ticket.counterId == None, Ticket.queueId == self.queueId)
            ).first()
            if no_counter_ticket:
                no_counter_ticket.counterId = self.id


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    queueId = db.Column(db.Integer, db.ForeignKey('queue.id'))
    counterId = db.Column(db.Integer, db.ForeignKey('counter.id'), nullable=True)

    number = db.Column(db.Integer, default=0)

    counter = db.relationship('Counter', backref="tickets")
    queue = db.relationship('Queue', backref="tickets")

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def ensure_in_counter(self):
        if self.counter is not None:
            return

        counter = db.session.query(
            Counter
        ).outerjoin(
            Ticket
        ).filter(
            Ticket.id == None
        ).first()

        self.counter = counter

    def assign_number(self):
        pass
