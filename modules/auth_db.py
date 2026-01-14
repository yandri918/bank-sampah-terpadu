import sqlite3
import os

DB_FILE = "users.db"

def get_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_db():
    """Initialize the users table."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_user(email, password_hash, name, role="user"):
    """Register a new user."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (email, password_hash, name, role) VALUES (?, ?, ?, ?)', 
                  (email, password_hash, name, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Email already exists
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    """Retrieve user details by email."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, email, password_hash, name, role FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "email": user[1],
            "password_hash": user[2],
            "name": user[3],
            "role": user[4]
        }
    return None
