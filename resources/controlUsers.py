# from pickle import TRUE
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blocklist import BLOCKLIST

attributes = reqparse.RequestParser()
attributes.add_argument('user_name', type=str, required=True, help="the field 'user_name' cannot be left blank")
attributes.add_argument('login', type=str, required=True, help="the field 'login' cannot be left blank")
attributes.add_argument('password', type=str, required=True, help="the field 'password' cannot be left blank")
attributes.add_argument('email', type=str, required=True, help="the field 'email' cannot be left blank")
attributes.add_argument('create_date', type=str, required=False, help="the field 'create_date' cannot be left blank")
attributes.add_argument('admin', type=int, required=True, help="the field 'admin' cannot be left blank")

login_attributes = reqparse.RequestParser()
login_attributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
login_attributes.add_argument('password',  type=str, required=True, help="The field 'password' cannot be left blank")

class Users(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}
    
    def post(self):
               
        #agrupando os dados
        data = User.arguments.parse_args()
        new_user_object = UserModel(**data) # valores vindo em um objeto
        try:
            new_user_object.save_user()
        except:
            return{'message': 'an error ocurred trying to save user'}, 500
        return new_user_object.json()
    

class User(Resource):
    """
    # arguments***
    # definindo quais valores poderam ser enviados
    # qualquer informação diferente não é aceita
    arguments = reqparse.RequestParser()
    arguments.add_argument('account_name', type=str, required=True , help="the field 'account_name' cannot be left blank, and use only string")
    arguments.add_argument('title',type=str, required=True,help="the field 'title' cannot be left blank, and use only string")
    arguments.add_argument('account_type', type=int, required=True, help="the field 'account_type' cannot be left blank")
    arguments.add_argument('due_date', type=str, required=False, help="the field 'due_date' cannot be left blank")
    arguments.add_argument('net_value',type=float, required=TRUE,help="the field 'net_value' cannot be left blank, and use only float")
    arguments.add_argument('gross_value',type=float, required=False,help="the field 'gross_value' cannot be left blank, and use only float")
    arguments.add_argument('details',type=str, required=False,help="the field 'details' cannot be left blank, and use only string")
    arguments.add_argument('paid_received',type=int, required=True,help="the field 'paid_received' cannot be left blank, and use only Integer")
    arguments.add_argument('create_date',type=str, required=False,help="the field 'create_date' cannot be left blank, and use only DateTime Format")
    arguments.add_argument('date_release',type=str, required=False,help="the field 'date_release' cannot be left blank, and use only DateTime Format")
    arguments.add_argument('user',type=str, required=True,help="the field 'user' cannot be left blank, and use only string")
    """
    
    def get(self, user_id):
        print(user_id)        
        user = UserModel.find_user(user_id)
        if user:
            return user.json()

        return {'message':'Id not Found'}, 404
    

    """    
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
    """
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurred trying to delete user.'}, 500
            return {'message': 'User Deleted'}
        return {'message': 'User not found.'}, 404
    
class CreateUser(Resource):
    
    def post(self):
        
        data = attributes.parse_args()
        
        if UserModel.find_by_login(data['login']):
            return {"message": "The login'{}'already exists".format(data['login'])}
        
        user = UserModel(**data)
        user.save_user()
        return {'message': 'User created successfully'}, 201


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        data = login_attributes.parse_args()
        
        user = UserModel.find_by_login(data['login'])
        
        # verificando usuário e senha
        if user and safe_str_cmp(user.password, data['password']):
            # se estiver correto, criar token de acesso
            access_token = create_access_token(identity=user.user_id)
            return {'access_token': access_token}, 200
        return {'message': 'The username ou password is incorrect.'}, 401
    
    
class userLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLOCKLIST.add(jwt_id)
        return {'message': 'logged out  successfully'}, 200