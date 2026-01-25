import tkinter as tk

from bank_manager import manager

class BankGUI(tk.Tk):
      def __init__(self):
          super().__init__()
          self.title("Welcome to the bank system:")
          self.geometry("500x400")

          self.mgr = manager("bank.json")
          #tk.StringVar()：一个能被 GUI 输入框实时更新的字符串变量
          self.current_name = tk.StringVar()

          #创建一个 空白容器区域(页面）
          container = tk.Frame(self)
          #fill="both":让这个容器 水平 + 垂直方向都填满可用空间
          #expand=True：当窗口变大时，这个 Frame 跟着一起变大
          container.pack(fill = "both", expand = True)

          #创建一个字典，用来保存所有页面对象。
          self.frames = {}
          for F in (HomePage, DepositPage, WithdrawPage, TransferPage):
              #对象
              frame = F(container,self)#固定用法, e.g.frame = DepositPage(container, self)
              self.frames[F.__name__]= frame#e.g. self.frames["HomePage"] = <HomePage对象>
              frame.grid(row=0, column=0, sticky="nsew")
          self.show("HomePage")

      def show(self,page_name):
          self.frames[page_name].tkraise()

      def get_current_account(self):
          name = self.current_name.get().strip()
          if not name:
             print("Warning", "Please enter Account Name")
             return False
          return name

class HomePage(tk.Frame):
      #parent = container app = self
      def __init__(self,parent,app):
          super().__init__(parent)
          self.app = app
          tk.Label(self, text = "Welcome to bank system", font=("Arial", 14)).pack(pady=10)

          row1 = tk.Frame(self)
          row1.pack(pady = 5)
          tk.Label(row1,text = "Name:").pack(side = "left")
          self.new_name = tk.Entry(row1)
          self.new_name.pack(side="left", padx=5)
          tk.Button(row1, text="Create", command=self.create_account).pack(side="left")

          row2 = tk.Frame(self)
          row2.pack(pady=5)
          tk.Label(row2,text = "Account_Name:").pack(side = "left")
          tk.Entry(row2, textvariable = self.app.current_name).pack(side="left")
          tk.Button(row2, text="Login", command=self.login_account).pack(side="left")

          row3 = tk.Frame(self)
          row3.pack(pady=15)
          tk.Button(row3, text="Deposit", width=10, command=lambda: self.app.show("DepositPage")).pack(side="left",
                                                                                                       padx=5)
          tk.Button(row3, text="Withdraw", width=10, command=lambda: self.app.show("WithdrawPage")).pack(side="left",
                                                                                                       padx=5)
          tk.Button(row3, text="Transfer", width=10, command=lambda: self.app.show("TransferPage")).pack(side="left",
                                                                                                       padx=5)
          tk.Button(row3, text="Exit", width=10, command=self.app.destroy).pack(side="left", padx=5)


          #在当前页面上创建一行空白文字显示区域，并把它放到页面上。
          self.info = tk.Label(self,text="")
          self.info.pack()

      def create_account(self):
          name = self.new_name.get().strip()
          ok = self.app.mgr.sign_up(name)
          #config：在程序运行时动态改变控件的内容或外观。
          if ok:
             self.info.config(text = "Account created successfully")
             self.app.current_name.set(name)
          else:
              self.info.config(text="Account already exists")

      def login_account(self):
          name = self.app.current_name.get().strip()

          ok = self.app.mgr.bank_login(name)
          if ok:
              self.app.current_name.set(name)
              self.info.config(text="Login successful")
              self.app.show("HomePage")
          else:
              self.info.config(text="Account not found")


class DepositPage(tk.Frame):
      # parent = container app = self
      def __init__(self, parent, app):
          super().__init__(parent)
          self.app = app
          tk.Label(self, text="Deposit", font=("Arial", 14)).pack(pady=10)

          row1 = tk.Frame(self)
          row1.pack(pady=5)
          tk.Label(row1, text="How much do you want to deposit:").pack(side="left")
          self.amount = tk.Entry(row1)
          self.amount.pack(padx=5)

          # row2 = tk.Frame(self)
          # self.info = tk.Label(row2,text="Your balance is")
          # self.info.pack(padx=5)

          row3 = tk.Frame(self)
          row3.pack(pady=15)
          tk.Button(row3, text="Confirm", command=self.bank_confirm).pack(side="left", padx=5)
          tk.Button(row3, text="Return", command=lambda: self.app.show("HomePage")).pack(side="left",padx=5)

      def bank_confirm(self):
          self.info = tk.Label(self, text="")
          self.info.pack()
          name = self.app.get_current_account()
          money = float(self.amount.get())
          bal = self.app.mgr.bank_deposit(name, money)
          if bal is False:
              self.info.config(text="Account not found.")
          else:
              self.info.config(text=f"Your balance is {bal}")

class WithdrawPage(tk.Frame):
       def __init__(self, parent, app):
            super().__init__(parent)
            self.app = app
            tk.Label(self, text="Withdraw", font=("Arial", 14)).pack(pady=10)

            row1 = tk.Frame(self)
            row1.pack(pady=5)
            tk.Label(row1, text="How much do you want to withdraw:").pack(side="left")
            self.amount = tk.Entry(row1)
            self.amount.pack(padx=5)

            row2 = tk.Frame(self)
            row2.pack(pady=15)
            tk.Button(row2, text="Confirm", command=self.bank_confirm).pack(side="left", padx=5)
            tk.Button(row2, text="Return", command=lambda: self.app.show("HomePage")).pack(side="left", padx=5)

       def bank_confirm(self):
            self.info = tk.Label(self, text="")
            self.info.pack()
            name = self.app.get_current_account()
            money = float(self.amount.get())
            bal = self.app.mgr.bank_withdraw(name, money)
            if bal is False:
                self.info.config(text="Sorry! This is not allowed.")
            else:
                self.info.config(text=f"Your balance is {bal}")

class TransferPage(tk.Frame):
        def __init__(self, parent, app):
            super().__init__(parent)
            self.app = app
            tk.Label(self, text="Transfer", font=("Arial", 14)).pack(pady=10)

            row1 = tk.Frame(self)
            row1.pack(pady=5)
            tk.Label(row1, text="Who do you want to Transfer:").pack(side="left")
            self.to_name = tk.Entry(row1)
            self.to_name.pack(padx=5)

            row2 = tk.Frame(self)
            row2.pack(pady=5)
            tk.Label(row2, text="How much do you want to Transfer:").pack(side="left")
            self.amount = tk.Entry(row2)
            self.amount.pack(padx=5)

            row3 = tk.Frame(self)
            row3.pack(pady=15)
            tk.Button(row3, text="Confirm", command=self.bank_confirm).pack(side="left", padx=5)
            tk.Button(row3, text="Return", command=lambda: self.app.show("HomePage")).pack(side="left", padx=5)

        def bank_confirm(self):
            self.info = tk.Label(self, text="")
            self.info.pack()

            for_name = self.app.get_current_account()
            to_name = self.to_name.get().strip()
            money = float(self.amount.get())

            result = self.app.mgr.bank_transfer(money,for_name,to_name)

            if result is False:
                self.info.config(text=f"Sorry! This is not allowed.")
            else:
                sender_bal,receiver_bal = result
                self.info.config(text=f"Your balance is {sender_bal}\n{to_name} balance is {receiver_bal}")


if __name__ == "__main__":
    BankGUI().mainloop()
