from conexion import create_db_connection
from flask import Blueprint, jsonify, request, session
from validar_key import Validar_Token
from werkzeug.security import generate_password_hash, check_password_hash
usuariosapi = Blueprint('Usuarios', __name__)
 

@usuariosapi.route('/usuarios/crear', methods=['POST'])
def crear_usuario():
            # Se valida la API Key enviada en la cabecera del request
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    usu = request.json
    passhash = generate_password_hash(usu['password'])
    # pbkdf2:sha256:260000$awJ80tfWJouHfYGl$b357d8be88edbe32b369a90fcbb83f3100681d3eeed0c5f5b4673b53ce338163
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO db_usuarios(tipo_documento,numero_documento,nombres,apellidos,departamento,municipio,usuario, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (usu['tipo_documento'],usu['numero_documento'],usu['nombres'],usu['apellidos'],usu['departamento'],usu['municipio'],usu['usuario'], passhash))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Usuario Creado Exitosamente.'}), 201

@usuariosapi.route('/login', methods=['POST'])
def login():
    _json = request.json
    _username = _json['usuario']
    _password = _json['password']
    print(_password)
    # validate the received values
    if _username and _password:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM db_usuarios WHERE usuario=%s"
        cursor.execute(query, (_username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        username = result['usuario']
        password = result['password']
        if result:
            if check_password_hash(password, _password):
                session['username'] = username
                cursor.close()
                return jsonify({'message' : 'You are logged in successfully'})
            else:
                resp = jsonify({'message' : 'Bad Request - invalid password'})
                resp.status_code = 400
                return resp
    else:
        resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
        resp.status_code = 400
        return resp
         
@usuariosapi.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message' : 'You successfully logged out'})