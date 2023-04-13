from conexion import create_db_connection
from flask import Blueprint, jsonify, request, session, send_from_directory
from validar_key import Validar_Token
from werkzeug.security import generate_password_hash, check_password_hash
from os import getcwd, path, remove, mkdir
usuariosapi = Blueprint('Usuarios', __name__)
PATH_FILE  = getcwd() + "/uploads/"
CURRENT_DIRECTORY  = getcwd() + "/uploads/"

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
    return jsonify({'message' : 'You successfully logged out'}), 201


@usuariosapi.route('/usuarios/subir', methods=['POST'])
def subir_archivo():
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    try:
        # usu = request.json
        archivo = request.files['archivo']
        archivo.save(PATH_FILE + archivo.filename)
        # connection = create_db_connection()
        # cursor = connection.cursor()
        # query = "INSERT INTO db_usuarios(tipo_documento,numero_documento,nombres,apellidos,departamento,municipio,usuario, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        # cursor.execute(query, (usu['tipo_documento'],usu['numero_documento'],usu['nombres'],usu['apellidos'],usu['departamento'],usu['municipio'],usu['usuario'], passhash))
        # connection.commit()
        # cursor.close()
        # connection.close()
        return jsonify({'message': 'Usuario Creado Exitosamente.'}), 201
    except FileNotFoundError:
        return jsonify({'message': 'No se Logro Cargar el Archivo.'}), 405
    

@usuariosapi.route('/usuarios/ver/<string:nombre_archivo>', methods=['GET'])
def ver_archivo(nombre_archivo):
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    try:
        return send_from_directory(PATH_FILE,path=nombre_archivo,as_attachment=False)
    except FileNotFoundError:
        return jsonify({'message': 'No se Logro Cargar el Archivo.'}), 405
    

@usuariosapi.route('/usuarios/descargar/<string:nombre_archivo>', methods=['GET'])
def descargar_archivo(nombre_archivo):
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    try:
        return send_from_directory(PATH_FILE,path=nombre_archivo,as_attachment=True)
    except FileNotFoundError:
        return jsonify({'message': 'No se Logro Cargar el Archivo.'}), 405


@usuariosapi.route('/usuarios/eliminar', methods=['POST'])
def eliminar_archivo():
    api_key = request.headers.get('autorizacion')
    if not Validar_Token(api_key):
        return jsonify({'mensaje': 'API Key inválida'}), 401
    try:
        archivo = request.json['nombrearchivo']
        if path.isfile(PATH_FILE + archivo) == False:
            return jsonify({'message': 'archivo no encontrado'}), 404
        else:
            remove(PATH_FILE + archivo)
        return jsonify({'message': 'Archivo Eliminado Exitosamente.'}), 201
    except OSError:
        return jsonify({'message': 'No se Logro eliminar el Archivo.'}), 405
    

@usuariosapi.route('/usuarios/subircarpeta', methods=['POST'])
def carpetas_archivo():
    # api_key = request.headers.get('autorizacion')
    # if not Validar_Token(api_key):
    #     return jsonify({'mensaje': 'API Key inválida'}), 401
    try:
        archivos = request.files.getlist("files")
        for file in archivos:
            print(file)
            directory_file = file.filename.split("/")
            directory_file.pop()
            directory_file = "/".join(directory_file)
            print (directory_file)
            if path.exists(CURRENT_DIRECTORY + directory_file) == False:
                mkdir(path=CURRENT_DIRECTORY + directory_file)
                file.save(CURRENT_DIRECTORY + file.filename)
            else:
                file.save(CURRENT_DIRECTORY + file.filename)
        return jsonify({'message': 'Archivo Eliminado Exitosamente.'}), 201
    except FileNotFoundError:
        return jsonify({'message': 'No se Logro eliminar el Archivo.'}), 405