import tkinter as tk
from input_window import Input
class Choice:
    """Make choice on cell"""
    #remove choice, make choice

    def __init__(self, parent, cell_id):
        self.parent = parent  # this is an instance of the sudoku class
        self.cell_id = cell_id
        self.cell_id_str = "." + str(self.cell_id)
        self.build()


    def build(self):
        self.root = tk.Tk()
        self.root.title('Cell Options')
        self.root.bind('<Return>', self.handle_event)
        self.label = tk.Label(self.root, text="Make a Choice")
        self.label.grid(row=0, column=0, pady=10, padx=10)

        self.choice = tk.IntVar(self.root)

        self.rbtn1 = tk.Radiobutton(self.root, text="Remove Choice (if any)", variable=self.choice, value=0)
        self.rbtn1.grid(row=1, column=0)

        self.rbtn2 = tk.Radiobutton(self.root, text="Make Choice", variable=self.choice, value=1)
        self.rbtn2.grid(row=2, column=0)

        self.button = tk.Button(self.root, text='Confirm', command=self.handle_choice)
        self.button.grid(row=3, column=0, pady=10)

        self.root.mainloop()

    def handle_choice(self):
        self.choice = self.choice.get()
        self.root.destroy()

        if self.choice == 0: #remove choice
           

        else: #make choice
            Input(self.parent, self.cell_id)

           

    def handle_event(self, event):
        self.handle_choice()
