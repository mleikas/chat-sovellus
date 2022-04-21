from db import db
import users

def get_list():
    sql = "SELECT I.content, U.username, I.sent_at FROM info I, users U WHERE I.user_id=U.id ORDER BY I.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(content):
    user_id = users.user_id
    if user_id == 0:
        return False
    sql = "INSERT INTO info (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True

def search(content):
    pass