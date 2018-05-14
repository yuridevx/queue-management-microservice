from flask_restful import Resource, reqparse, fields, marshal_with

import models

parser = reqparse.RequestParser()

parser.add_argument('start', type=int, default=0)
parser.add_argument('limit', type=int, default=100)

queue_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'createdAt': fields.DateTime(),
    'updatedAt': fields.DateTime(),
}

get_fields = {
    'start': fields.Integer,
    'limit': fields.Integer,
    'count': fields.Integer,
    'results': fields.List(fields.Nested(queue_fields))
}


class Queue(Resource):
    @marshal_with(get_fields)
    def get(self):
        args = parser.parse_args()
        queues = models.Queue.query().offset(args['start']).limit(args['limit']).all()

        res = {
            'start': args['start'],
            'limit': args['limit'],
            'count': len(queues),
            'results': queues
        }

        return res, 200 if len(queues) > 0 else 204
