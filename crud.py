"CRUD operations."

from model import User, Car
from database import db, connect_to_db


def create_user(email, password):
    "Create and return a new user."

    user = User(email=email, password=password)

    return user

def create_car(email, password):
    "Create and return a new user."

    user = User(email=email, password=password)

    return user
    
def get_users():
    "Return all users."

    return User.query.all()


def get_user_by_id(user_id):
    "Return a user by primary key."

    return User.query.get(user_id)

def get_user_by_email(email):
    "Return a user by email."

    return User.query.filter(User.email == email).first()


def create_car(make, year):
    "Create and return a new car."

    car = Car(
        make=make,
        year=year,
    )

    return car
    

def get_cars(user):
    "Returns all cars."
    return Car.query.filter(Car.user_id == user.user_id).all()

def get_all_cars():
    return Car.query.all()

def get_car_by_id(car_id):
    "Return car by primary key."

    return Car.query.get(car_id)



if __name__ == "__main__":
    from server import app

    connect_to_db(app)
