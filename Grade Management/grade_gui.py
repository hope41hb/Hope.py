import tkinter as tk
#from grade_logic this file import GradeManager this class
from grade_logic import GradeManager
#Pop-up notification to user
from tkinter import messagebox

class GradeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grade Management")
        self.geometry("400x300")

        #Create an object from the GradeManager() class
        self.manager = GradeManager()

        #Store all "frames" in a dictionary
        self.frames = {}
        #Traverse all page classes
        for Page in (MenuPage, AddPage, DeletePage, AvgPage):
            #Page(self): Create a page object
            frame = Page(self)#e.g frame = MenuPage(self)
            #Store the page in a dictionary
            self.frames[Page] = frame
            frame.place(relwidth=1, relheight=1)

        #When the program starts, the main menu page is displayed first
        self.show_frame(MenuPage)

    #Show the page I specified
    def show_frame(self, page):
        self.frames[page].tkraise()

class MenuPage(tk.Frame):#Layout
    def __init__(self, app):
        super().__init__(app)

        tk.Label(self, text="Grade Management", font=("Arial", 16)).pack(pady=20)

        tk.Button(self, text="ADD",
                  command=lambda: app.show_frame(AddPage)).pack(pady=5)

        tk.Button(self, text="AVG / LV",
                  command=lambda: app.show_frame(AvgPage)).pack(pady=5)

        tk.Button(self, text="Delete",
                  command=lambda: app.show_frame(DeletePage)).pack(pady=5)

        tk.Button(self, text="Exit",
                  command=app.quit).pack(pady=5)

class AddPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        tk.Label(self, text="Student name").grid(row=0, column=0)
        tk.Label(self, text="Math").grid(row=1, column=0)
        tk.Label(self, text="CS").grid(row=2, column=0)
        tk.Label(self, text="Physics").grid(row=3, column=0)

        #Entry: Allow users to input content
        self.name = tk.Entry(self)
        self.math = tk.Entry(self)
        self.cs = tk.Entry(self)
        self.phy = tk.Entry(self)

        #grid: Arrange in a "table" format
        self.name.grid(row=0, column=1)
        self.math.grid(row=1, column=1)
        self.cs.grid(row=2, column=1)
        self.phy.grid(row=3, column=1)

        #Command: Function to be executed after clicking the button
        tk.Button(self, text="Save", command=self.save).grid(row=4, column=0)
        tk.Button(self, text="Return",
                  command=lambda: app.show_frame(MenuPage)).grid(row=4, column=1)#Return to the main page

    def save(self):
        self.app.manager.add_student(
            self.name.get(),#Read student name
            float(self.math.get()),#Read the content (string) from the Math input box and convert it to a float
            float(self.cs.get()),#Computer Science
            float(self.phy.get())#Physics
        )

class DeletePage(tk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        tk.Label(self, text="Student name").pack(pady=10)
        self.name = tk.Entry(self)
        self.name.pack()

        tk.Button(self, text="Delete", command=self.delete).pack(pady=5)#Call “delete” this object
        tk.Button(self, text="Return",
                  command=lambda: app.show_frame(MenuPage)).pack(pady=5)#Return to the main page

    def delete(self):
        #From "GradeManager" this class call "delete_student" this object to get the student name
        name = self.name.get().strip()
        ok = self.app.manager.delete_student(name)#call the delete_student this method name
        if ok:#if it has
           messagebox.showinfo("Success", "Student has been deleted.")
        else:#if it doesn't has
           messagebox.showerror("Error", "Student not found.")

class AvgPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

       #Layout
        tk.Label(self, text="Student name").grid(row=0, column=0)
        self.name = tk.Entry(self)
        self.name.grid(row=0, column=1)

        tk.Button(self, text="Check", command=self.check).grid(
            row=1, column=0, columnspan=2)

        self.avg_label = tk.Label(self, text="Average:")
        self.avg_label.grid(row=2, column=0, columnspan=2)

        self.level_label = tk.Label(self, text="Level:")
        self.level_label.grid(row=3, column=0, columnspan=2)

        self.Con_label = tk.Label(self, text="Condition:")
        self.Con_label.grid(row=4, column=0, columnspan=2)

        #return to the main page
        tk.Button(self, text="Return",
                  command=lambda: app.show_frame(MenuPage)).grid(
            row=5, column=0, columnspan=2)

    def check(self):
        # From "GradeManager" this class call "get_average_and_level" this object to get the student name
        avg, level = self.app.manager.get_average_and_level(self.name.get())
        if avg is not None:#If the average mark is valid
            self.avg_label.config(text=f"Average: {avg:.2f}")#Round to two decimal places
            self.level_label.config(text=f"Level: {level}")#config:modify its parameters
            self.Con_label.config(text=f"Condition:Student is exists")
        else:# if the student no longer exists
            self.avg_label.config(text="")
            self.level_label.config(text="")
            self.Con_label.config(text=f"Condition:Student no longer exists")

if __name__ =="__main__":
    app = GradeApp()
    app.mainloop()