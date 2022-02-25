from create_db import database
from datetime import datetime
from json import dumps

class converter():
    
    def defaultconverter(o):
          if isinstance(o, datetime):
            return o.__str__()

class UserModel(database.Model):
    
    __tablename__ = 'users' # definindo nome na tabela do DB
    
    user_id = database.Column(database.Integer, primary_key=True)
    user_name = database.Column(database.String(100), nullable=False)
    login = database.Column(database.String(50), nullable=False)
    password = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    create_date = database.Column(database.String(30), nullable=False)
    admin = database.Column(database.Boolean, default=False, server_default="false") #1 or 0
 
    #construtor
    def __init__(self,user_name, login, password, email, create_date, admin):
   
        self.user_name = user_name
        self.login = login
        self.password = password
        self.email = email
        self.create_date = dumps(datetime.now(),default = converter.defaultconverter)
        self.admin = int(admin)
                
        
    #JSON
    def json(self):
        return{
        'user_id': self.user_id,
        'user_name': self.user_name,
        'password': self.password,
        'email': self.email,
        'create_date' : self.create_date,
        'admin' : self.admin
        }  
    
    @classmethod    
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls,login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    def save_user(self):
        database.session.add(self)
        database.session.commit()
        
    def update_user(self,user_name ,password, email, create_date, admin):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.create_date = create_date
        self.admin = admin
        
    def delete_user(self):
        database.session.delete(self)
        database.session.commit()
        