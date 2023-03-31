from flask import Flask, jsonify, request
from clientes import *
from usuarios import *

app = Flask(__name__)

# Usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    return jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
    user = request.json
    create_user(user)
    return '', 204

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = request.json
    update_user(user_id, user)
    return '', 204

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    delete_user(user_id)
    return '', 204

# Clientes
@app.route('/clientes', methods=['GET'])
def get_clients():
    clients = get_all_clients()
    # return jsonify({'clientes': clients})
    return clients

@app.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = get_client_by_id(client_id)
    return jsonify(client)

@app.route('/clients', methods=['POST'])
def create_client():
    client = request.json
    create_client(client)
    return '', 204

@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = request.json
    update_client(client_id, client)
    return '', 204

@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    delete_client(client_id)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
