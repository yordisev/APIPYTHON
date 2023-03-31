from flask import Flask

from user_crud import users_bp
from client_crud import clients_bp

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(clients_bp)

if __name__ == '__main__':
    app.run(debug=True)
