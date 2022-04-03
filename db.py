from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app.config["SQL_ALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
