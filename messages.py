from db import db
import users

def get_list():
    sql = "SELECT I.content, U.username, I.sent_at FROM info I, users U WHERE I.user_id=U.id ORDER BY I.id DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_areas():
    sql = "SELECT id, area_name FROM areas WHERE visibility=True"
    result = db.session.execute(sql)
    return result.fetchall()

def get_area_name(area_id):
    sql = "SELECT area_name FROM areas WHERE id=:id"
    result = db.session.execute(sql, {"id": area_id})
    return result.fetchone()[0]

def get_threads(area_id):
    sql = "SELECT id, thread_name FROM threads WHERE area_id=:id and visibility=True"
    result = db.session.execute(sql, {"id":area_id})
    return result.fetchall()

def get_header(thread_id):
    sql = "SELECT A.id, A.area_name, T.thread_name FROM areas A, threads T WHERE T.id=:id AND T.area_id=A.id LIMIT 1"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()

def send(content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO info (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True

def make_thread(thread_name, content, area_id):
    if len(topic) > 140:
        return False
    user_id = session.get("user_id", 0)
    sql = "INSERT INTO threads (thread_name, area_id, visibility) \ VALUES (:topic, :area, True)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True

def delete(message_id):
    sql = "UPDATE info SET visible=False WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    db.session.commit()
    return result.rowcount

def search(content):
    pass