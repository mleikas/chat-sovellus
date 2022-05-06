from app import app
from flask import render_template, session, request, redirect, abort
import messages, users
from db import db

@app.route("/")
def index():
    listing = messages.get_areas()
    return render_template("index.html",areas=listing)

@app.route("/send", methods=["POST"])
def send():
    if request.form["csrf_token"] != (session["csrf_token"]):
        abort(403)
    content = request.form["content"]
    thread_id = request.form["thread_id"]
    if messages.send(content, thread_id):
        return redirect("/thread/"+str(thread_id))
    else:
        return render_template("error.html", errormsg="Viestin lähetys ei toiminut")

@app.route("/areas/<int:id>")
def areas(id):
    name = messages.get_area_name(id)
    threads = messages.get_threads(id)
    return render_template("areas.html", threads=threads, area_name=name, area_id=id)

@app.route("/thread/<int:id>")
def thread(id):
    messages1 = messages.get_list(id)
    header = messages.get_header(id)
    return render_template("thread.html", messages=messages1, thread_id=id, header=header)

@app.route("/make_thread", methods=["POST"])
def make_thread():
    if request.form["csrf_token"] != (session["csrf_token"]):
        abort(403)
    thread_name = request.form["thread_name"]
    content = request.form["content"]
    area_id = request.form["area_id"]
    post_thread = messages.make_thread(thread_name, content, area_id)
    if post_thread == False:
        return render_template("error.html", errormsg="Tarkista syötteet")
    return redirect("/areas/"+str(area_id))

@app.route("/delete", methods=["POST"])
def delete():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    message_id = request.form["message_id"]
    user_id = int(request.form["user_id"])
    thread_id = request.form["thread_id"]
    print(user_id)
    if session["user_id"] == user_id:
        delete_message = messages.delete(message_id)
    if delete_message == False:
        return render_template("error.html", errormsg="Viestin poistaminen epäonnistui")
    return redirect("/thread/"+str(thread_id))

@app.route("/delete_threads", methods=["POST"])
def delete_threads():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    area_id = request.form["area_id"]
    thread_id = request.form["thread_id"]

    if user.admin() == True:
        messages.delete_threads(thread_id)
    
    return redirect("/areas/"+str(area_id))

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

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    sql = "SELECT I.id, U.id, I.content, I.sent_at, I.thread_message AS users_id FROM users U, info I WHERE I.content LIKE :query AND I.visibility=True AND I.user_id=U.id"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    listing = result.fetchall()
    return render_template("result.html", messages1=listing)