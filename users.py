from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = token_hex(16)
            return True
        else:
            return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def logout():
    del session["csrf_token"]
    del session["user_id"]

def create_admin(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO admins (username,password, admin) VALUES (:username,:password,TRUE)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def admin():
    user_id = session.get("user_id", 0)
    sql = "SELECT user_id, admin FROM users WHERE user_id=:user_id AND admin=TRUE"
    result = db.session.execute(sql, {"user_id": user_id})
    if result.fetchone():
        return True
    else:
        return False
