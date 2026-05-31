from flask import Flask, render_template, request, redirect
import sqlite3

import joblib
import numpy as np
# Load trained ML model for health risk prediction
patient_risk_model = joblib.load("health_model.pkl")

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
            remarks TEXT
        )
    """)
    conn.close()

init_db()

# This function predicts health risk using trained ML model
def get_remark(glucose, haemoglobin, cholesterol):

    prediction_result = patient_risk_model.predict([[glucose, haemoglobin, cholesterol]])[0]

    if prediction_result == 1:
        return "High Health Risk (AI Model)"
    else:
        return "Normal (AI Model)"

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

    # AI remark generation
    remarks = get_remark(glucose, haemoglobin, cholesterol)

    conn = sqlite3.connect('database.db')
    conn.execute("""
        INSERT INTO patients (name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks))
    conn.commit()
    conn.close()

    return redirect('/')

# delete patient
@app.route('/delete/<int:id>')
def delete_data(id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# update patient
@app.route('/update/<int:id>', methods=['POST'])
def update_data(id):
    name = request.form['name']
    dob = request.form['dob']
    email = request.form['email']
    glucose = float(request.form['glucose'])
    haemoglobin = float(request.form['haemoglobin'])
    cholesterol = float(request.form['cholesterol'])

    # AI remark generation
    remarks = get_remark(glucose, haemoglobin, cholesterol)

    conn = sqlite3.connect('database.db')
    conn.execute("""
        UPDATE patients 
        SET name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
        WHERE id=?
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks, id))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
