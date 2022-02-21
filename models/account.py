from create_db import database
from datetime import datetime
from json import dumps

class converter():
    
    def defaultconverter(o):
          if isinstance(o, datetime):
            return o.__str__()

class AccountModel(database.Model):
    
    __tablename__ = 'accounts' # definindo nome na tabela do DB
    
    account_id = database.Column(database.Integer, primary_key=True)
    account_name = database.Column(database.String(50), nullable=False)
    title = database.Column(database.String(50), nullable=False)
    net_value = database.Column(database.Float, nullable=True)
    gross_value = database.Column(database.Float, nullable=False)
    details = database.Column(database.String(500), nullable=True)
    paid_received = database.Column(database.Boolean, default=False, server_default="false")
    # create_date = database.Column(database.DateTime(timezone=True))
    create_date = database.Column(database.String(30), nullable=False)
    date_release = database.Column(database.String(30), nullable=True)
    user = database.Column(database.String(50),nullable=False)
    
    
 
    #construtor
    def __init__(self,account_name,title,net_value, gross_value, details, paid_received,create_date, date_release,user):
   
        #self.account_id = account_id
        self.account_name = account_name
        self.title = title
        self.net_value = net_value
        self.gross_value = gross_value
        self.details = details
        self.paid_received = int(paid_received)
        #self.create_date = dumps(datetime.now(),default = converter.defaultconverter)
        self.create_date = dumps(datetime.now(),default = converter.defaultconverter)
        self.date_release = date_release
        self.user = user
        
        
    #JSON
    def json(self):
        return{
        'account_id': self.account_id,
        'account_name': self.account_name,
        'title': self.title,
        'net_value': self.net_value,
        'gross_value': self.gross_value,
        'details': self.details,
        'paid_received': self.paid_received,
        'create_date' : self.create_date,
        'date_release' : self.date_release,
        'user': self.user
        }  
    
    @classmethod    
    def find_account(cls, account_id):
        account = cls.query.filter_by(account_id=account_id).first()
        if account:
            return account
        return None
    
    def save_account(self):
        database.session.add(self)
        database.session.commit()
        
    def update_account(self,account_name ,title, net_value, gross_value, details, paid_received,create_date, date_release, user):
        self.account_name = account_name
        self.title = title
        self.net_value = net_value
        self.gross_value = gross_value
        self.details = details
        self.paid_received = int(paid_received)
        self.create_date = create_date
        self.date_release = date_release
        self.user = user
        
    def delete_account(self):
        database.session.delete(self)
        database.session.commit()
        