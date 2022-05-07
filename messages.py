from db import db
from flask import session
import users

def get_list(thread_id):
    sql = "SELECT I.id, I.content, U.username, I.sent_at, U.id AS users_id, I.thread_message  FROM info I, users U WHERE I.user_id=U.id AND thread_id=:id AND I.visibility=True ORDER BY I.id DESC"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchall()

def get_areas():
    sql = "SELECT id, area_name FROM areas WHERE visibility=True"
    result = db.session.execute(sql)
    return result.fetchall()

def get_area_name(area_id):
    sql = "SELECT area_name FROM areas WHERE id=:id"
    result = db.session.execute(sql, {"id":area_id})
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
    if thread_id == False:
        return False
    if user_id == 0:
        return False
    sql = "INSERT INTO info (content, user_id, sent_at, thread_id, thread_message, visibility) VALUES (:content, :user_id, NOW(), :thread_id, False, True)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True

def make_thread(thread_name, content, area_id):
    user_id = users.user_id()
    if area_id == False:
        return False
    if len(thread_name) > 140:
        return False
    sql = "INSERT INTO threads (thread_name, area_id, visibility) VALUES (:thread_name, :area, True)"
    db.session.execute(sql, {"thread_name":thread_name, "area":area_id})

    sql = "SELECT MAX(id) FROM threads"
    thread_id = db.session.execute(sql).fetchone()[0]

    sql = "INSERT INTO info (content, user_id, sent_at, thread_id, thread_message, visibility) VALUES (:content, :user_id, NOW(), :thread_id, True, True)"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})

    db.session.commit()
    return True

def delete(message_id):
    sql = "UPDATE info SET visibility=False WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    db.session.commit()
    return result.rowcount

def delete_thread(thread_id):
    sql = "UPDATE threads SET visibility=False WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    sql = "UPDATE info SET visibility=False WHERE thread_id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

def make_area(area_name):
    if area_name == False:
        return False
    if len(area_name) > 140:
        return False
    sql = "INSERT INTO areas (area_name, visibility) VALUES (:name, TRUE);"
    db.session.execute(sql, {"name":area_name})
    sql = "SELECT MAX(id) FROM areas"
    area_id = db.session.execute(sql).fetchone()[0]
    sql = "INSERT INTO area_access (area_id, visibility) VALUES (:area_id, TRUE)"
    db.session.execute(sql, {"area_id":area_id})
    db.session.commit()
    return True

def delete_area(area_id):
    sql = "UPDATE areas SET visibility=False WHERE id=:id"
    db.session.execute(sql, {"id":area_id})
    sql = "SELECT MAX(id) FROM areas"
    area_id = db.session.execute(sql).fetchone()[0]
    sql = "UPDATE threads SET visibility=False WHERE area_id=:id"
    db.session.execute(sql, {"id":area_id})
    db.session.commit()

def get_newest_post():
    sql = "SELECT I.id, I.time, U.username FROM info I, users U WHERE I.thread_id=:thread_id AND U.id=I.user_id ORDER BY I.id DESC LIMIT 1"
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()

def get_search_result(query):
    sql = "SELECT I.id, I.content, U.username, I.thread_id, I.sent_at, U.id AS users_id FROM info I, users U WHERE I.content LIKE :query AND I.user_id=U.id"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()