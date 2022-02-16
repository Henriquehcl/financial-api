from create_db import database
from sqlalchemy.sql import func

class AccountModel(database.Model):
    
    __tablename__ = 'accounts' # definindo nome na tabela do DB
    
    account_id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(50), nullable=False)
    net_value = database.Column(database.Float, nullable=True)
    gross_value = database.Column(database.Float, nullable=False)
    details = database.Column(database.String(500), nullable=True)
    paid_received = database.Column(database.Boolean, nullable=True)
    create_date = database.Column(database.DateTime(timezone=True), server_default=func.now())
    date_release = database.Column(database.Date, nullable=True)
    user = database.Column(database.String(50),nullable=False)
    
    
    #construtor
    def __init__(self,account_id,title,net_value, gross_value, details, paid_received, create_date,date_release,user):
        self.account_id = account_id
        self.title = title
        self.net_value = net_value
        self.gross_value = gross_value
        self.details = details
        self.paid_received = paid_received
        self.create_date = create_date
        self.date_release = date_release
        self.user = user
        
    #JSON
    def json(self):
        return{
        'account_id': self.account_id,
        'conta': self.conta,
        'data': self.data,
        'valor': self.valor
        }  
        