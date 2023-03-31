from flask import Blueprint, jsonify, request

from conexion import create_db_connection

users_bp = Blueprint('users', __name__)

# Usuarios
@users_bp.route('/users', methods=['GET'])
def get_users():
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({'users': result})

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id=%s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify(result)

@users_bp.route('/users', methods=['POST'])
def create_user():
    user = request.json
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(query, (user['name'], user['email']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User created successfully.'}), 201

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = request.json
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "UPDATE users SET name=%s, email=%s WHERE id=%s"
    cursor.execute(query, (user['name'], user['email'], user_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User updated successfully.'}), 200

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE id=%s"
    cursor.execute(query, (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User deleted successfully.'}), 200
