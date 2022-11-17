import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_to_db(app, db):
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(os.getcwd(), 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print("Connected to db!")