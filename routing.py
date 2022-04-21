from app import app
from flask import render_template, request, redirect
import messages, users

@app.route("/")
def index():
    listing = messages.get_list()
    return render_template("index.html",messages1=listing)

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", errormsg="Viestin lähetys ei toiminut")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", errormsg="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", errormsg="Salasanat eroavat toisistaan")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", errormsg="Rekisteröinti ei onnistunut")  
