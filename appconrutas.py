from flask import Flask, session, jsonify, render_template
from flask_cors import CORS
from user_crud import users_bp
from client_crud import clients_bp
from login import usuariosapi
from datetime import timedelta

app = Flask(__name__,template_folder='template')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(users_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(usuariosapi)
app.config['SECRET_KEY'] = 'Coders20323.!'
 
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)


@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return jsonify({'message' : 'You are already logged in', 'username' : username})
    else:
        return render_template('noautorizado.html')
        # resp = jsonify({'message' : 'Unauthorized'})
        # resp.status_code = 401
        # return resp

if __name__ == '__main__':
    app.run(debug=True)
