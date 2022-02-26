from flask import Flask, jsonify
from flask_restful import Api
from blocklist import BLOCKLIST
from resources.controlAccounts import Accounts, Account
from resources.controlUsers import User, CreateUser, UserLogin, userLogout
from flask_jwt_extended import JWTManager

app = Flask(__name__)
#configuração do DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# login
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

#criando o DB
@app.before_first_request
def create_data_base():
    database.create_all()
    
@jwt.token_in_blocklist_loader
def check_blocklist(token):
    return token['jti'] in BLOCKLIST

@jwt.revoked_token_loader
def access_token_invalid():
    return jsonify({'message': 'You have been logged out'}), 401

api.add_resource(Accounts, '/financeiro') # list all acounts
api.add_resource(Account, '/financeiro/<int:account_id>') # showing selected by id
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(CreateUser, '/user/created')
api.add_resource(UserLogin, '/user/login')
api.add_resource(userLogout, '/user/logout')

if __name__ == '__main__':
    from create_db import database
    database.init_app(app)
    app.run(debug=True)