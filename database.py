import os
import streamlit as st
import sqlite3
import pandas as pd
# import mysql.connector # Uncomment when using actual MySQL

def get_db_connection():
    """
    Establishes a connection to the database.
    For instant deployment on Streamlit Cloud without external DB setup, 
    we use SQLite by default. 
    To use MySQL, configure st.secrets["mysql"] in your Streamlit dashboard.
    """
    # Check if MySQL secrets exist (for Streamlit Cloud deployment)
    try:
        if "mysql" in st.secrets:
            # try:
            #     connection = mysql.connector.connect(
            #         host=st.secrets["mysql"]["host"],
            #         database=st.secrets["mysql"]["database"],
            #         user=st.secrets["mysql"]["user"],
            #         password=st.secrets["mysql"]["password"]
            #     )
            #     return connection, "mysql"
            # except Exception as e:
            #     print(f"MySQL Connection Error: {e}")
            pass
    except Exception:
        # st.secrets parsing fails locally if secrets.toml doesn't exist
        pass
    
    # Fallback to local SQLite for instant prototyping
    conn = sqlite3.connect('trafficguard.db', check_same_thread=False)
    # Ensure tables exist
    create_sqlite_tables(conn)
    return conn, "sqlite"

def create_sqlite_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT UNIQUE NOT NULL,
            owner_name TEXT NOT NULL,
            is_repeat_offender BOOLEAN DEFAULT FALSE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT,
            violation_type TEXT,
            fine_amount REAL,
            status TEXT DEFAULT 'PENDING',
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Insert some dummy data if empty
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO vehicles (vehicle_number, owner_name) VALUES ('MH01AB1234', 'John Doe')")
        cursor.execute("INSERT INTO vehicles (vehicle_number, owner_name, is_repeat_offender) VALUES ('KA05XY9876', 'Jane Smith', 1)")
        cursor.execute("INSERT INTO violations (vehicle_number, violation_type, fine_amount) VALUES ('KA05XY9876', 'Speeding', 2000.0)")
    conn.commit()

def fetch_all_violations():
    conn, db_type = get_db_connection()
    query = "SELECT * FROM violations"
    df = pd.read_sql_query(query, conn)
    # Note: Streamlit's pd.read_sql manages closing the cursor, but we close connection if needed.
    if db_type == "mysql":
        conn.close()
    return df

def get_vehicle_by_number(vehicle_number):
    conn, db_type = get_db_connection()
    if db_type == "sqlite":
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE vehicle_number = ?", (vehicle_number,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "vehicle_number": row[1], "owner_name": row[2], "is_repeat_offender": row[3]}
        return None
    # Add MySQL logic here later
    return None

def insert_violation(vehicle_number, violation_type, fine_amount):
    conn, db_type = get_db_connection()
    if db_type == "sqlite":
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO violations (vehicle_number, violation_type, fine_amount) VALUES (?, ?, ?)",
            (vehicle_number, violation_type, fine_amount)
        )
        conn.commit()
    # Add MySQL logic here later
    return True
