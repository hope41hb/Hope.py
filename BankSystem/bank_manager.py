import json
from Bank_account import bank_account

class manager:
      def __init__(self,file_name = "bank.json"):
          self.bank_tasks = []
          self.filename = file_name
          self.load()

      def sign_up(self,name):
          name =name.strip()
          if not name:
             return False

          for account in self.bank_tasks:
              if account.name == name:
                  return False

          account = bank_account(name,0)
          self.bank_tasks.append(account)
          self.save()
          return True

      def bank_login(self,name):
          for Bank_account in self.bank_tasks:
              if Bank_account.name == name:
                 return True
          return False

      def bank_deposit(self,name,money):
          for Bank_account in self.bank_tasks:
              if Bank_account.name == name:
                 Bank_account.balance += money
                 self.save()
                 return Bank_account.balance
          return False

      def bank_withdraw(self,name,money):
          for Bank_account in self.bank_tasks:
              if Bank_account.name == name:
                  if Bank_account.balance - money < -1500:
                     return False
                  Bank_account.balance -= money
                  self.save()
                  return Bank_account.balance
          return False

      def bank_transfer(self,money,from_id,to_id):
          sender = None
          receiver = None
          for account in self.bank_tasks:
              if account.name == from_id:
                 #sender:对象，人名
                 sender = account
              if account.name == to_id:
                 receiver = account
          if sender is None or receiver is None:
              return False
          if sender.balance - money >= -1500:
              sender.balance -= money
              receiver.balance += money
              self.save()
          return sender.balance,receiver.balance

      def save(self):
          with open(self.filename, "w") as f:
              json.dump([t.bank_to_dict() for t in self.bank_tasks], f, indent=4)

      def load(self):
          try:
              with open(self.filename, "r") as f:
                  data = json.load(f)
                  self.bank_tasks = [bank_account(**d) for d in data]
          except:
              self.bank_tasks = []
