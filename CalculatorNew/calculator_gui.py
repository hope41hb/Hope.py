import tkinter as tk
from calculator_logic import CalculatorLogic

#main class responsible for the calculator graphical user interface
class CalculatorGUI:
    def __init__(self, root):
        #set up the main window
        self.root = root
        self.root.title('Scientific Calculator')
        self.root.geometry('500x750')
        self.root.resizable(False, False)
        
        #creat the calculator logic 
        self.logic = CalculatorLogic()
        self.just_calculated = False

        #display where the numbers and results are shown
        self.display = tk.Entry(
            root,
            font=('Arial', 18),
            borderwidth=5,
            relief='ridge',
            justify='right'
        )
        #make the display stretch across the window
        self.display.pack(fill='x', padx=10, pady=10, ipady=10)
        #frame to hold all calculator buttons
        button_frame = tk.Frame(root)
        button_frame.pack()
        #list of buttons with their position on the grid
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('x', 2, 3), 
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            
            ('sin(', 5, 0), ('cos(', 5, 1), ('tan(', 5, 2), ('√(', 5, 3),
            ('arcsin(', 6, 0), ('arccos(', 6, 1), ('arctan(', 6, 2), ('^', 6, 3),
            ('(', 7, 0), (')', 7, 1), ("²", 7, 2), ("⌫", 7, 3),
            ('AC', 8, 0)
            ]
        #create each button and place it on the screen
        for (text, row, col) in buttons:
            tk.Button(
                button_frame,
                text=text,
                width=8,
                height=2,
                font=('Arial', 12),
                #when a button is clicked, call the on_click function
                command=lambda t=text: self.on_click(t)
                ).grid(row=row, column=col, padx=4, pady=4)
    #this function runs when any button is clicked       
    def on_click(self, text):
        #if error is shown it clears it before doing anything else 
        if self.display.get() == 'Error':
            self.display.delete(0, tk.END)
        #clear everything when any AC is pressed
        if text == 'AC':
            self.display.delete(0, tk.END)
            self.just_calculated = False
        #calculate the result when = is pressed
        elif text == '=':
            try:
              #send the text in the display to the logic part
              result = self.logic.evaluate(self.display.get())
              self.display.delete(0, tk.END)
              self.display.insert(0, result)
              self.just_calculated = False
            except:
              #show "Error" if something goes wrong
              self.display.delete(0, tk.END)
              self.display.insert(0, 'Error')
        #remove the last character when backspace is pressed
        elif text == "⌫":
          current = self.display.get()
          self.display.delete(0, tk.END)
          self.display.insert(0, current[:-1])
        #add numbers, symbols, or functions to the display
        else:
          if self.just_calculated:
              self.display.delete(0, tk.END)
              self.just_calculated = False
          self.display.insert(tk.END, text)
          

#start the calculator program            
if __name__ == '__main__':
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()
            
        
