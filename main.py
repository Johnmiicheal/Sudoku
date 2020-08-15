import tkinter as tk
import random
import copy
from tkinter import messagebox

class Sudoku:
    def __init__(self, difficulty,method="backtrack"):

        self.width, self.height = 800,800
        self.difficulty = difficulty
        self.linewd_sm, self.linewidth_bg = 3,7
        self.cellsize =  self.width // 9
        self.entry = False
        self.method=method #backtrack or shift
        self.build()
        # self.use_backtracking()


    def build(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width+100}x{self.height+30}")
        self.root.resizable(width=False, height=False)

        self.board = tk.Canvas(self.root,width=self.width, height=self.height)
        self.board.bind("<Button-1>", self.handle_button1)
        self.board.bind("<Button-3>", self.handle_button3) 
        self.board.grid(row=0,column=1, pady=15, padx=15)

        self.buttons = tk.Frame(self.root)
        self.buttons.grid(row=0,column=0, pady=10)

        self.solve_btn =  tk.Button(self.buttons, text=' SOLVE ', command=self.solve, fg='blue')
        self.solve_btn.grid(row=0,column=0)

        self.restart_btn = tk.Button(self.buttons, text='RESTART', command=self.restart, fg='red')
        self.restart_btn.grid(row=1,column=0)


        self.gen_lines()
        self.make_puzzle()

        self.root.mainloop()


    def gen_lines_helper(self, x, y, length,width):
        step = length // 3
        pos = [step*i for i in range(1,3)]

        for i in range(2):
            self.board.create_line(x, y+pos[i], x+length, y+pos[i], width=width) #horizontal lines
            self.board.create_line(x+pos[i],y,x+pos[i], y+length, width= width) #vertical lines
    
    def gen_lines(self):
        self.gen_lines_helper(0,0, self.width, self.linewidth_bg) # draw main lines

        tlc = {} #index -> location map
        for y in range(3):
            for x in range(3):
                tlc[y*3+x] = [y,x] 

        small_step  = self.width//3
        for i in range(9):
            y,x = [idx*small_step for idx in tlc[i]]
            self.gen_lines_helper(x, y, small_step, self.linewd_sm) #draw small lines


    def gen_puzzle(self):
        """Generates solved sudoku using array shift method"""
        
        #generate seed nums to be shifted
        seed_nums = [i for i in range(1,10)]
        random.shuffle(seed_nums)

        shift_fn = lambda L, shift :  L[shift:] + L[:shift] #convenient list shifting

        puzzle = []
        shift_vals  = [0,3,3,1,3,3,1,3,3]
        for shift in shift_vals:
            seed_nums = shift_fn(seed_nums, shift)
            row = copy.copy(seed_nums)
            puzzle.append(row)

        return puzzle


    def checkGrid(self,grid):
        """Check if grid is full"""
        for row in range(0,9):
            for col in range(0,9):
                if grid[row][col]==0:
                    return False 
        return True 



    



    def gen_puzzle2(self):
        """Using backtracking"""
        self._p2_counter = 0
        #Find next empty cell
        for i in range(0,81):
            row=i//9
            col=i%9
            if self._p2_grid[row][col]==0:
                random.shuffle(self.numberlist)
                for value in self.numberlist:
                    if not(value in self._p2_grid[row]): # check value not in row
                        if not value in ([self._p2_grid[i][col] for i in range(9)]): #Check value not in column
                        #Find current square and check val not in square
                            square=[]
                            if row<3:
                                if col<3:
                                    square=[self._p2_grid[i][0:3] for i in range(0,3)]
                                elif col<6:
                                    square=[self._p2_grid[i][3:6] for i in range(0,3)]
                                else:  
                                    square=[self._p2_grid[i][6:9] for i in range(0,3)]
                            elif row<6:
                                if col<3:
                                    square=[self._p2_grid[i][0:3] for i in range(3,6)]
                                elif col<6:
                                    square=[self._p2_grid[i][3:6] for i in range(3,6)]
                                else:  
                                    square=[self._p2_grid[i][6:9] for i in range(3,6)]
                            else:
                                if col<3:
                                    square=[self._p2_grid[i][0:3] for i in range(6,9)]
                                elif col<6:
                                    square=[self._p2_grid[i][3:6] for i in range(6,9)]
                                else:  
                                    square=[self._p2_grid[i][6:9] for i in range(6,9)]

                            #Check that this value has not already be used on this 3x3 square
                            if not value in (square[0] + square[1] + square[2]):
                                self._p2_grid[row][col]=value
                                if self.checkGrid(self._p2_grid ):
                                    self._p2_counter+=1
                                    break
                                else:
                                    if self.gen_puzzle2():
                                        return True
                # break
            # self._p2_grid[row][col]=0 



    def use_backtracking(self):
        self._p2_grid = [[0 for i in range(9)] for i in range(9)]
        self.numberlist = [1,2,3,4,5,6,7,8,9]
        self.gen_puzzle2()
        # print(self._p2_grid)
        return self._p2_grid





    def make_puzzle(self):
        """Applies removal rate, mutability index to solved sudoku and draws puzzle on board"""

        diffs = {'easy':0.5, 'medium': 0.6, 'hard': 0.8}
        self.solution = self.gen_puzzle() if self.method=="shift" else self.use_backtracking()
        self.puzzle = copy.deepcopy(self.solution)
        
        #apply removal rate to puzzle
        removal_rate = diffs[self.difficulty]
        num_to_remove = int(removal_rate * 81)

        # empty random indexes in range num_to_remove
        for _ in range(num_to_remove):
            _range = [i for i in range(9)]
            x,y = random.choice(_range), random.choice(_range)
            self.puzzle[y][x] = None


        #print puzzle on board && construct mutability index
        self.mutablility_index = [[None for i in range(9)]for i in range(9)]

        for y in range(len(self.puzzle)):
            for x in range(len(self.puzzle)):                
                curr = self.puzzle[y][x]

                cell_id = y*9+x
                self.draw(curr, cell_id)

                #check mutability 
                self.mutablility_index[y][x] = True if curr == None else False


    def solve(self):
        """Solve puzzle, apply solution matrix"""
        for y in range(len(self.puzzle)):
            for x in range(len(self.puzzle)):

                correct = self.solution[y][x]
                curr = self.puzzle[y][x]

                if curr != correct:
                    cell_id = y*9+x
                    self.rect("blue", cell_id )
                    self.draw(correct, cell_id)
                    
                    
    def restart(self):
        """Restart puzzle, clear all mutable choices"""

        for y in range(len(self.puzzle)):
            for x in range(len(self.puzzle)):
                if self.mutable(x,y):
                    cell_id = y*9+x
                    self.board.delete( "." + str(cell_id))
                    self.board.delete(".r" + str(cell_id) )


    def handle_choice(self, cell_id):
        """Handles choice made in entry widget"""
        try:

            x,y = self.cell_id_to_loc(cell_id)
            
            choice = int(self.choice.get())
            self.e.destroy()

            # draw choice on board
            color = "green" if choice == self.solution[y][x] else "red" 
            self.rect(color, cell_id)
            self.draw(choice, cell_id)


            # add choice to puzzle and check completeness            
            self.puzzle[y][x] = choice
            if self.puzzle == self.solution:
                messagebox.showinfo("Game Over", "You Won!")
                self.root.destroy()
                self.entry = False

        except:
            messagebox.showinfo("Input Error", "Invalid Input. Only integers from 1-9 inclusive.")


    def gen_entry(self, cell_id):
        """Generates entry widget on cell"""

        #Delete existing entry, if any
        
        if self.entry is False:
            self.entry = True
            pos_x, pos_y = self.cell_id_to_pos(cell_id)

            self.choice = tk.StringVar(self.root)
            self.e = tk.Entry(self.board, textvariable=self.choice)
            self.e.bind('<Return>', lambda event : self.handle_choice(cell_id))
            self.e.focus()
            
            self.board.create_window(pos_x,pos_y,window = self.e, width=self.cellsize, height=self.cellsize)


    def handle_button1(self, event):
        """On left click"""
        x,y = self.pos_to_loc(event.x, event.y)
        if self.mutable(x,y):
            cell_id = y*9+x
            self.gen_entry(cell_id)


    def handle_button3(self, event):
        """On right click"""

        x,y = self.pos_to_loc(event.x, event.y)
        if self.mutable(x,y):
            cell_id = y*9+x
            self.board.delete("." + str(cell_id) )
            self.board.delete(".r" + str(cell_id) )     


    def draw(self, text, cell_id):
        """Draw text on cell"""
        x,y = self.cell_id_to_pos(cell_id)
        if text is not None:
            self.board.create_text(x, y, text=text, font=('Times', 20), tag= "."+str(cell_id) )


    def rect(self, color, cell_id):
        """Highlight cell"""
        x,y = self.cell_id_to_pos(cell_id)
        rect_tag = ".r" + str(cell_id) 

        #get rectangle limits
        step = (self.cellsize / 2) + 1
        x1,x2 = x-step, x+step
        y1,y2 = y-step, y+step

        self.board.create_rectangle(x1,y1,x2,y2, fill=color, tag=rect_tag)
        

    mutable = lambda self, x, y: self.mutablility_index[y][x] #return cell mutability


    def pos_to_loc(self, x, y):
        loc_x = x// self.cellsize
        loc_y = y// self.cellsize
        return loc_x, loc_y
        

    def cell_id_to_pos(self, cell_id):
        y = cell_id // 9
        x = cell_id - (y*9)

        pos_x, pos_y = x*self.cellsize, y*self.cellsize

        #center positions
        pos_x += self.cellsize // 2
        pos_y += self.cellsize // 2

        return pos_x, pos_y


    def cell_id_to_loc(self, cell_id):
        y = cell_id // 9
        x = cell_id - (y*9)
        return x, y





if __name__ == "__main__":
    s = Sudoku(difficulty='easy')