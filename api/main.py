from typing import Tuple
from flask import Flask, request, jsonify
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

@app.route("/api/countries", methods=["POST"])
def post_countries():
    body = request.get_json()
    if not body or "nume" not in body or "lat" not in body or "lon" not in body:
        return "Wrong request", 400
    try:
        db_conn, db_cursor = connect_db()
        db_cursor.execute("INSERT INTO Tari (nume_tara, latitudine, longitudine) VALUES (%s, %s, %s)", (body["nume"], body["lat"], body["lon"]))
        db_conn.commit()
        db_cursor.execute("SELECT id FROM Tari where nume_tara = %s", (body["nume"], ))
        id = db_cursor.fetchone()[0]
        db_cursor.close()
        db_conn.close()
        return jsonify({"id": id}), 201
    except Exception as e:
        return str(e), 409

@app.route("/api/countries", methods=["GET"])
def get_countries():
    db_conn, db_cursor = connect_db()
    db_cursor.execute("SELECT * FROM Tari")
    countries = db_cursor.fetchall()
    db_cursor.close()
    db_conn.close()
    return jsonify([{"id": country[0], "nume": country[1], "lat": country[2], "lon": country[3]} for country in countries]), 200

@app.route("/api/countries/<int:id>", methods=["PUT"])
def put_countries(id: int):
    body = request.get_json()
    if not body or "id" not in body or "nume" not in body or "lat" not in body or "lon" not in body or id != body["id"]:
        return "Wrong request", 400
    try:
        db_conn, db_cursor = connect_db()
        # Check that country with id exists in database
        db_cursor.execute("SELECT * FROM Tari WHERE id = %s", (id, ))
        if not db_cursor.fetchone():
            return "Tara nu exista", 404
        db_cursor.execute("UPDATE Tari SET id = %s, nume_tara = %s, latitudine = %s, longitudine = %s WHERE id = %s", (body["id"], body["nume"], body["lat"], body["lon"], id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        return "", 200
    except Exception as e:
        return str(e), 409
    
@app.route("/api/countries/<int:id>", methods=["DELETE"])
def delete_countries(id: int):
    try:
        db_conn, db_cursor = connect_db()
        # Check that country with id exists in database
        db_cursor.execute("SELECT * FROM Tari WHERE id = %s", (id, ))
        if not db_cursor.fetchone():
            return "Tara nu exista", 404
        db_cursor.execute("DELETE FROM Tari WHERE id = %s", (id, ))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        return "", 200
    except Exception as e:
        return str(e), 404
    
@app.route("/api/cities", methods=["POST"])
def post_cities():
    body = request.get_json()
    if not body or "idTara" not in body or "nume" not in body or "lat" not in body or "lon" not in body:
        return "Wrong request", 400
    try:
        db_conn, db_cursor = connect_db()
        # Check that country with id exists in database
        db_cursor.execute("SELECT * FROM Tari WHERE id = %s", (body["idTara"], ))
        if not db_cursor.fetchone():
            return "Tara nu exista", 404
        db_cursor.execute("INSERT INTO Orase (nume_oras, latitudine, longitudine, id_tara) VALUES (%s, %s, %s, %s)", (body["nume"], body["lat"], body["lon"], body["idTara"]))
        db_conn.commit()
        db_cursor.execute("SELECT id FROM Orase where id_tara = %s AND nume_oras = %s", (body["idTara"], body["nume"],))
        id = db_cursor.fetchone()[0]
        db_cursor.close()
        db_conn.close()
        return jsonify({"id": id}), 201
    except Exception as e:
        return str(e), 409

@app.route("/api/cities", methods=["GET"])
def get_cities():
    db_conn, db_cursor = connect_db()
    db_cursor.execute("SELECT id, id_tara, nume_oras, latitudine, longitudine FROM Orase")
    cities = db_cursor.fetchall()
    db_cursor.close()
    db_conn.close()
    return jsonify([{"id": city[0], "idTara": city[1], "nume": city[2], "lat": city[3], "lon": city[4], } for city in cities]), 200

@app.route("/api/cities/country/<int:id_Tara>", methods=["GET"])
def get_cities_by_country(id_Tara: int):
    db_conn, db_cursor = connect_db()
    db_cursor.execute("SELECT id, id_tara, nume_oras, latitudine, longitudine FROM Orase WHERE id_tara = %s", (id_Tara, ))
    cities = db_cursor.fetchall()
    db_cursor.close()
    db_conn.close()
    return jsonify([{"id": city[0], "idTara": city[1], "nume": city[2], "lat": city[3], "lon": city[4], } for city in cities]), 200

@app.route("/api/cities/<int:id>", methods=["PUT"])
def put_cities(id: int):
    body = request.get_json()
    if not body or "id" not in body or "idTara" not in body or "nume" not in body or "lat" not in body or "lon" not in body or id != body["id"]:
        return "Wrong request", 400
    try:
        db_conn, db_cursor = connect_db()
        db_cursor.execute("SELECT * FROM Tari WHERE id = %s", (body["idTara"], ))
        if not db_cursor.fetchone():
            return "Tara nu exista", 404
        db_cursor.execute("UPDATE Orase SET id = %s, nume_oras = %s, latitudine = %s, longitudine = %s, id_tara = %s WHERE id = %s", (body["id"], body["nume"], body["lat"], body["lon"], body["idTara"], id))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        return "", 200
    except Exception as e:
        return str(e), 409
    
@app.route("/api/cities/<int:id>", methods=["DELETE"])
def delete_cities(id: int):
    try:
        db_conn, db_cursor = connect_db()
        db_cursor.execute("DELETE FROM Orase WHERE id = %s", (id,))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        return "", 200
    except Exception as e:
        return str(e), 404

@app.route("/api/temperatures", methods=["POST"])
def post_temperatures():
    body = request.get_json()
    if not body or "idOras" not in body or "valoare" not in body or not isinstance(body["valoare"], (int, float)):
        return "Wrong request", 400
    try:
        db_conn, db_cursor = connect_db()
        db_cursor.execute("SELECT * FROM Orase WHERE id = %s", (body["idOras"],))
        if not db_cursor.fetchone():
            return "Orasul nu exista", 404
        db_cursor.execute("INSERT INTO Temperaturi (valoare, id_oras) VALUES (%s, %s)", (body["valoare"], body["idOras"]))
        db_conn.commit()
        db_cursor.execute("SELECT id FROM Temperaturi where id_oras = %s AND valoare = %s", (body["idOras"], body["valoare"],))
        id = db_cursor.fetchone()[0]
        db_cursor.close()
        db_conn.close()
        return jsonify({"id": id}), 201
    except Exception as e:
        return str(e), 409

if __name__ == '__main__':
    app.run('0.0.0.0', port=os.getenv("PORT"), debug=True)