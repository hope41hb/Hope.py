# importing the necessary  imports
import tkinter as tk
import math
import re


# using OOP to make a class for easy use
class CalculatorApp:
    def __init__(self, root):
        # setting the window size and title
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("500x700")
        # creating the welcome page and having a button in the middle of the page to go to the main calculator page
        self.label = tk.Label(self.root, text="WELCOME!", font=("Times New Roman", 26))
        self.label.pack(pady=50)
        self.welcome_button = tk.Button(self.root, text="Click Here", command=self.clear_screen)
        self.welcome_button.pack()
        # this is to edit the design and colour of the page
        self.root.configure(bg="#FAF6F7")
        self.label.configure(bg="#FFA2B9", fg="#FFD1DC")
        self.welcome_button.configure(bg="#FFA2B9", fg="#FFD1DC")

    # this is a method that clears the first page to show the second page
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        # this is the layout of the second page
        self.display = self.create_display(self.root)

        buttons = [
            'AC', '²', '√', '^', 'sin',
            '7', '8', '9', 'log', 'cos',
            '4', '5', '6', 'ln', 'tan',
            '1', '2', '3', '+', '-',
            '.', '0', '00', 'x', '÷',
            'Exit', '⌫', '(', ')', '='
        ]

        # create and place the buttons and its color
        self.create_buttons(self.root, buttons)
        self.configure_grid(self.root)
        self.display.configure(bg="#FAF6F7", fg="#FFD1DC")

        # update button text colour
        for child in self.root.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(bg="#FFA2B9", fg="#F83B72")

    # create and place the buttons in the grid
    def create_display(self, root):
        display = tk.Entry(root, font=('Times New Roman', 20), justify='right')
        display.grid(row=0, column=0, columnspan=5, sticky="nsew")
        return display

    # this is to activate the buttons for the following actions
    def create_buttons(self, root, buttons):
        row_val, col_val = 1, 0
        for button in buttons:
            if button in ['sin', 'cos', 'tan', 'log', 'ln']:
                btn = tk.Button(root, text=button, font=('Times New Roman', 20), padx=20, pady=20,
                                command=lambda b=button: self.append_function(b))
            else:
                btn = tk.Button(root, text=button, font=('Times New Roman', 20), padx=20, pady=20,
                                command=lambda b=button: self.on_button_click(b))
            #Each button press moves the character one space to the right.
            btn.grid(row=row_val, column=col_val, sticky="nsew")
            col_val += 1
            #If there are more than 5 buttons on a line, wrap to a new line
            if col_val > 4:
                col_val = 0
                row_val += 1

    def configure_grid(self, root):
        # configure the grid to expand properly
        for i in range(5):
            root.grid_columnconfigure(i, weight=1)
        for i in range(7):  # Increased to 7 rows to accommodate all buttons
            root.grid_rowconfigure(i, weight=1)

    def on_button_click(self, button_text):
        # Clear error message on any button press
        if self.display.get() == "Error":
            self.display.delete(0, tk.END)
            # Handle button clicks for numbers and basic operations
        if button_text == 'AC':
            self.display.delete(0, tk.END)
        elif button_text == '=':
            try:
                # Evaluate the expression in the display
                expression = self.display.get()
                result = self.evaluate_expression(expression)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif button_text == '⌫':
            current_text = self.display.get()
            if current_text:
                self.display.delete(len(current_text) - 1, tk.END)
        elif button_text == '.':
            self.display.insert(tk.END, ".")
        elif button_text == 'Exit':
            self.root.quit()
        elif button_text == '^':
            self.display.insert(tk.END, "**")
        else:
            # Append the button text to the display
            self.display.insert(tk.END, button_text)

    def append_function(self, func):
        # Insert function name without parentheses
        self.display.insert(tk.END, func)

    def evaluate_expression(self, expression):
        # handle basic operations and symbols
        expression = expression.replace("x", "*").replace("÷", "/")
        expression = expression.replace("²", "**2")

        # handle square roots with both √number and number√ formats
        expression = re.sub(r'√(\d+(\.\d+)?)', r'math.sqrt(\1)', expression)
        expression = re.sub(r'(\d+(\.\d+)?)√', r'math.sqrt(\1)', expression)

        # handle complex square roots with parentheses
        expression = re.sub(r'√\(([^)]+)\)', r'math.sqrt(\1)', expression)

        # handle mathematical functions
        expression = expression.replace("sin", "math.sin(math.radians")
        expression = expression.replace("cos", "math.cos(math.radians")
        expression = expression.replace("tan", "math.tan(math.radians")
        expression = expression.replace("log", "math.log10")
        expression = expression.replace("ln", "math.log")


        # add closing parentheses for trigonometric functions
        for func in ["sin", "cos", "tan"]:
            if func in expression:
                expression += ")"

        return eval(expression, {"math": math})


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
