from flask_app import app
from flask import render_template, flash, redirect, request, session
from flask_app.models.log_reg import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration", methods=["POST"])
def register():

    if User.reg_valid(request.form):
        
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "confirm_pass": request.form["confirm_pass"],
            "password": pw_hash
        }

        user_id = User.save(data)
        session["user_id"] = user_id
        flash("User created")
        return redirect("/")
    else:
        return redirect("/")
    

@app.route("/login", methods=["POST"])
def login():
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect ("/")
    
    session["user_id"] = user_in_db.id

    return redirect("/success")

@app.route("/success")
def successful_login():
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect("/")

    return render_template("success.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!")
    return render_template("index.html")
