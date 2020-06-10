import tkinter as tk
import random
import copy
from input_window import Input
from tkinter import messagebox

class Sudoku:
    def __init__(self, mode, difficulty):
        if mode == 'debug':
            self.gen_puzzle()
            

        else:

            self.width, self.height = 800,800
            self.difficulty = difficulty
            self.linewd_sm, self.linewidth_bg = 3,7
            self.game = [[[None for i in range(3)] for i in range(3)] for i in range(9)]
            self.cellsize =  self.width // 9
            self.solution = []
            self.build()



    def build(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height+100}")
        # self.root.resizable(width=False, height=False)
         


        self.board = tk.Canvas(self.root,width=self.width, height=self.height)
        self.board.pack()
        self.board.bind("<Button-1>", self.handle_button1)
        self.board.bind("<Button-3>", self.handle_button3) 

        self.solve_btn =  tk.Button(self.root, text='Solve', command=self.solve)
        self.solve_btn.pack()

        self.gen_lines()
        self.make_puzzle()

        self.root.mainloop()


    def gen_lines_recursive(self, x, y, length,width):
        step = length // 3
        pos = [step*i for i in range(1,3)]

        #main grid lines
        for i in range(2):
            self.board.create_line(x, y+pos[i], x+length, y+pos[i], width=width) #horizontal lines
            self.board.create_line(x+pos[i],y,x+pos[i], y+length, width= width) #vertical lines
    
    def gen_lines(self):

        self.gen_lines_recursive(0,0, self.width, self.linewidth_bg)

        tlc = {} #idx to pos
        for y in range(3):
            for x in range(3):
                tlc[y*3+x] = [y,x] 
        
        # print(tlc)

        small_step  = self.width//3
        for i in range(9):
            y,x = [idx*small_step for idx in tlc[i]]
            self.gen_lines_recursive(x, y, small_step, self.linewd_sm)

    def pos_to_loc(self, x, y):
        loc_x = x// self.cellsize
        loc_y = y// self.cellsize
        return loc_x, loc_y

    def loc_to_pos(self, x, y):
        pos_x, pos_y = x*self.cellsize, y*self.cellsize
        #center positions
        pos_x += self.cellsize // 2
        pos_y += self.cellsize // 2

        return pos_x, pos_y


    def loc_to_pos_rect(self, x, y):
        cellsize = (self.width - 40) // 9

        pos_x, pos_y = x*cellsize, y*cellsize
        #center positions
        pos_x += cellsize // 2
        pos_y += cellsize // 2

        return pos_x, pos_y
        


    def flatten(self,arr):
        return [j for j in i for i in arr]

    def reshape(self, arr, step=3):
        #converts a 1d array to a 2d array, each row of size step, provided step*2 values
        ls = []
        for i in range(step):
            ls.append([j for j in arr[step*i:step*i+step] ] )

        return ls


    def shift_ls(self, ls, shift):

        #shifts flattened array
        for _ in range(shift):
           left = ls.pop(0)
           ls.append(left)

        return ls


    def gen_puzzle(self):
        seed_nums = [i for i in range(1,10)]
        random.shuffle(seed_nums)

        puzzle = []
        shift_vals  = [0,3,3,1,3,3,1,3,3]
        for idx in shift_vals:
           
            seed_nums = self.shift_ls(seed_nums, idx)
            row = copy.copy(seed_nums)
            # row = self.reshape(row)
            puzzle.append(row)

        return puzzle


    def make_puzzle(self):
        diffs = {'easy':0.5, 'medium': 0.6, 'hard': 0.8}

        removal_rate = diffs[self.difficulty]
        num_to_remove = int(removal_rate * 81)
        self.puzzle = self.gen_puzzle()
        self.solution = copy.deepcopy(self.puzzle)

        #apply removal rate to puzzle
        for _ in range(num_to_remove):
            _range = [i for i in range(9)]
            x,y = random.choice(_range), random.choice(_range)
            self.puzzle[y][x] = None


        #print puzzle on board
        #construct mutability index
        self.mutablility_index = [[None for i in range(9)]for i in range(9)]
        for row_idx in range(len(self.puzzle)):
            for col_idx in range(len(self.puzzle)):
                
                x,y = col_idx, row_idx
                pos_x, pos_y = self.loc_to_pos(x,y)
                cell_id = y*9+x

                self.draw(pos_x, pos_y, self.puzzle[row_idx][col_idx], cell_id)

                #disallows player interaction with generated numbers
                curr = self.puzzle[row_idx][col_idx]
                mutability = True if curr == None else False
                self.mutablility_index[row_idx][col_idx] = mutability


    def draw(self, x, y, text, cell_id):
        # text = '' if text is None else text
        if text is not None:
            self.board.create_text(x, y, text=text, font=('Times', 20), tag= "."+str(cell_id) )
            

      
    def handle_button3(self, event):
        x,y = self.pos_to_loc(event.x, event.y)
        mutable = self.check_mutability(x,y)
        if mutable:
            cell_id = y*9+x
            # cell_id_str = "c" + str(cell_id)
            self.board.delete("." + str(cell_id) ) #num
            self.board.delete(".r" + str(cell_id) ) #rect

            # x,y = self.loc_to_pos(x,y)
            # self.crummy_delete(x,y)


    def cell_id_to_pos(self, cell_id):
        y = cell_id // 9
        x = cell_id - (y*9)

        pos_x,pos_y = self.loc_to_pos(x,y)
        return pos_x, pos_y


    def cell_id_to_loc(self, cell_id):
        y = cell_id // 9
        x = cell_id - (y*9)

        return x, y



    def solve(self):
        for row_idx in range(len(self.puzzle)):
            for col_idx in range(len(self.puzzle)):
                x,y = col_idx, row_idx
                correct = self.solution[row_idx][col_idx]
                curr = self.puzzle[row_idx][col_idx]
                if curr != correct:
                    cell_id = y*9+x
                    tag = "." + str(cell_id)
                    self.rect(x,y,"blue", cell_id )
                    x,y = self.loc_to_pos(x,y)
                    self.draw(x,y, correct, tag)
                    
                    



    def handle_choice_entry(self, cell_id):
        try:
            choice = int(self.choice.get())
            self.e.destroy()

            x,y = self.cell_id_to_loc(cell_id)
            if choice == self.solution[y][x]:
                self.rect(x,y,"green", cell_id)
            else:
                self.rect(x,y,"red", cell_id)



            x,y = self.cell_id_to_pos(cell_id)
            self.draw(x, y, choice, cell_id)
            x,y = self.pos_to_loc(x,y)
            self.puzzle[y][x] = choice
            if self.puzzle == self.solution:
                messagebox.showinfo("Gameover", "Game is oVer")
                self.root.destroy()

        except:
            messagebox.showinfo("Input Error", "invalid input")






    def gen_entry(self, pos_x, pos_y, cell_id):
        x,y = pos_x, pos_y
        self.choice = tk.StringVar(self.root)
        self.e = tk.Entry(self.board, textvariable=self.choice)
        self.e.bind('<Return>', lambda event : self.handle_choice_entry(cell_id))
        self.e.focus()
        # entry_window()

        # step = self.cellsize / 2
        # x1,x2 =  x-step, x+step
        # y1,y2 = y-step, y+step


        self.board.create_window(x,y,window = self.e, width=self.cellsize, height=self.cellsize)




    def handle_button1(self, event):
        x,y = self.pos_to_loc(event.x, event.y)
        
        mutable = self.check_mutability(x,y)
        if mutable:
            cell_id = y*9+x
            x,y = self.loc_to_pos(x,y)
            
            self.gen_entry(x,y, cell_id)
            # Input(self, cell_id)


    def crummy_delete(self, x, y):
        #Draws white square to cover location
        step  =self.cellsize // 2
        x1,x2 =  x-step, x+step
        y1,y2 = y-step, y+step

        self.board.create_rectangle(x1,y1,x2,y2)


    def rect(self, x, y, color, cell_id):
        rect_tag = ".r" + str(cell_id) 
        x,y = self.loc_to_pos(x,y)
        step  =self.cellsize / 2
        x1,x2 =  x-step, x+step
        y1,y2 = y-step, y+step

        self.board.create_rectangle(x1,y1,x2,y2, fill=color, tag=rect_tag)
        


    def check_mutability(self, x, y):
        item = self.mutablility_index[y][x]
        return item == True






if __name__ == "__main__":
    s = Sudoku(mode = 'main', difficulty='easy' )