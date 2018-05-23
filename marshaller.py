from flask_restful import fields

queue = {
    'id': fields.Integer,
    'name': fields.String,
    'createdAt': fields.DateTime(dt_format='iso8601'),
    'updatedAt': fields.DateTime(dt_format='iso8601'),
}

queue_get = {
    'start': fields.Integer,
    'limit': fields.Integer,
    'count': fields.Integer,
    'results': fields.List(fields.Nested(queue))
}

counter = {
    'id': fields.Integer,
    'name': fields.String,
    'number': fields.Integer,
    'createdAt': fields.DateTime(dt_format='iso8601'),
    'updatedAt': fields.DateTime(dt_format='iso8601'),
}

counters_get = {
    'start': fields.Integer,
    'limit': fields.Integer,
    'count': fields.Integer,
    'results': fields.List(fields.Nested(counter))
}

ticket = {
    'id': fields.Integer,
    'number': fields.Integer,
    'queueId': fields.Integer,
    'counterId': fields.Integer,
    'createdAt': fields.DateTime(dt_format='iso8601'),
    'updatedAt': fields.DateTime(dt_format='iso8601'),
}

ticket_get = {
    'start': fields.Integer,
    'limit': fields.Integer,
    'count': fields.Integer,
    'results': fields.List(fields.Nested(ticket))
}
