from flask import Flask
from flask_restful import Api

from models import db

import resources

app = Flask(__name__)
app.config.from_object('default-config')
app.config.from_envvar('QUEUE_CONFIG', silent=True)
api = Api(app)

api.add_resource(resources.Queue, '/queue')

db.init_app(app)

if __name__ == '__main__':
    app.run()
