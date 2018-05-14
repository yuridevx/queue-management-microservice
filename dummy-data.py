import models
from app import app

models.db.init_app(app)

with app.app_context():
    models.db.drop_all()
    models.db.create_all()

    q1 = models.Queue(name='Cool')
    q2 = models.Queue(name='Whool')

    models.db.session.add(q1)
    models.db.session.add(q2)
    models.db.session.commit()
