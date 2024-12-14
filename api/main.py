from typing import Tuple
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def connect_db():
    db_conn = psycopg2.connect(database=os.getenv("DB_NAME"),
                               host=os.getenv("DB_HOST"),
                               user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASS"),
                               port=os.getenv("DB_PORT"))
    db_cursor = db_conn.cursor()
    return db_conn, db_cursor

@app.route("/api/countries", methods=["POST"])
def post_countries():
    body = request.get_json()
    if not body or "nume" not in body or "lat" not in body or "lon" not in body:
        return "Wrong request", 400
    try:
        db_conn, db_cursor = connect_db()
        db_cursor.execute("INSERT INTO Tari (nume_tara, latitudine, longitudine) VALUES (%s, %s, %s)", (body["nume"], body["lat"], body["lon"]))
        db_conn.commit()
        id = db_cursor.lastrowid
        db_cursor.close()
        db_conn.close()
        return jsonify({"id": id}), 201
    except Exception as e:
        return str(e), 409

@app.route("/api/countries", methods=["GET"])
def get_countries():
    db_conn, db_cursor = connect_db()
    db_cursor.execute("SELECT * FROM countries")
    countries = db_cursor.fetchall()
    db_cursor.close()
    db_conn.close()
    return jsonify([{"id": country[0], "name": country[1], "lat": country[2], "lon": country[3]} for country in countries]), 200

if __name__ == '__main__':
    app.run('0.0.0.0', port=os.getenv("PORT"), debug=True)