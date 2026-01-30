class Member:
      def __init__(self,name,book):
          self.name = name
          self.book = book

      #Creat a dictionary
      def to_book_dict(self):
          return{
              "name": self.name,
              "book": self.book
          }