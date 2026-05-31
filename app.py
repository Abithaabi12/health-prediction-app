from flask import Flask, render_template, request, redirect
import sqlite3
import requests

app = Flask(__name__)

# initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dob TEXT,
            email TEXT,
            glucose REAL,
            haemoglobin REAL,
            cholesterol REAL,
            status TEXT
        )
    """)
    conn.close()

init_db()

# simple health prediction (with API usage)
def get_health_status(glucose, haemoglobin, cholesterol):
    try:
        # calling free API (just to show integration)
        response = requests.get("https://api.agify.io?name=test")
        data = response.json()
        print("API called:", data)

        # basic logic (realistic beginner level)
        if glucose > 140:
            return "Diabetes Risk"
        elif cholesterol > 200:
            return "High Cholesterol"
        elif haemoglobin < 12:
            return "Low Haemoglobin"
        else:
            return "Normal"

    except:
        return "Check manually"

# home page
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()
    return render_template('index.html', data=data)

# add patient
@app.route('/add', methods=['POST'])
def add_data():
    name = request.form['name']
    dob = request.form['dob']
    email = request.form['email']
    glucose = float(request.form['glucose'])
    haemoglobin = float(request.form['haemoglobin'])
    cholesterol = float(request.form['cholesterol'])

    status = get_health_status(glucose, haemoglobin, cholesterol)

    conn = sqlite3.connect('database.db')
    conn.execute("""
        INSERT INTO patients (name, dob, email, glucose, haemoglobin, cholesterol, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, dob, email, glucose, haemoglobin, cholesterol, status))
    conn.commit()
    conn.close()

    return redirect('/')

# delete
@app.route('/delete/<int:id>')
def delete_data(id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# update
@app.route('/update/<int:id>', methods=['POST'])
def update_data(id):
    name = request.form['name']
    dob = request.form['dob']
    email = request.form['email']
    glucose = float(request.form['glucose'])
    haemoglobin = float(request.form['haemoglobin'])
    cholesterol = float(request.form['cholesterol'])

    status = get_health_status(glucose, haemoglobin, cholesterol)

    conn = sqlite3.connect('database.db')
    conn.execute("""
        UPDATE patients 
        SET name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, status=? 
        WHERE id=?
    """, (name, dob, email, glucose, haemoglobin, cholesterol, status, id))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)