from pickle import TRUE
from flask_restful import Resource, reqparse
from models.account import AccountModel

class Accounts(Resource):
    def get(self):
        return {'accounts': [account.json() for account in AccountModel.query.all()]}
    
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
    arguments.add_argument('title',type=str, required=True,help="the field 'account_name' cannot be left blank, and use only string")
    arguments.add_argument('net_value',type=float, required=TRUE,help="the field 'account_name' cannot be left blank, and use only float")
    arguments.add_argument('gross_value',type=float, required=False,help="the field 'account_name' cannot be left blank, and use only float")
    arguments.add_argument('details',type=str, required=False,help="the field 'account_name' cannot be left blank, and use only string")
    arguments.add_argument('paid_received',type=int, required=True,help="the field 'account_name' cannot be left blank, and use only Integer")
    arguments.add_argument('create_date',type=str, required=False,help="the field 'account_name' cannot be left blank, and use only DateTime Format")
    arguments.add_argument('date_release',type=str, required=False,help="the field 'account_name' cannot be left blank, and use only DateTime Format")
    arguments.add_argument('user',type=str, required=True,help="the field 'account_name' cannot be left blank, and use only string")
    
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
    
    def delete(self, account_id):
        account = AccountModel.find_account(account_id)
        if account:
            try:
                account.delete_account()
            except:
                return {'message': 'An error ocurred trying to deleto accoutn.'}, 500
            return {'message': 'Account Deleted'}
        return {'message': 'Account not found.'}, 404