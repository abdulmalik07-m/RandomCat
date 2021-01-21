import configparser
import sqlite3

import log

db_log = log.get_logger('db')


config = configparser.ConfigParser()
config.read('config.ini')
DATABASE_PATH = config.get('DATABASE', 'PATH')


def log(func):
    def wrapper(cat_id, cur):
        db_log.info(f'Try to get id:{cat_id}')  # Logging
        return func(cat_id, cur)
    return wrapper


def add_cat_to_bd(cat_url, cat_id, cur):
    cur.execute("SELECT cat_id FROM cats")
    if cat_id not in cur.fetchall():  # Try to find cat_id in db
        cur.execute("INSERT INTO cats VALUES (?, ?)", (cat_url, cat_id))  # Push new record to db


@log
def find_cat_id(cat_id, cur):
    cur.execute('SELECT cat_url FROM cats WHERE cat_id=?', (cat_id,))  # Find pic by id
    url = cur.fetchone()
    return url


def create_db():
    db = sqlite3.connect(DATABASE_PATH)
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS cats (
        cat_url TEXT,
        cat_id TEXT
        )""")
    db.commit()
    db.close()

