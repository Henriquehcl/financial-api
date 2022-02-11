class AccountModel:
    
    #construtor
    def __init__(self,account_id,conta,data,valor):
        self.account_id = account_id
        self.conta = conta
        self.data = data
        self.valor = valor
        
    #JSON
    def json(self):
        return{
        'account_id': self.account_id,
        'conta': self.conta,
        'data': self.data,
        'valor': self.valor
        }  
        