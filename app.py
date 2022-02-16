from flask import Flask
from flask_restful import Api
from resources.control import Accounts, Account

app = Flask(__name__)
#configuração do DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

#criando o DB
@app.before_first_request
def create_data_base():
    database.create_all()

api.add_resource(Accounts, '/financeiro') # list all acounts
api.add_resource(Account, '/financeiro/<int:account_id>') # showing selected by id

if __name__ == '__main__':
    from create_db import database
    database.init_app(app)
    app.run(debug=True)