from flask import Flask
from flask_restful import Api

import resources
from models import db

app = Flask(__name__)
app.config.from_object('default-config')
app.config.from_envvar('QUEUE_CONFIG', silent=True)
api = Api(app)

api.add_resource(resources.QueueCollection, '/queue')
api.add_resource(resources.QueueItem, '/queue/<int:queue_id>')

api.add_resource(resources.CounterCollection, '/queue/<int:queue_id>/counters')
api.add_resource(resources.CounterItem, '/queue/<int:queue_id>/counters/<int:counter_id>')

api.add_resource(resources.TicketCollection, '/queue/<int:queue_id>/tickets',
                 '/queue/<int:queue_id>/counters/<int:counter_id>/tickets')
api.add_resource(resources.TicketItem, '/queue/<int:queue_id>/tickets/<int:ticket_id>',
                 '/queue/<int:queue_id>/counters/<int:counter_id>/tickets/<int:ticket_id>')

db.init_app(app)

if __name__ == '__main__':
    app.run()
