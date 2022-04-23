from app import app
from flask import render_template, request, redirect
import messages, users
from db import db

@app.route("/")
def index():
    listing = messages.get_areas()
    return render_template("index.html",areas=listing)

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

@app.route("/areas/<int:id>")
def areas(areaid):
    name = messages.get_area_name(id)
    threads = message.get_threads(id)
    return render_template("areas.html", threads=threads, area_name=name, area_id=areaid)

@app.route("/thread/<int:id>")
def thread(threadid):
    messages1 = messages.get_messages(id)
    header = messages.get_header(id)
    return render_template("thread.html", messages=messages1, thread_id=threadid, header=header)

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

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    sql = "SELECT id, content FROM messages WHERE content LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    listing = result.fetchall()
    return render_templat("result.html", messages1=listing)