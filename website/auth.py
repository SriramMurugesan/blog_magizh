from flask import Blueprint,render_template

auth= Blueprint("auth", __name__) 


@auth.route("/Login")
def login():
    return "Login"


@auth.route("/sign-up")
def sign_up():
    return "Sign Up"

@auth.route("/logout")
def logout():
    return "Logout"

