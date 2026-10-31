import sqlite3

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

# Players table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    team TEXT
)
""")

# Matches table
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1 TEXT,
    team2 TEXT,
    match_date TEXT,
    venue TEXT
)
""")

conn.commit()
conn.close()

print("Tables created successfully")
