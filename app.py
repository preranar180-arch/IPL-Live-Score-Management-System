from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from dotenv import load_dotenv
from database import get_db_connection

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_team', methods=['POST'])
def add_team():
    team = request.form['team']
    cursor.execute("INSERT INTO teams(team_name) VALUES(%s)", (team,))
    db.commit()
    return redirect('/')

@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name']
    role = request.form['role']
    team = request.form['team']
    cursor.execute("INSERT INTO players(name, role, team_id) VALUES(%s,%s,%s)",
                   (name, role, team))
    db.commit()
    return redirect('/')

@app.route('/add_match', methods=['POST'])
def add_match():
    t1 = request.form['team1']
    t2 = request.form['team2']
    cursor.execute("INSERT INTO matches(team1, team2, score1, score2, status) VALUES(%s,%s,0,0,'Upcoming')",
                   (t1, t2))
    db.commit()
    return redirect('/')


#def get_db_connection():
    pass



@app.route('/update_score', methods=['POST'])
@app.route('/update_score', methods=['POST'])
def update_score():
    match_id = request.form['match_id']
    score1 = request.form['score1']
    score2 = request.form['score2']
    status = request.form['status']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE matches
        SET score1=%s, score2=%s, status=%s
        WHERE match_id=%s
    """, (score1, score2, status, match_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/live')



@app.route('/live')
def live():
    cursor.execute("SELECT * FROM matches")
    matches= cursor.fetchall()
    return render_template('live_score.html', matches=matches)



@app.route('/report')
def report():
    cursor.execute("SELECT COUNT(*) FROM teams")
    teams = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM players")
    players = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM matches")
    matches = cursor.fetchone()[0]

    return render_template(
        'report.html',
        teams=teams,
        players=players,
        matches=matches
    )


app.run(debug=True)
