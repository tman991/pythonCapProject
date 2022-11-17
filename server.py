from flask import Flask, render_template, request, flash, session, redirect 
from model import Car, User, Buy_Request
from database import db, connect_to_db
from jinja2 import StrictUndefined
import crud


app = Flask(__name__,
                static_url_path='', 
                static_folder='web/static'
            )

connect_to_db(app, db)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    "View homepage."
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    if user:
        return redirect("/cars")
    return render_template("home.html")

@app.route('/logout')
def logout():
    "Log a user out."
    session["user_email"] = ""
    return redirect("/")

@app.route('/register')
def register():
    "View registeration page."
    return render_template("register.html")

@app.route('/cars')
def user_cars():
    "View users cars"
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    if user is None:
        flash("You must log in to view cars.")
        return render_template("home.html")

    cars = crud.get_cars(user)
    return render_template("user_cars.html", cars=cars)

@app.route('/allcars')
def all_cars():
    "View all cars"
    cars = crud.get_all_cars()
    return render_template("all_cars.html", cars=cars)

@app.route('/allusers')
def all_users():
    "View all users"
    users = crud.get_users()
    return render_template("all_users.html", users=users)

@app.route("/cars/<car_id>")
def show_car(car_id):
    "Show details on a car."
    car = crud.get_car_by_id(car_id)
    return render_template("car_details.html", car=car)

@app.route("/users", methods=["POST"] )
def register_user():
    "Create new user"

    email = request.form.get("email")
    password = request.form.get("password")


    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create account. Try different email")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please log in.")

    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    "Process user login."

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/cars")


@app.route("/cars", methods=["POST"])
def add_car():
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("You must log in to add a car.")
        return redirect("/")
    user = crud.get_user_by_email(logged_in_email)
    style = request.form.get("style")
    wheels = int(request.form.get("wheel"))
    year = int(request.form.get("year"))
    make = request.form.get("make")
    color = request.form.get("color")
    car = Car(seat_style=style, year=year, make=make, color=color, wheel_count=wheels, user_id=user.user_id)
    db.session.add(car)
    db.session.commit()
    flash("Car Added successfully!")
    return redirect("/cars")

@app.route("/cars/delete/<car_id>", methods=["GET"])
def delete_car(car_id):
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("You must log in to add a car.")
        return redirect("/")
    user = crud.get_user_by_email(logged_in_email)
    Car.query.filter(Car.user_id == user.user_id).filter(car_id == Car.car_id).delete()
    db.session.commit()
    flash("Car Removed successfully!")
    return redirect("/cars")

@app.route("/requests", methods=["GET"])
def get_all_requests():
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        return ('You must be logged in', 403)   
    user = crud.get_user_by_email(logged_in_email)
    requests = Buy_Request.query.filter(Buy_Request.requested_id == user.user_id).all()
    return render_template("all_requests.html", requests=requests)

@app.route("/requests", methods=["POST"])
def make_request():
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        return ('You must be logged in', 403)   
    user = crud.get_user_by_email(logged_in_email)
    requestor_id = user.user_id
    message = request.form.get("message")
    buy_price = request.form.get("buy_price")
    car_id = request.form.get("car_id")
    requested_id = request.form.get("requested")

    if int(requestor_id) == int(requested_id):
        flash("Cannot request yourself")
        return redirect("/")      
    car = Buy_Request(message=message, car_id=car_id, requested_id=requested_id, buy_price=buy_price, requestor_id=requestor_id)
    db.session.add(car)
    #flash(requested_id, requestor_id)
    db.session.commit()
    flash("Requested successfully.")
    return redirect("/cars")


if __name__ == "__main__":
    app.run(debug=True)




