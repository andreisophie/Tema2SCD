from typing import Tuple
from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def connect_db() -> Tuple[psycopg2._psycopg.connection, psycopg2._psycopg.cursor]:
    db_conn = psycopg2.connect(database=os.getenv("DB_NAME"),
                            host=os.getenv("DB_HOST"),
                            user=os.getenv("DB_USER"),
                            password=os.getenv("DB_PASS"),
                            port=os.getenv("DB_PORT"))
    db_cursor = db_conn.cursor()
    return db_conn, db_cursor

@app.route("/ruta1", methods=["GET"])
def hello():
    return "Hello, World!"


@app.route("/ruta2")
def salut():
    return "Salut, Lume!"


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)