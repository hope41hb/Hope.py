class bank_account:
      def __init__(self, name, balance):
          self.name = name
          self.balance = balance

      def bank_to_dict(self):
          return{
              "name": self.name,
              "balance": self.balance,
          }
