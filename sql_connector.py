import mysql.connector

def connect():
    conn = mysql.connector.connect(host='78.29.44.222',
                                    port='3000',
                                    database='WowtoDatabase',
                                    user='wowto',
                                    password='wowto')
    if conn.is_connected():
        return conn
