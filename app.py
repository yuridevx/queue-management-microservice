from flask import Flask
from flask_restful import Api

import resources
from models import db

app = Flask(__name__)
app.config.from_object('default-config')
app.config.from_envvar('QUEUE_CONFIG', silent=True)
api = Api(app)

api.add_resource(resources.QueueCollection, '/queue')
api.add_resource(resources.QueueItem, '/queue/<int:queueId>')

api.add_resource(resources.CounterCollection, '/queue/<int:queueId>/counters')
api.add_resource(resources.CounterItem, '/queue/<int:queueId>/counters/<int:counterId>')

api.add_resource(resources.TicketCollection, '/queue/<int:queueId>/tickets',
                 '/queue/<int:queueId>/counters/<int:counterId>/tickets')
api.add_resource(resources.TicketItem, '/queue/<int:queueId>/tickets/<int:ticketId>',
                 '/queue/<int:queueId>/counters/<int:counterId>/tickets/<int:ticketId>')

db.init_app(app)

if __name__ == '__main__':
    app.run()
