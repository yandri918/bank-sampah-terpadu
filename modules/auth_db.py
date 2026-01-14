import sqlite3
import pandas as pd
import datetime

DB_FILE = "users.db"

def get_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_db():
    """Initialize the database tables."""
    conn = get_connection()
    c = conn.cursor()
    
    # Users Table
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

    # Transactions Table (New)
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            tanggal DATE,
            nasabah TEXT,
            petugas TEXT,
            lokasi TEXT,
            
            -- Waste Categories (Weights)
            burnable REAL, paper REAL, cloth REAL, cans REAL,
            electronics REAL, pet_bottles REAL, plastic_marks REAL,
            white_trays REAL, glass_bottles REAL, metal_small REAL, hazardous REAL,
            
            -- Financials
            total_kg REAL,
            total_paid INTEGER,
            total_revenue INTEGER,
            profit INTEGER
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

def save_transaction(data):
    """Save a transaction dictionary to SQLite."""
    conn = get_connection()
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO transactions (
                timestamp, tanggal, nasabah, petugas, lokasi,
                burnable, paper, cloth, cans, electronics, pet_bottles, plastic_marks,
                white_trays, glass_bottles, metal_small, hazardous,
                total_kg, total_paid, total_revenue, profit
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.datetime.now(),
            data['Tanggal'], data['Nasabah'], data['Petugas'], data['Lokasi'],
            data['Burnable'], data['Paper'], data['Cloth'], data['Cans'],
            data['Electronics'], data['PET_Bottles'], data['Plastic_Marks'],
            data['White_Trays'], data['Glass_Bottles'], data['Metal_Small'], data['Hazardous'],
            data['total_kg'], data['Total_Bayar_Nasabah'], data['Est_Pendapatan_Bank'], data['Est_Profit']
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving transaction: {e}")
        return False
    finally:
        conn.close()

def get_all_transactions():
    """Fetch all transactions as a Pandas DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
        # Rename columns to match legacy CSV format for compatibility if needed, 
        # or just map them properly in the dashboard.
        
        # Mapping back to friendly names for display
        mapper = {
            'timestamp': 'Timestamp', 'tanggal': 'Tanggal', 'nasabah': 'Nasabah',
            'petugas': 'Petugas', 'lokasi': 'Lokasi',
            'burnable': 'Burnable', 'paper': 'Paper', 'cloth': 'Cloth',
            'cans': 'Cans', 'electronics': 'Electronics', 'pet_bottles': 'PET_Bottles',
            'plastic_marks': 'Plastic_Marks', 'white_trays': 'White_Trays',
            'glass_bottles': 'Glass_Bottles', 'metal_small': 'Metal_Small',
            'hazardous': 'Hazardous',
            'total_kg': 'Total_KG',
            'total_paid': 'Total_Bayar_Nasabah',
            'total_revenue': 'Est_Pendapatan_Bank',
            'profit': 'Est_Profit'
        }
        df.rename(columns=mapper, inplace=True)
        return df
    except Exception as e:
        print(f"Error reading transactions: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
