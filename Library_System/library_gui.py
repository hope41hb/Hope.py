import tkinter as tk
from book_manager import Book


class LibraryGUI(tk.Tk):
      def __init__(self):
          super().__init__()
          self.title("Library System")
          self.geometry("500x400")
          self.file = Book("library.json")

          self.current_user = None

          # 创建一个 空白容器区域(页面）
          container = tk.Frame(self)
          # fill="both":让这个容器 水平 + 垂直方向都填满可用空间
          # expand=True：当窗口变大时，这个 Frame 跟着一起变大
          container.pack(fill="both", expand=True)

          # 创建一个字典，用来保存所有页面对象。
          self.frames = {}
          for F in (HomePage,BorrowPage, ReturnPage, ShowPage):
              # 对象
              frame = F(container, self)  # 固定用法, e.g.frame = HomePage(container, self)
              self.frames[F.__name__] = frame  # e.g. self.frames["HomePage"] = <HomePage对象>
              frame.grid(row=0, column=0, sticky="nsew")
          self.show("HomePage")

      def show(self,show_page):
          #取出对应的页面对象 tkraise:把这一页翻到最前面
          self.frames[show_page].tkraise()


class HomePage(tk.Frame):
    # parent = container app = self
      def __init__(self, parent, app):
          super().__init__(parent)
          self.app = app
          tk.Label(self, text="Welcome to library system", font=("Arial", 14)).pack(pady=10)


          row1 = tk.Frame(self)
          row1.pack(pady=5)
          tk.Button(row1, text="Sign up", command=self.create_account).pack(side="left")
          self.new_name = tk.Entry(row1)
          self.new_name.pack(side="left", padx=5)

          row2 = tk.Frame(self)
          row2.pack(pady=5)
          tk.Button(row2, text="login", command=self.login_account).pack(side="left")
          self.new_name2 = tk.Entry(row2)
          self.new_name2.pack(side="left", padx=5)

          row3 = tk.Frame(self)
          row3.pack(pady=15)
          tk.Button(row3, text="Borrow", width=10, command=lambda: self.app.show("BorrowPage")).pack(side="left",
                                                                                                       padx=5)
          tk.Button(row3, text="Return", width=10, command=lambda: self.app.show("ReturnPage")).pack(side="left",
                                                                                                         padx=5)
          tk.Button(row3, text="ShowAll", width=10, command=lambda: self.app.show("ShowPage")).pack(side="left",
                                                                                                         padx=5)
          tk.Button(row3, text="Exit", width=10, command=self.app.destroy).pack(side="left", padx=5)

          self.info = tk.Label(self,text="")
          self.info.pack()

      def create_account(self):
          name = self.new_name.get().strip()
          status = self.app.file.book_sign_up(name)
          # config：在程序运行时动态改变控件的内容或外观。
          if status == 3:
              self.info.config(text="Account created successfully")
          elif status == 2:
              self.info.config(text="Account already exists")
          elif status == 1:
              self.info.config(text="Account can be empty")

      def login_account(self):
          name = self.new_name2.get().strip()
          ok = self.app.file.login(name)
          if ok:
              self.app.current_user = name
              self.info.config(text="Login successful")
              self.app.show("HomePage")
          else:
              self.info.config(text="Account not found")


class BorrowPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        tk.Label(self, text="Borrow", font=("Arial", 14)).pack(pady=10)

        row1 = tk.Frame(self)
        row1.pack(pady=5)
        tk.Label(row1, text="Which book do you want to borrow:").pack(side="left")
        self.borrowed_book = tk.Entry(row1)
        self.borrowed_book.pack(side="left", padx=5)
        tk.Button(row1, text="Add", command=self.borrow_book).pack(side="left")

        row2 = tk.Frame(self)
        row2.pack(pady=15)
        tk.Button(row2, text="Return", command=lambda: self.app.show("HomePage")).pack(side="left", padx=5)

        self.info = tk.Label(self, text="")
        self.info.pack()

    def borrow_book(self):
        book = self.borrowed_book.get().strip()
        ok = self.app.file.borrow(self.app.current_user,book)
        if ok:
            self.info.config(text="Borrow successful")
        else:
            self.info.config(text="Borrow failed")


class ReturnPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        tk.Label(self, text="Borrow", font=("Arial", 14)).pack(pady=10)

        row1 = tk.Frame(self)
        row1.pack(pady=5)
        tk.Label(row1, text="Which book do you want to return:").pack(side="left")
        self.return_book = tk.Entry(row1)
        self.return_book.pack(side="left", padx=5)
        tk.Button(row1, text="Return", command=self.book_return).pack(side="left")

        row2 = tk.Frame(self)
        row2.pack(pady=15)
        tk.Button(row2, text="Return", command=lambda: self.app.show("HomePage")).pack(side="left", padx=5)

        self.info = tk.Label(self, text="")
        self.info.pack()

    def book_return(self):
        book = self.return_book.get().strip()
        ok = self.app.file.return_book(self.app.current_user,book)
        if ok:
            self.info.config(text="Return successful")
        else:
            self.info.config(text="Book not found")


class ShowPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        tk.Label(self, text="Show_all_books_status", font=("Arial", 14)).pack(pady=10)

        row2 = tk.Frame(self)
        row2.pack(pady=15)
        tk.Button(row2, text="Show", command=self.refresh).pack(side="left")

        self.text = tk.Text(self, width=40, height=12, font=("Consolas", 16))
        self.text.pack(pady=10)

        row1 = tk.Frame(self)
        row1.pack(pady=15)
        tk.Button(row1, text="Return", command=lambda: self.app.show("HomePage")).pack(side="left", padx=5)

    def refresh(self):
        self.text.delete("1.0", "end")
        rows = self.app.file.get_all_books_status()
        for title,status in rows:
            self.text.insert("end",f"{title}  {status}\n")


if __name__ == "__main__":
    LibraryGUI().mainloop()