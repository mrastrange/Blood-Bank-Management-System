# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def get_db_connection():
    conn = sqlite3.connect('blood_bank.db')
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    with get_db_connection() as conn:
        # Create tables if they don't exist
        conn.execute('''CREATE TABLE IF NOT EXISTS Admin (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL
                        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS Donor (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            blood_type TEXT NOT NULL,
                            age INTEGER,
                            contact_info TEXT
                        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS Request (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            blood_type TEXT NOT NULL,
                            age INTEGER,
                            contact_info TEXT
                        )''')

        # Insert a sample admin for testing
        admin_username = "a"
        admin_password = hashlib.sha256("a".encode()).hexdigest()
        conn.execute("INSERT OR IGNORE INTO Admin (username, password) VALUES (?, ?)", 
                     (admin_username, admin_password))
        conn.commit()

setup_database()

# SQL function to retrieve donors by blood group
def get_donors_by_blood_type(blood_type):
    with get_db_connection() as conn:
        donors = conn.execute("SELECT id, name, blood_type, age, contact_info FROM Donor WHERE blood_type = ?", (blood_type,)).fetchall()
    return donors

@app.route('/need_blood', methods=['GET', 'POST'])
def need_blood():
    donors = []
    if request.method == 'POST':
        blood_type = request.form['blood_type']
        if blood_type:
            donors = get_donors_by_blood_type(blood_type)
            if not donors:
                flash("No donors found with the requested blood type.", "error")
            else:
                flash("Donors found!", "success")
        else:
            flash("Please enter a blood type.", "error")
    
    return render_template('need_blood.html', donors=donors)

# Index Route
@app.route('/')
def index():
    return render_template('index.html')

# Admin Login Page
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        with get_db_connection() as conn:
            admin = conn.execute("SELECT * FROM Admin WHERE username = ? AND password = ?", (username, password)).fetchone()
        if admin:
            session['admin_logged_in'] = True
            flash("Login successful!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid login credentials", "error")
    return render_template('admin.html')

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    with get_db_connection() as conn:
        donors = conn.execute("SELECT id, name, blood_type, age FROM Donor").fetchall()
        requests = conn.execute("SELECT id, name, blood_type, age, contact_info FROM Request").fetchall()
    
    return render_template('dashboard.html', donors=donors, requests=requests)

# Delete Request (Admin Only)
@app.route('/admin/delete_request/<int:request_id>')
def delete_request(request_id):
    if session.get('admin_logged_in'):
        with get_db_connection() as conn:
            conn.execute("DELETE FROM Request WHERE id = ?", (request_id,))
            conn.commit()
    return redirect(url_for('admin_dashboard'))

# User Request Page
@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        name = request.form['name']
        blood_type = request.form['blood_type']
        age = int(request.form['age'])
        contact_info = request.form['contact_info']
        with get_db_connection() as conn:
            conn.execute("INSERT INTO Request (name, blood_type, age, contact_info) VALUES (?, ?, ?, ?)", 
                         (name, blood_type, age, contact_info))
            conn.commit()
        flash("Request submitted successfully.")
    return render_template('request.html')

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# Route to Add a Donor (Admin Only)
@app.route('/admin/add_donor', methods=['POST'])
def add_donor():
    if session.get('admin_logged_in'):
        name = request.form['name']
        blood_type = request.form['blood_type']
        age = int(request.form['age'])
        contact_info = request.form['contact_info']
        with get_db_connection() as conn:
            conn.execute("INSERT INTO Donor (name, blood_type, age, contact_info) VALUES (?, ?, ?, ?)", 
                         (name, blood_type, age, contact_info))
            conn.commit()
        flash("Donor added successfully.")
    return redirect(url_for('admin_dashboard'))

# User Donor Signup Page
@app.route('/become_donor', methods=['GET', 'POST'])
def become_donor():
    if request.method == 'POST':
        name = request.form['name']
        blood_type = request.form['blood_type']
        age = int(request.form['age'])
        contact_info = request.form['contact_info']
        with get_db_connection() as conn:
            conn.execute("INSERT INTO Donor (name, blood_type, age, contact_info) VALUES (?, ?, ?, ?)", 
                         (name, blood_type, age, contact_info))
            conn.commit()
        flash("You have successfully registered as a donor!", "success")
        return redirect(url_for('become_donor'))

    return render_template('become_donor.html')

if __name__ == '__main__':
    app.run(debug=True)
