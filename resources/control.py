from hashlib import new
from flask_restful import Resource, reqparse
from models.account import AccountModel

accounts = [{
    'account_id': 1,
    'conta': 'pagar',
    'data': '01/10/2022',
    'valor': 'R$30,00'
    },
            {
    'account_id': 2,
    'conta': 'pagar',
    'data': '01/10/2022',
    'valor': 'R$300,00'
    }]

        

class Accounts(Resource):
    def get(self):
        return accounts
    
    def post(self):
        #verificando se a conta existe
        # if AccountModel.find_account(account_id):
        #    return {"message": "Accoutn id '{}' already exists".format(account_id)}, 400
                
        #agrupando os dados
        data = Account.arguments.parse_args()
        #new_account = {'account_id': account_id, **data} #kwargs
        new_account_object = AccountModel(**data) # valores vindo em um objeto
        # new_account = new_account_object.json()#convertendo o objeto para json
        # accounts.append(new_account)
        # return new_account, 200
        new_account_object.save_account()
        return new_account_object.json()
    

class Account(Resource):
    # arguments***
    # definindo quais valores poderam ser enviados
    # qualquer informação diferente não é aceita
    arguments = reqparse.RequestParser()
    arguments.add_argument('account_name')
    arguments.add_argument('title')
    arguments.add_argument('net_value')
    arguments.add_argument('gross_value')
    arguments.add_argument('details')
    arguments.add_argument('paid_received')
    arguments.add_argument('create_date')
    arguments.add_argument('date_release')
    arguments.add_argument('user')
    
    def get(self, account_id):        
        account = AccountModel.find_account(account_id)
        if account:
            return account
        """for account in accounts:
            if account['account_id'] == account_id:
                return account
            """
        return {'message':'Id not Found'}, 404
    

        
    def put(self, account_id):
        data = Account.arguments.parse_args()
        #new_account = {'account_id': account_id, **data} #kwargs
        new_account_object = AccountModel(account_id, **data) # valores vindo em um objeto
        new_account = new_account_object.json()#convertendo o objeto para json        
        account = Account.find_account(account_id)
        #edita a conta
        if account:
            account.update(new_account)
            return new_account,200
        #se a conta não existir, cria uma nova
        accounts.append(new_account)
        return new_account, 201
    
    def delete(self, account_id):
        global accounts
        accounts = [account for account in accounts if account['account_id']!= account_id]
        return {'message': 'account deleted'}