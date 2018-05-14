from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
