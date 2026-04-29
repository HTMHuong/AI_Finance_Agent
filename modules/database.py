import sqlite3
import pandas as pd
import os

DB_PATH = 'data/finance.db'

def connect_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Khởi tạo cấu trúc Database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT,
            note TEXT,
            type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_transactions():
    """Lấy dữ liệu từ CSV để hiển thị (Ưu tiên CSV cho bài tập này)"""
    csv_path = 'data/sample_data.csv'
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()