import sqlite3
from flask import g
import os.path

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#db_path = os.path.join(BASE_DIR, "code_challange_lap4.db")

DATABASE = 'code_challange_lap4.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
         db = g._database = sqlite3.connect(DATABASE)
    return db



