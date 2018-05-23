import models
from app import app

models.db.init_app(app)

with app.app_context():
    models.db.drop_all()
    models.db.create_all()

    q1 = models.Queue(name='First queue')
    q2 = models.Queue(name='Second queue')

    c11 = models.Counter(name='First queue, counter 1', queue=q1)
    c12 = models.Counter(name='First queue, counter 2', queue=q1)

    c21 = models.Counter(name='First queue, counter 1', queue=q2)
    c22 = models.Counter(name='First queue, counter 2', queue=q2)

    models.db.session.add_all([q1, q2, c11, c12, c21, c22])

    t11 = models.Ticket(queue=q1)
    t11.pick_counter()
    t11.assign_number()

    models.db.session.add(t11)

    t12 = models.Ticket(queue=q1)
    t12.pick_counter()
    t12.assign_number()

    models.db.session.add(t12)

    t13 = models.Ticket(queue=q1)
    t13.pick_counter()
    t13.assign_number()

    models.db.session.add(t13)

    t21 = models.Ticket(queue=q2)
    t21.pick_counter()
    t21.assign_number()

    models.db.session.add(t21)

    t22 = models.Ticket(queue=q2)
    t22.pick_counter()
    t22.assign_number()

    models.db.session.add(t22)

    t23 = models.Ticket(queue=q2)
    t23.pick_counter()
    t23.assign_number()

    models.db.session.add(t23)

    models.db.session.commit()

    c11.update_number()
    models.db.session.commit()

    c12.update_number()
    models.db.session.commit()

    c21.update_number()
    models.db.session.commit()

    c22.update_number()
    models.db.session.commit()

