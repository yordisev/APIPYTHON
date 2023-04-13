from flask import Blueprint, jsonify, request
from validar_key import Validar_Token
from conexion import create_db_connection

clients_bp = Blueprint('clients', __name__)

# Clientes
@clients_bp.route('/clientes', methods=['GET'])
def get_clients():
        # Se valida la API Key enviada en la cabecera del request
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM db_usuarios"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({'clients': result})

@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
            # Se valida la API Key enviada en la cabecera del request
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM db_clientes WHERE id=%s"
    cursor.execute(query, (client_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify(result)

@clients_bp.route('/clients', methods=['POST'])
def create_client():
            # Se valida la API Key enviada en la cabecera del request
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    client = request.json
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO db_clientes (name, email) VALUES (%s, %s)"
    cursor.execute(query, (client['name'], client['email']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Client created successfully.'}), 201

@clients_bp.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
            # Se valida la API Key enviada en la cabecera del request
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    client = request.json
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "UPDATE db_clientes SET name=%s, email=%s WHERE id=%s"
    cursor.execute(query, (client['name'], client['email'], client_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Client updated successfully.'}), 200

@clients_bp.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
            # Se valida la API Key enviada en la cabecera del request
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM db_clientes WHERE id=%s"
    cursor.execute(query, (client_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Client deleted successfully.'}), 200

# @clients_bp.route('/clients', methods=['POST'])
# def create_client():
#     client = request.json
#     connection = create_db_connection()
#     cursor = connection.cursor()
#     query = "CALL create_client_proc(%s, %s)"
#     cursor.execute(query, (client['name'], client['email']))
#     connection.commit()
#     cursor.close()
#     connection.close()
#     return jsonify({'message': 'Client created successfully.'}), 201