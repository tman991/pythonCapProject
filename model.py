"Models for custom car making app."
from database import db


class User(db.Model):  # type: ignore
    "A user."

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"



class Car(db.Model):  # type: ignore
    "A car."

    __tablename__ = "cars"

    car_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    user = db.relationship("User", backref="customizing")
    make = db.Column(db.String)
    year = db.Column(db.Integer)
    color = db.Column(db.String)
    seat_style = db.Column(db.String)
    wheel_count = db.Column(db.Integer)
    def __repr__(self):
        return f"<Car car_id={self.car_id} make={self.make} user={self.user_id}>"


class Buy_Request(db.Model):
    __tablename__ = "buy_request"
    request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    car_id = db.Column(db.Integer, db.ForeignKey(Car.car_id))
    requested_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    buy_price = db.Column(db.Integer)
    message = db.Column(db.String)

    def __repr__(self):
        return f"<Car car_id={self.car_id} make={self.make} user={self.user_id}>"