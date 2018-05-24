import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_

import constants

db = SQLAlchemy()


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    lastTicketNumber = db.Column(db.Integer, default=0)

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    number = db.Column(db.Integer, default=0)

    queueId = db.Column(db.Integer, db.ForeignKey('queue.id', ondelete="CASCADE", onupdate="RESTRICT"))

    queue = db.relationship('Queue', backref="counters")

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def update_number(self):
        used_numbers = db.session.query(Counter.id, Counter.number).filter(Counter.queueId == self.queueId).all()

        excluded_numbers = []

        for id, number in used_numbers:
            if id == self.id:
                continue

            if number == 0:
                continue

            excluded_numbers.append(number)

        self.number = db.session.query(func.min(Ticket.number)).filter(
            (Ticket.queueId == self.queueId) & Ticket.number.notin_(excluded_numbers)
        ).scalar()

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

    queueId = db.Column(db.Integer, db.ForeignKey('queue.id', ondelete="CASCADE", onupdate="RESTRICT"))
    counterId = db.Column(db.Integer, db.ForeignKey('counter.id', ondelete="SET NULL", onupdate="RESTRICT"),
                          nullable=True)

    number = db.Column(db.Integer, default=0)

    counter = db.relationship('Counter', backref="tickets")
    queue = db.relationship('Queue', backref="tickets")

    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def pick_counter(self):
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
        numbers = [
            number for (number,) in
            db.session.query(Ticket.number).filter(
                (Ticket.number > 0) & (Ticket.queueId == self.queue.id)
            ).all()
        ]

        self.queue.lastTicketNumber = pick_number(numbers, self.queue.lastTicketNumber)
        self.number = self.queue.lastTicketNumber


def pick_number(numbers, start):
    overflow = False

    if start < 1:
        start = 1

    while start in numbers:

        if not overflow and start > constants.COUNTER_MAX:
            overflow = True
            start = 1
            continue

        start += 1

    return start
