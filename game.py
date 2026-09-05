# ============================================================
# game.py — Reaction Time Game (GPIO17 button) → SQLite
#   - results(id, player_name, score, time_played, date_saved)
#   - game(user_id, score_1, score_2, score_3)
# DB path: ~/Desktop/game.db  (pairs with server.py viewer)
# ============================================================

import time
import random
import sqlite3
from pathlib import Path
from datetime import timedelta
import RPi.GPIO as GPIO

# ---------- Config ----------
PLAYER     = "Reigner"            # shown in results table
USER_ID    = 1                    # snapshot row key in 'game'
BUTTON_PIN = 17                   # button between GPIO17 and GND
DB_PATH    = Path.home() / "Desktop" / "game.db"

# Optional Sense HAT feedback (safe if not present)
try:
    from sense_hat import SenseHat
    sense = SenseHat()
    SENSE_AVAILABLE = True
except Exception:
    SENSE_AVAILABLE = False
    sense = None

# ---------- GPIO ----------
GPIO.setmode(GPIO.BCM)
# Internal pull-up: idle HIGH; press to GND → LOW
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_button_press(msg="Press the button to continue…"):
    print(msg)
    GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)  # active LOW
    time.sleep(0.15)  # debounce

# ---------- Visual helpers ----------
def show_ready():
    if SENSE_AVAILABLE: sense.clear(255, 0, 0)
    else: print("Get ready…")

def show_go():
    if SENSE_AVAILABLE: sense.clear(0, 255, 0)
    else: print("GO!")

def clear_display():
    if SENSE_AVAILABLE: sense.clear()

# ---------- DB helpers ----------
def init_db():
    """Create tables if missing (matches the viewer schema)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score       INTEGER NOT NULL,     -- reaction time (ms)
            time_played TEXT NOT NULL,        -- 'HH:MM:SS'
            date_saved  TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game (
            user_id  INTEGER PRIMARY KEY,
            score_1  INTEGER NOT NULL,
            score_2  INTEGER NOT NULL,
            score_3  INTEGER NOT NULL
        );
    """)

    con.commit()
    con.close()
    print(f"[DB] Ready at: {DB_PATH}")

def insert_result(player, score_ms, elapsed_str):
    """Append one round to results."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO results (player_name, score, time_played, date_saved)
        VALUES (?, ?, ?, datetime('now'))
    """, (player, score_ms, elapsed_str))
    con.commit()
    con.close()

def update_game_snapshot(user_id, s1, s2, s3):
    """Upsert the 3-score snapshot."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO game (user_id, score_1, score_2, score_3) VALUES (?, ?, ?, ?)",
            (user_id, s1, s2, s3)
        )
    except sqlite3.IntegrityError:
        cur.execute(
            "UPDATE game SET score_1=?, score_2=?, score_3=? WHERE user_id=?",
            (s1, s2, s3, user_id)
        )
    con.commit()
    con.close()

# ---------- one round ----------
def reaction_round() -> int:
    """Run one round; return reaction time (ms)."""
    clear_display()
    show_ready()
    time.sleep(random.uniform(1.0, 3.0))
    show_go()

    start = time.time()
    while GPIO.input(BUTTON_PIN) == 1:   # wait until button goes LOW
        pass
    rt_ms = int((time.time() - start) * 1000)

    clear_display()
    if SENSE_AVAILABLE:
        sense.show_message(f"{rt_ms} ms", scroll_speed=0.06, text_colour=[255,255,255])
    else:
        print(f"Reaction: {rt_ms} ms")

    return rt_ms

# ---------- main ----------
def main():
    session_start = time.time()
    try:
        init_db()
        print("\n=== Reaction Game ===")
        print(f"DB: {DB_PATH}")
        wait_for_button_press("Press the button (GPIO17→GND) to START.")

        scores = []
        for i in range(3):
            print(f"\nRound {i+1}…")
            rt = reaction_round()
            scores.append(rt)
            elapsed = str(timedelta(seconds=int(time.time() - session_start)))
            insert_result(PLAYER, rt, elapsed)
            time.sleep(0.8)

        update_game_snapshot(USER_ID, scores[0], scores[1], scores[2])
        print(f"\n✅ Finished. Scores: {scores} | Best: {min(scores)} ms")
        print("Open http://raspberrypi.local:8080 to view.")
    finally:
        clear_display()
        GPIO.cleanup()
        print("[GPIO] Cleaned up pins.")

if __name__ == "__main__":
    main()