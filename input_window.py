import tkinter as tk
class Input:
    """Make choice on cell"""
    #remove choice, make choice

    def __init__(self, parent, cell_id):
        self.parent = parent  # this is an instance of the sudoku class
        self.cell_id = cell_id
        self.cell_id_str = "." + str(self.cell_id)
        self.build()


    def build(self):
        self.root = tk.Tk()
        self.root.title('Input Window')
        self.root.bind('<Return>', self.handle_event)
        # self.root.focus_force()
        self.root.after(1, lambda: self.root.focus_force())
        # self.label = tk.Label(self.root, text="Input num in range(1,9) inclusive")
        # self.label.grid(row=0, column=0, pady=10, padx=10)

        self.choice = tk.StringVar(self.root)

        self.entry = tk.Entry(self.root, textvariable= self.choice)
        # self.entry.grid(row=1,column=0,pady=10,padx=10)
        self.entry.grid(row=0,column=0,pady=10,padx=10)
        self.entry.focus()



        # self.button = tk.Button(self.root, text='Confirm', command=self.handle_choice)
        # self.button.grid(row=3, column=0, pady=10)

        self.root.mainloop()


    def cell_id_to_pos(self):
        y = self.cell_id // 9
        x = self.cell_id - (y*9)

        pos_x,pos_y = self.parent.loc_to_pos(x,y)
        return pos_x, pos_y


    def cell_id_to_loc(self):
        y = self.cell_id // 9
        x = self.cell_id - (y*9)

        return x, y


    def handle_choice(self):
        choice = int(self.choice.get())
        self.root.destroy()

       
   
     
        x,y = self.cell_id_to_loc()
        if choice == self.parent.solution[y][x]:
            self.parent.rect(x,y,"green", self.cell_id)
        else:
            self.parent.rect(x,y,"red", self.cell_id)



        x,y = self.cell_id_to_pos()
        self.parent.draw(x, y, choice, self.cell_id)


        # self.parent.board.delete(self.cell_id_str)


           

    def handle_event(self, event):
        self.handle_choice()
