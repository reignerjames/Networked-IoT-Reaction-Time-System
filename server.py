# server.py  —  simple viewer for ~/Desktop/game.db
from flask import Flask, jsonify, send_from_directory
import sqlite3
from pathlib import Path

app = Flask(__name__, static_url_path="", static_folder=".")

DB_PATH = Path.home() / "Desktop" / "game.db"

def q(sql, params=()):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(sql, params).fetchall()
    con.close()
    return [dict(r) for r in rows]

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# --- JSON APIs ---
@app.route("/api/results")
def api_results():
    rows = q("SELECT id, player_name, score, time_played, date_saved "
             "FROM results ORDER BY id DESC LIMIT 200")
    return jsonify(rows)

@app.route("/api/game")
def api_game():
    rows = q("SELECT user_id, score_1, score_2, score_3 FROM game")
    return jsonify(rows)

# quick health check
@app.route("/api/ping")
def ping():
    return {"ok": True, "db": str(DB_PATH)}

if __name__ == "__main__":
    # 0.0.0.0 so your PC can view it via http://raspberrypi.local:8080
    app.run(host="0.0.0.0", port=8080, debug=False)