from flask_restful import Resource, marshal_with, abort
from sqlalchemy import and_

import marshal
import models
import parsers

class QueueCollection(Resource):
    @marshal_with(marshal.queue_get)
    def get(self):
        args = parsers.get_request.parse_args()
        queues = models.Queue.query.offset(args['start']).limit(args['limit']).all()

        res = {
            'start': args['start'],
            'limit': args['limit'],
            'count': len(queues),
            'results': queues
        }

        return res, 200 if len(queues) > 0 else 204

    @marshal_with(marshal.queue)
    def post(self):
        args = parsers.post_name.parse_args()
        queue = models.Queue(name=args['name'])
        models.db.session.add(queue)
        models.db.session.commit()

        return queue, 201


class QueueItem(Resource):
    @staticmethod
    def get_queue(queueId):
        queue = models.Queue.query.filter(models.Queue.id == queueId).first()

        if not queue:
            abort(404)

        return queue

    @marshal_with(marshal.queue)
    def get(self, queueId):
        return self.get_queue(queueId)

    @marshal_with(marshal.queue)
    def put(self, queueId):
        args = parsers.post_name.parse_args()

        queue = self.get_queue(queueId)
        queue.name = args['name']

        models.db.session.commit()

        return queue

    def delete(self, queueId):
        queue = self.get_queue(queueId)

        models.db.session.delete(queue)
        models.db.session.commit()


class CounterCollection(Resource):
    @marshal_with(marshal.counters_get)
    def get(self, queueId):
        args = parsers.get_request.parse_args()

        counters = models.Counter.query.filter(
            models.Counter.queueId == queueId
        ).offset(
            args['start']
        ).limit(
            args['limit']
        ).all()

        res = {
            'start': args['start'],
            'limit': args['limit'],
            'count': len(counters),
            'results': counters
        }

        return res, 200 if len(counters) > 0 else 204

    @marshal_with(marshal.counter)
    def post(self, queueId):
        args = parsers.post_name.parse_args()

        counter = models.Counter(name=args['name'])
        counter.queueId = queueId

        models.db.session.add(counter)
        models.db.session.commit()

        return counter


class CounterItem(Resource):

    @staticmethod
    def get_counter(counterId):
        counter = models.Counter.query.filter(models.Counter.id == counterId).first()

        if not counter:
            abort(404)

        return counter

    @marshal_with(marshal.counter)
    def get(self, counterId, queueId):
        return self.get_counter(counterId)

    @marshal_with(marshal.counter)
    def put(self, counterId, queueId):
        args = parsers.post_name.parse_args()

        counter = self.get_counter(counterId)
        counter.name = args['name']

        models.db.session.commit()

        return counter

    def delete(self, counterId, queueId):
        counter = self.get_counter(counterId)

        models.db.session.delete(counter)
        models.db.session.commit()


class TicketCollection(Resource):
    @marshal_with(marshal.ticket_get)
    def get(self, queueId, counterId=None):
        args = parsers.get_request.parse_args()

        counters = models.Ticket.query.filter(
            and_(
                models.Ticket.queueId == queueId,
                models.Ticket.counterId == counterId
            )
        ).offset(
            args['start']
        ).limit(
            args['limit']
        ).all()

        res = {
            'start': args['start'],
            'limit': args['limit'],
            'count': len(counters),
            'results': counters
        }

        return res, 200 if len(counters) > 0 else 204

    @marshal_with(marshal.ticket)
    def post(self, queueId, counterId=None):
        ticket = models.Ticket(queueId=queueId, counterId=counterId)

        models.db.session.add(ticket)

        ticket.ensure_in_counter()
        ticket.assign_number()
        ticket.counter.update_number()

        models.db.session.commit()

        return ticket


class TicketItem(Resource):

    @staticmethod
    def get_ticket(ticketId):
        counter = models.Ticket.query.filter(models.Ticket.id == ticketId).first()

        if not counter:
            abort(404)

        return counter

    @marshal_with(marshal.ticket)
    def get(self, queueId, ticketId, counterId=None):
        return self.get_ticket(ticketId)

    def delete(self, queueId, ticketId, counterId=None):
        ticket = self.get_ticket(ticketId)

        counter = ticket.counter

        models.db.session.delete(ticket)

        counter.assign_tickets()

        models.db.session.commit()
