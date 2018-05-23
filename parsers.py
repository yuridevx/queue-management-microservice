from flask_restful import reqparse

get_request = reqparse.RequestParser()

get_request.add_argument('start', type=int, default=0)
get_request.add_argument('limit', type=int, default=100)

post_name = reqparse.RequestParser()

post_name.add_argument('name', type=str, required=True)
