import mysql.connector

def create_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prestamos_db",
        port=3306
    )
    return connection
