# importing the necessary imports
import tkinter as tk
from calculator_logic import CalculatorLogic

# using OOP to make a class for easy use
class CalculatorApp:
    def __init__(self, root):
        #Save the main window object
        self.root = root
        #create computational logic objects
        self.logic = CalculatorLogic()
        # setting the window size and title
        self.root.title("Calculator")
        self.root.geometry("500x700")
        # creating the welcome page and having a button in the middle of the page to go to the main calculator page
        self.label = tk.Label(root, text="WELCOME!", font=("Times New Roman", 26))
        self.label.pack(pady=50)
        self.welcome_button = tk.Button(root, text="Click Here", command=self.clear_screen)
        self.welcome_button.pack()
        # this is to edit the design and color of the page
        self.root.configure(bg="#FAF6F7")
        self.label.configure(bg="#FFA2B9", fg="#FFD1DC")
        self.welcome_button.configure(bg="#FFA2B9", fg="#FFD1DC")

    # this is a method that clears the first page to show the second page
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # this is the layout of the second page
        self.display = tk.Entry(self.root, font=('Times New Roman', 20), justify='right')
        self.display.grid(row=0, column=0, columnspan=5, sticky="nsew")

        buttons = [
            'AC', '²', '√', 'arcsin', 'sin',
            '7', '8', '9', 'arccos', 'cos',
            '4', '5', '6', 'arctan', 'tan',
            '1', '2', '3', '+', '-',
            '.', '0', '^', 'x', '÷',
            'Exit', '⌫', '(', ')', '='
        ]

        #through loop to create button
        row, col = 1, 0
        for b in buttons:
            btn = tk.Button(
                self.root,
                text=b,
                font=('Times New Roman', 20),
                command=lambda x=b: self.on_click(x)
            )
            # Each button press moves the character one space to the right.
            btn.grid(row=row, column=col, sticky="nsew")
            col += 1
            # If there are more than 5 buttons on a line, wrap to a new line
            if col > 4:
                col = 0
                row += 1

        # configure the grid to expand properly
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(7):# Increased to 7 rows to accommodate all buttons
            self.root.grid_rowconfigure(i, weight=1)

    def on_click(self, text):
        # Clear error message on any button press
        if self.display.get() == "Error":
            self.display.delete(0, tk.END)
            # Handle button clicks for numbers and basic operations
        if text == "AC":
            self.display.delete(0, tk.END)

        elif text == "=":
            try:
                # Evaluate the expression in the display
                result = self.logic.evaluate(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")

        elif text == "⌫":
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current[:-1])

        elif text == "Exit":
            self.root.quit()

        elif text == "^":
            self.display.insert(tk.END, "**")

        else:
            # Append the button text to the display
            self.display.insert(tk.END, text)


if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()