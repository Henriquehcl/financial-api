#from pickle import TRUE
from flask_restful import Resource, reqparse
from models.account import AccountModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(
                        account_name = None,
                        title = None,
                        account_type = 0,
                        value_min = 0,
                        value_max = 100000,
                        limit = 30,
                        offset = 0, **data):
    
    if title:
        return {
            'account_name':account_name,
            'title':title,
            'account_type':account_type,
            'value_min': value_min,
            'value_max': value_max,
            'limit':limit,
            'offset':offset
        }
    return {
            'account_name':account_name,
            'title':title,
            'account_type':account_type,
            'value_min': value_min,
            'value_max': value_max,
            'limit':limit,
            'offset':offset
        }
# pesquisa por URL
path_params = reqparse.RequestParser()
path_params.add_argument('account_name', type=str)
path_params.add_argument('title', type=str)
path_params.add_argument('account_type', type=int)
path_params.add_argument('value_min', type=float)
path_params.add_argument('value_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Accounts(Resource):
    def get(self):
        #conectar ao DB
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        data = path_params.parse_args()
        valid_data = {key:data[key] for key in data if data[key] is not None}
        params = normalize_path_params(**valid_data)
        
        if not params.get('title'):
            query = "SELECT * FROM accounts \
                WHERE (account_name = ?) \
                and account_type = ? \
                and (due_value > ? and due_value < ?) \
                LIMIT ? OFFSET ?"
            tupla = tupla([params[key] for key in params])
            result = cursor.execute(query, tupla)
        else:
            query = "SELECT * FROM accounts \
                WHERE (account_name = ?) \
                and title = ? \
                and account_type = ? \
                and (due_value > ? and due_value < ?) \
                LIMIT ? OFFSET ?"
            tupla = tupla([params[key] for key in params])
            result = cursor.execute(query, tupla)
        return {'accounts': [account.json() for account in AccountModel.query.all()]}
    
    @jwt_required()
    def post(self):
               
        #agrupando os dados
        data = Account.arguments.parse_args()
        new_account_object = AccountModel(**data) # valores vindo em um objeto
        try:
            new_account_object.save_account()
        except:
            return{'message': 'an error ocurred trying to save account'}, 500
        return new_account_object.json()
    

class Account(Resource):
    # arguments***
    # definindo quais valores poderam ser enviados
    # qualquer informação diferente não é aceita
    arguments = reqparse.RequestParser()
    arguments.add_argument('account_name', type=str, required=True , help="the field 'account_name' cannot be left blank, and use only string")
    arguments.add_argument('title',type=str, required=True,help="the field 'title' cannot be left blank, and use only string")
    arguments.add_argument('account_type', type=int, required=True, help="the field 'account_type' cannot be left blank")
    arguments.add_argument('due_date', type=str, required=False, help="the field 'due_date' cannot be left blank")
    arguments.add_argument('net_value',type=float, required=True,help="the field 'net_value' cannot be left blank, and use only float")
    arguments.add_argument('gross_value',type=float, required=False,help="the field 'gross_value' cannot be left blank, and use only float")
    arguments.add_argument('details',type=str, required=False,help="the field 'details' cannot be left blank, and use only string")
    arguments.add_argument('paid_received',type=int, required=True,help="the field 'paid_received' cannot be left blank, and use only Integer")
    arguments.add_argument('create_date',type=str, required=False,help="the field 'create_date' cannot be left blank, and use only DateTime Format")
    arguments.add_argument('date_release',type=str, required=False,help="the field 'date_release' cannot be left blank, and use only DateTime Format")
    arguments.add_argument('user',type=str, required=True,help="the field 'user' cannot be left blank, and use only string")
    
    def get(self, account_id):
        print(account_id)        
        account = AccountModel.find_account(account_id)
        if account:
            return account.json()
        """for account in accounts:
            if account['account_id'] == account_id:
                return account
            """
        return {'message':'Id not Found'}, 404
    

    @jwt_required()    
    def put(self, account_id):
        data = Account.arguments.parse_args()
        account_found = AccountModel.find_account(account_id)
        if account_found:
            account_found.update_account(**data)
            account_found.save_account()
            return account_found.json(), 200
        account = AccountModel(account_id, **data)
        #account.save()
        try:
            account.save_account()
        except:
            return{'message': 'an error ocurred trying to save account'}, 500
        return account.json(), 201
    
    @jwt_required()
    def delete(self, account_id):
        account = AccountModel.find_account(account_id)
        if account:
            try:
                account.delete_account()
            except:
                return {'message': 'An error ocurred trying to delete account.'}, 500
            return {'message': 'Account Deleted'}
        return {'message': 'Account not found.'}, 404