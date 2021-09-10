from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import bcrypt
import smtplib
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Configure and initialize SQLAlchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calories.db"
db = SQLAlchemy(app)

# Make a regular expression for validating an email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Create db models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    goal = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

# Home page
@app.route("/")
def index():
    # Calorie goal
    global goal
    if "user_id" in session:
        goal = Users.query.filter_by(id = session["user_id"]).first().goal
    else:
        goal = 0
    
    return render_template("index.html", goal=goal)

# Log in page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Calorie goal
    global goal
    if "user_id" in session:
        goal = Users.query.filter_by(id = session["user_id"]).first().goal
    else:
        goal = 0

    if request.method == "POST":

        # Obtain information from form
        name = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was sumbitted
        if not name:
            return render_template("login.html", error="The username field is required")
        name = name.strip()

        # Ensure password was sumbitted
        if not password:
            return render_template("login.html", error="The password field is required")
        password.strip()
        password_byte = password.encode("utf-8")

        # Ensure username exists and password is correct
        if (not Users.query.filter_by(name = name).all()) or bcrypt.checkpw(password_byte, Users.query.filter_by(name = name).first().password_hash) == False:
            return render_template("login.html", error="Invalid username or password")

        # Set session user id and goal
        session["user_id"] = (Users.query.filter_by(name=name).first()).id
        goal = Users.query.filter_by(id = session["user_id"]).first().goal

        # Redirect to the home page
        return redirect("/")
    else:
        return render_template("login.html", error=0)

# Sign up page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Calorie goal
    global goal
    if "user_id" in session:
        goal = Users.query.filter_by(id = session["user_id"]).first().goal
    else:
        goal = 0

    if request.method == "POST":
        
        # Obtain information from form
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Ensure username is valid and unique
        if not name:
            return render_template("signup.html", error="The username field is required")
        name = name.strip()
        if Users.query.filter_by(name = name).all():
            return render_template("signup.html", error="This username is taken")

        # Ensure email is valid and unique
        if not email:
            return render_template("signup.html", error="The email field is required")
        email = email.strip()
        if not re.fullmatch(regex, email):
            return render_template("signup.html", error="Please enter a valid email")
        if Users.query.filter_by(email = email).all():
            return render_template("signup.html", error="This email is taken")

        # Ensure password and confirmation are valid
        if not password:
            return render_template("signup.html", error="The password field is required")
        password = password.strip()
        if not confirmation:
            return render_template("signup.html", error="The confirmation field is required")
        confirmation = confirmation.strip()

        password_byte = password.encode("utf-8")
        confirmation_byte = confirmation.encode("utf-8")
        hashed = bcrypt.hashpw(password_byte, bcrypt.gensalt())

        # Ensure the password is long enough
        if len(password) < 8:
            return render_template("signup.html", error="Password is too short")
        # Ensure the password has a number
        check = False
        for character in password:
            if character.isnumeric():
                check = True
        if check == False:
            return render_template("signup.html", error="The password should have at least one digit (0-9)")      

        # Ensure password and confirmation match
        if password != confirmation:
            return render_template("signup.html", error="Passwords do not match")

        # Add user details to database
        user = Users(name=name, email=email, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        # Set session user id and goal
        session["user_id"] = (Users.query.filter_by(name=name).first()).id
        goal = Users.query.filter_by(id = session["user_id"]).first().goal

        # Send email confirmation
        SUBJECT = "Registration Successful"
        TEXT = "Welcome to TrackCal!\nAccount details:\nUSERNAME: " + name + "\nPASSWORD: " + password
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.environ.get("EMAIL"), os.environ.get("EMAIL_PASSWORD"))
        server.sendmail(os.environ.get("EMAIL"), email, message)
        server.quit()

        # Redirect to the home page
        return redirect("/")

    else:
        return render_template("signup.html", error=0)

# Log out page
@app.route("/logout")
def logout():
    # Calorie goal
    global goal
    if "user_id" in session:
        goal = Users.query.filter_by(id = session["user_id"]).first().goal
    else:
        goal = 0

    session.clear()
    return render_template("login.html", error=0)

# BMR calculator page
@app.route("/bmrcalculator", methods=["GET", "POST"])
def bmrcalculator():
    # Calorie goal
    global goal
    if "user_id" in session:
        goal = Users.query.filter_by(id = session["user_id"]).first().goal
    else:
        goal = 0

    if request.method == "POST":
        
        # Obtain information from form
        age = request.form.get("age")
        height = request.form.get("height")
        weight = request.form.get("weight")
        gender = request.form.get("gender")

        # Ensure age is valid
        if not age:
            return render_template("bmrcalculator.html", bmr=0, error="The age field is required", goal=goal)
        age = age.strip()
        if int(age) < 15 or int(age) > 80:
            return render_template("bmrcalculator.html", bmr=0, error="Invalid age", goal=goale)

        # Ensure height, weight and gender are valid
        if not height:
            return render_template("bmrcalculator.html", bmr=0, error="The height field is required", goal=goal)
        if int(height) < 0:
            return render_template("bmrcalculator.html", bmr=0, error="Invalid height", goal=goal)
        height = height.strip()
        if not weight:
            return render_template("bmrcalculator.html", bmr=0, error="The weight field is required", goal=goal)
        if int(weight) < 0:
            return render_template("bmrcalculator.html", bmr=0, error="Invalid weight", goal=goal)
        weight = weight.strip()
        if not gender:
            return render_template("bmrcalculator.html", bmr=0, error="Select a gender", goal=goal)
        gender = gender.strip()

        # Calculate BMR
        bmr = (10 * int(weight)) + (6.25 * int(height)) - (5 * int(age))
        if gender == "male":
            bmr += 5
        else:
            bmr -= 161

        return render_template("bmrcalculator.html", bmr=bmr, error=0, goal=goal)

    else:
        return render_template("bmrcalculator.html", bmr=0, error=0, goal=goal)

# Calorie tracker page
@app.route("/calories", methods=["GET", "POST"])
def calories():
    case = 0

    # Calorie goal
    global goal
    if "user_id" in session:
        goal = Users.query.filter_by(id = session["user_id"]).first().goal
    else:
        goal = 0

    date = datetime.now()

    if request.method == "POST":

        # If calorie goal is updated
        if request.form.get("find"):

            case = 1

            # Obtain information from the form
            bmr = request.form.get("bmr")
            form_goal = request.form.get("goal")
            amount = request.form.get("amount")

            # Ensure BMR is valid
            if not bmr:
                return render_template("calories.html", goal=goal, error="The BMR field is required", date=date, case=case, progress=-1)
            if int(bmr) < 0:
                return render_template("calories.html", goal=goal, error="Invalid BMR", date=date, case=case, progress=-1)
            bmr = bmr.strip()

            # Ensure goal is valid
            if not form_goal:
                return render_template("calories.html", goal=goal, error="Select a goal", date=date, case=case, progress=-1)

            # Ensure amount is valid
            if not amount:
                return render_template("calories.html", goal=goal, error="Select an amount", date=date, case=case, progress=-1)

            if form_goal == "lose":
                factor = -1
            else:
                factor = 1

            goal = (float(bmr) * 1.375) + (factor * ((7700 * float(amount)) / 7))
            goal = int(goal)

            user = Users.query.filter_by(id = session["user_id"]).first()
            user.goal = goal
            db.session.commit()

            return render_template("calories.html", goal=goal, error=0, date=date, case=case, progress=-1)

        case = 2

        if goal == 0:
            return render_template("calories.html", goal=goal, error="Calorie goal needs to be set first", date=date, case=case, progress=-1)

        # Update and view functionality

        # Obtain information from form
        day = request.form.get("date")
        month = request.form.get("month")
        year = request.form.get("year")
        calories = request.form.get("calories")

        # Ensure date is valid
        if not day or not month or not year:
            return render_template("calories.html", goal=goal, error="The date fields are required", date=date, case=case, progress=-1)

        try:
            testDate = datetime(int(year), int(month), int(day))
        except ValueError:
            return render_template("calories.html", goal=goal, error="Invalid date", date=date, case=case, progress=-1)

        if testDate > datetime.now():
            return render_template("calories.html", goal=goal, error="Invalid date", date=date, case=case, progress=-1)

        day = int(day.strip())
        month = int(month.strip())
        year = int(year.strip())

        # Update calorie intake
        if request.form.get("add") or request.form.get("remove"):

            # Ensure calories are valid
            if not calories:    
                return render_template("calories.html", goal=goal, error="The calories field is required", date=date, case=case, progress=-1)
            if int(calories) < 0:
                return render_template("calories.html", goal=goal, error="Invalid calories", date=date, case=case, progress=-1)
            calories = int(calories.strip())

            # Check operation type
            if request.form.get("add"):
                factor = 1
            else:
                factor = -1

            # Update calories
            current_day = Tracker.query.filter_by(user_id = session["user_id"], date = day, month = month, year = year).first()

            if current_day:
                current_day.calories += (factor * calories)
                if current_day.calories < 0:
                    current_day.calories = 0
                db.session.commit()

            else:
                if request.form.get("remove"):
                    calories = 0
                record = Tracker(user_id = session["user_id"], date = day, month = month, year = year, calories = calories)
                db.session.add(record)
                db.session.commit()

        # View progress
        if not Tracker.query.filter_by(user_id = session["user_id"], date = day, month = month, year = year).first():
            db.session.add(Tracker(user_id = session["user_id"], date = day, month = month, year = year, calories = 0))
            db.session.commit()

        new_day = Tracker.query.filter_by(user_id = session["user_id"], date = day, month = month, year = year).first()

        progress = int((new_day.calories * 100)/goal)
        if progress > 100:
            progress = 100
        
        return render_template("calories.html", goal=goal, error=0, date=date, case=case, progress=progress, cal_done=new_day.calories)

    else:
        return render_template("calories.html", goal=goal, error=0, date=date, case=case, progress=-1)

# Information page
@app.route("/information")
def information():
    # Calorie goal
    global goal
    if "user_id" in session:
        goal = Users.query.filter_by(id = session["user_id"]).first().goal
    else:
        goal = 0

    return render_template("information.html", goal=goal)

# Donate page
@app.route("/donate")
def donate():
    # Calorie goal
    global goal
    if "user_id" in session:
        goal = Users.query.filter_by(id = session["user_id"]).first().goal
    else:
        goal = 0

    return render_template("donate.html", goal=goal)

# Paypal
@app.route("/paypal")
def paypal():
    paypal = os.environ.get("PAYPAL_LINK")
    return redirect(paypal)

if __name__ == "__main__":
    app.run(debug=True)