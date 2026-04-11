import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('users.db')

print("=== TABLES IN DB ===")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)
print("\n")

print("=== USERS TABLE (Last 5) ===")
try:
    users = pd.read_sql("SELECT * FROM users ORDER BY id DESC LIMIT 5", conn)
    print(users)
except Exception as e:
    print(f"Error reading users: {e}")
print("\n")

print("=== TRANSACTIONS TABLE (Last 5) ===")
try:
    trx = pd.read_sql("SELECT * FROM transactions ORDER BY id DESC LIMIT 5", conn)
    print(trx)
except Exception as e:
    print(f"Error reading transactions: {e}")

conn.close()
