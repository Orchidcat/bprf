from flask import Blueprint, render_template

second1 = Blueprint("second", __name__, static_folder="static", template_folder="templates")

@second1.route("/home")
@second1.route("/")
def home():
    return render_template("home.html")

@second1.route("/test")
def test():
    return "<h1>Admin test</h1>"
