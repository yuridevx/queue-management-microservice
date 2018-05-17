from flask_restful import Resource, reqparse, fields, marshal_with, abort
from sqlalchemy import and_, func

import models

get_parser = reqparse.RequestParser()

get_parser.add_argument('start', type=int, default=0)
get_parser.add_argument('limit', type=int, default=100)

post_queue_parser = reqparse.RequestParser()

post_queue_parser.add_argument('name', type=str, required=True)

queue_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'createdAt': fields.DateTime(dt_format='iso8601'),
    'updatedAt': fields.DateTime(dt_format='iso8601'),
}

queue_post_fields = {
    'name': fields.String
}

queue_get_fields = {
    'start': fields.Integer,
    'limit': fields.Integer,
    'count': fields.Integer,
    'results': fields.List(fields.Nested(queue_fields))
}


class QueueCollection(Resource):
    @marshal_with(queue_get_fields)
    def get(self):
        args = get_parser.parse_args()
        queues = models.Queue.query.offset(args['start']).limit(args['limit']).all()

        res = {
            'start': args['start'],
            'limit': args['limit'],
            'count': len(queues),
            'results': queues
        }

        return res, 200 if len(queues) > 0 else 204

    @marshal_with(queue_fields)
    def post(self):
        args = post_queue_parser.parse_args()
        queue = models.Queue(name=args['name'])
        models.db.session.add(queue)
        models.db.session.commit()

        return queue, 201


class QueueItem(Resource):
    @staticmethod
    def get_queue(queue_id):
        queue = models.Queue.query.filter(models.Queue.id == queue_id).first()

        if not queue:
            abort(404)

        return queue

    @marshal_with(queue_fields)
    def get(self, queue_id):
        return self.get_queue(queue_id)

    @marshal_with(queue_fields)
    def put(self, queue_id):
        args = post_queue_parser.parse_args()

        queue = self.get_queue(queue_id)
        queue.name = args['name']

        models.db.session.commit()

        return queue

    def delete(self, queue_id):
        queue = self.get_queue(queue_id)

        models.db.session.delete(queue)
        models.db.session.commit()


counter_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'number': fields.Integer,
    'createdAt': fields.DateTime(dt_format='iso8601'),
    'updatedAt': fields.DateTime(dt_format='iso8601'),
}

counters_fields = {
    'start': fields.Integer,
    'limit': fields.Integer,
    'count': fields.Integer,
    'results': fields.List(fields.Nested(counter_fields))
}

post_counter_parser = reqparse.RequestParser()
post_counter_parser.add_argument('name', type=str, required=True)
post_counter_parser.add_argument('number', type=int, required=True)


class CounterCollection(Resource):
    @marshal_with(counters_fields)
    def get(self, queue_id):
        args = get_parser.parse_args()

        counters = models.Counter.query.filter(models.Counter.queue_id == queue_id).offset(args['start']).limit(
            args['limit']).all()

        res = {
            'start': args['start'],
            'limit': args['limit'],
            'count': len(counters),
            'results': counters
        }

        return res, 200 if len(counters) > 0 else 204

    @marshal_with(counter_fields)
    def post(self, queue_id):
        args = post_counter_parser.parse_args()

        counter = models.Counter(name=args['name'], number=args['number'])
        counter.queue_id = queue_id

        models.db.session.add(counter)
        models.db.session.commit()

        return counter


class CounterItem(Resource):

    @staticmethod
    def get_counter(counter_id):
        counter = models.Counter.query.filter(models.Counter.id == counter_id).first()

        if not counter:
            abort(404)

        return counter

    @marshal_with(counter_fields)
    def get(self, counter_id, queue_id):
        return self.get_counter(counter_id)

    @marshal_with(counter_fields)
    def put(self, counter_id, queue_id):
        args = post_counter_parser.parse_args()

        counter = self.get_counter(counter_id)
        counter.name = args['name']
        counter.number = args['number']

        models.db.session.commit()

        return counter

    def delete(self, counter_id, queue_id):
        counter = self.get_counter(counter_id)

        models.db.session.delete(counter)
        models.db.session.commit()


ticket_fields = {
    'id': fields.Integer,
    'queue_id': fields.Integer,
    'counter_id': fields.Integer,
    'createdAt': fields.DateTime(dt_format='iso8601'),
    'updatedAt': fields.DateTime(dt_format='iso8601'),
}

tickets_fields = {
    'start': fields.Integer,
    'limit': fields.Integer,
    'count': fields.Integer,
    'results': fields.List(fields.Nested(ticket_fields))
}


class TicketCollection(Resource):
    @marshal_with(tickets_fields)
    def get(self, queue_id, counter_id=None):
        args = get_parser.parse_args()

        counters = models.Ticket.query.filter(
            and_(models.Ticket.queue_id == queue_id, models.Ticket.counter_id == counter_id)).offset(
            args['start']).limit(args['limit']).all()

        res = {
            'start': args['start'],
            'limit': args['limit'],
            'count': len(counters),
            'results': counters
        }

        return res, 200 if len(counters) > 0 else 204

    @marshal_with(ticket_fields)
    def post(self, queue_id, counter_id=None):
        ticket = models.Ticket(queue_id=queue_id, counter_id=counter_id)

        models.db.session.add(ticket)

        if counter_id is None:
            self.fill_to_counter(ticket)

        models.db.session.commit()

        return ticket

    def fill_to_counter(self, ticket):
        counter_id = models.db.session.query(models.Counter.id).outerjoin(models.Ticket).filter(
            models.Ticket.id == None).limit(1).scalar()

        ticket.counter_id = counter_id


class TicketItem(Resource):

    @staticmethod
    def get_ticket(ticket_id):
        counter = models.Ticket.query.filter(models.Ticket.id == ticket_id).first()

        if not counter:
            abort(404)

        return counter

    @marshal_with(ticket_fields)
    def get(self, queue_id, ticket_id, counter_id=None):
        return self.get_ticket(ticket_id)

    @marshal_with(ticket_fields)
    def put(self, queue_id, ticket_id, counter_id=None):
        ticket = self.get_ticket(ticket_id)

        models.db.session.commit()

        return ticket

    def delete(self, queue_id, ticket_id, counter_id=None):
        ticket = self.get_ticket(ticket_id)

        queue_id = ticket.queue_id
        counter_id = ticket.counter_id

        models.db.session.delete(ticket)

        if counter_id:
            self.refresh_counter(counter_id, queue_id)

        models.db.session.commit()

    @staticmethod
    def refresh_counter(counter_id, queue_id):
        is_zero_tickets = models.db.session.query(func.count('*')).select_from(models.Ticket).filter(
            models.Ticket.counter_id == counter_id).limit(1).scalar() == 0

        if is_zero_tickets:
            free_ticket = models.Ticket.query.filter(
                and_(models.Ticket.counter_id == None, models.Ticket.queue_id == queue_id)).first()
            if free_ticket:
                free_ticket.counter_id = counter_id
