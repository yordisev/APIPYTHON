from conexion import create_db_connection

def get_all_users():
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def get_user_by_id(user_id):
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE id=%s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def create_user(user):
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(query, (user['name'], user['email']))
    connection.commit()
    cursor.close()
    connection.close()

def update_user(user_id, user):
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "UPDATE users SET name=%s, email=%s WHERE id=%s"
    cursor.execute(query, (user['name'], user['email'], user_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_user(user_id):
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE id=%s"
    cursor.execute(query, (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
