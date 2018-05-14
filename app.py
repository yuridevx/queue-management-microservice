from flask import Flask
from flask_restful import Api

from models import db

app = Flask(__name__)
app.config.from_object('default-config', silent=True)
app.config.from_envvar('QUEUE_CONFIG', silent=True)
api = Api(app)

db.init_app(app)

if __name__ == '__main__':
    app.run()
