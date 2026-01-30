import json
from library_member import Member 

class Book:
      def __init__(self,file_name = "library.json"):
          self.filename = file_name
          #一个空字典
          self.library_tasks = []
          self.load()

          # Initialize books
          self.library_book = [
              "To Kill a Mockingbird",
              "1984",
              "Pride and Prejudice",
              "The Great Gatsby",
              "Harry Potter and the Philosopher’s Stone",
              "The Catcher in the Rye",
              "The Alchemist",
              "Atomic Habits",
              "The Little Prince",
              "Sapiens: A Brief History of Humankind"
          ]

      def book_sign_up(self,name):
          #把名字改成小写，不要空格
          name = name.strip().lower()
          #如果为空
          if not name:
             status = 1
             return status
          #如果存在
          for browser in self.library_tasks:
              if browser.name == name:
                  status = 2
                  return status
          #添加名字
          self.library_tasks.append(Member(name, []))
          self.save()
          status = 3
          return status

      def login(self,name):
          name = name.strip().lower()
          for browser in self.library_tasks:
              #如果找到名字，return True
              if browser.name == name:
                 return True
          self.save()
          #如果没找到名字
          return False

      def borrow(self, name, book_title):
          name = name.strip().lower()
          book_browsed = book_title.strip().lower()

          # 找到这个用户对象
          member = None
          for m in self.library_tasks:
              if m.name == name:
                  member = m
                  break
          if member is None:
              return False
          # 找到书并移动
          for book in list(self.library_book):
              if book.lower() == book_browsed:
                  self.library_book.remove(book)
                  member.book.append(book)  # 写入 member.book
                  self.save()
                  return True

              if book in member.book:
                  return False

          return False

      def return_book(self,name,book_title):
          name = name.strip().lower()
          book_title = book_title.strip().lower()

          # 找到这个用户对象
          member = None
          for m in self.library_tasks:
              if m.name == name:
                  member = m
                  break
          if member is None:
              return False

          # 找到这本书（在 member.book 里）
          target = None
          for b in member.book:
              if b.lower() == book_title:
                  target = b
                  break
          if target is None:
              return False  # 这个人没借这本书

          # 执行归还
          member.book.remove(target)
          self.library_book.append(target)

          self.save()
          return True

      def get_all_books_status(self):
          rows = []

          # 先收集所有已借出的书
          borrowed = {}  # key: normalized title(original_title, borrower_name)
          for member in self.library_tasks:
              for b in member.book:
                  key = b.strip().lower()
                  borrowed[key] = (b, member.name)

          # 显示 Available：只显示那些“不在 borrowed 里”的馆藏书
          for b in self.library_book:
              key = b.strip().lower()
              if key not in borrowed:
                  rows.append((b, "Available"))

          # 显示 Borrowed：显示所有借出书
          for title, borrower in borrowed.items():
              rows.append((title, f"Borrowed by {borrower}"))

          return rows


      def save(self):#存档
          #写入模式 "w"。 f 就是这个文件对象。
          with open(self.filename, "w") as f:
               #把所有 Task 对象转成普通字典列表。
               #json.dump：把字典列表写入文件 f（tasks.json
               json.dump([t.to_book_dict() for t in self.library_tasks], f, indent = 4)

      def load(self):#读档
          try:
              with open(self.filename,"r") as f:
                   #把 JSON 文件里的内容读出来，变成 Python 数据结构。
                   data = json.load(f)
                   #task(**d):**d 会把字典的 key-value 当作参数传入
                   #把 JSON 字典重新变回 task 对象列表
                   self.library_tasks = [Member(**d) for d in data]
         #如果文件不存在，或者内容损坏，就创建空任务列表。
          except:
              self.library_tasks = []
