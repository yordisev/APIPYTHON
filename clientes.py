from conexion import create_db_connection

def get_all_clients():
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM clientes"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def get_client_by_id(client_id):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM clients WHERE id=%s"
    cursor.execute(query, (client_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def create_client(client):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO clients (name, email) VALUES (%s, %s)"
    cursor.execute(query, (client['name'], client['email']))
    connection.commit()
    cursor.close()
    connection.close()

def update_client(client_id, client):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE clients SET name=%s, email=%s WHERE id=%s"
    cursor.execute(query, (client['name'], client['email'], client_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_client(client_id):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM clients WHERE id=%s"
    cursor.execute(query, (client_id,))
    connection.commit()
    cursor.close()
    connection.close()
