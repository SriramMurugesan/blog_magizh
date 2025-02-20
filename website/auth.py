from flask import Blueprint,render_template, redirect, url_for, request
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

auth= Blueprint("auth", __name__) 


@auth.route("/login",methods=["GET","POST"])
def login():
    email= request.form.get("email")
    password= request.form.get("password")
    return render_template("login.html")


@auth.route("/sign-up",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        username= request.form.get("username")
        email= request.form.get("email")
        password1= request.form.get("password1")
        password2= request.form.get("password2")

        email_exists= User.query.filter_by(email=email).first()
        username_exists= User.query.filter_by(username=username).first()
    
        if email_exists:
            flash("Email already exists",category="error")
        elif username_exists:
            flash("Username already exists",category="error")
        elif password1 != password2:
            flash("Passwords do not match",category="error")
        elif len(username)<2:
            flash("Username is too short",category="error")
        elif len(email)<4:
            flash("Email must be at least 4 characters",category="error")
        elif len(password1)<6:
            flash("Password must be at least 7 characters",category="error")
        else:
            new_user= User(email=email,username=username,password=generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created",category="success")
            return redirect(url_for("views.home"))

        return render_template("signup.html")

@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))