from flask import Flask
from flask_restful import Api
from resources.control import Accounts, Account

app = Flask(__name__)
api = Api(app)

api.add_resource(Accounts, '/financeiro') # list all acounts
api.add_resource(Account, '/financeiro/<int:account_id>') # showing selected by id

if __name__ == '__main__':
    app.run(debug=True)