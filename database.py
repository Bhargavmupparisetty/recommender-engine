import sqlite3
import time
import sys

class Database:
    
    def __init__(self):

        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                amount REAL NOT NULL,
                customer_name TEXT NOT NULL,
                billing_date TEXT DEFAULT (datetime('now','localtime'))
            )
        ''')

        conn.commit()
        conn.close()


    def insert_billed_value(self, item, amount, customer_name):
        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bills (item, amount, customer_name)
            VALUES (?, ?, ?)
        ''', (item, amount, customer_name))
        conn.commit()
        conn.close()

    def update_billed_value(self, bill_id, new_amount):
        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE bills SET amount = ? WHERE id = ?
        ''', (new_amount, bill_id))
        conn.commit()
        conn.close()

    def delete_billed_value(self, bill_id):
        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bills WHERE id = ?', (bill_id,))
        conn.commit()
        conn.close()

    def get_billed_values_by_timeframe(self, start_date, end_date):
        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM bills WHERE billing_date BETWEEN ? AND ?
        ''', (start_date, end_date))
        rows = cursor.fetchall()
        conn.close()
        return rows
