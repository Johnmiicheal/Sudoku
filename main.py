import tkinter as tk

class Sudoku:
    def __init__(self):
        self.width, self.height = 800,800
        self.build()


    def build(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(width=False, height=False)

        self.board = tk.Canvas(self.root,width=self.width, height=self.height)
        self.board.pack()
        self.gen_lines(7,3)

        self.root.mainloop()


    def gen_lines_recursive(self, x, y, length,width):
        step = length // 3
        pos = [step*i for i in range(1,3)]

        #main grid lines
        for i in range(2):
            self.board.create_line(x, y+pos[i], x+length, y+pos[i], width=width) #horizontal lines
            self.board.create_line(x+pos[i],y,x+pos[i], y+length, width= width) #vertical lines
    
    def gen_lines(self, b_width,s_width):

        self.gen_lines_recursive(0,0, self.width,  b_width)
        # step = self.width // 3
        # pos = [step*i for i in range(1,3)]

        # #main grid lines
        # for i in range(2):
        #     self.board.create_line(0,pos[i], self.width,pos[i], width=b_width) #vertical lines
        #     self.board.create_line(pos[i],0,pos[i],self.height, width= b_width) #horizontal lines


        # step = step // 3
        # pos = [step*i for i in range(1,3]
        # #inner grid lines
        # for i in range(9):
        #     for j in range(3):
        #         #verts
        #         self.board.create_line(pos)


        # step2 = step//3
        # pos2 = [step2*i for i in range(1,3)]

        
        tlc = {} #idx to pos
        for y in range(3):
            for x in range(3):
                tlc[y*3+x] = [y,x] 
        
        print(tlc)

        small_step  = self.width//3
        for i in range(9):
            y,x = [idx*small_step for idx in tlc[i]]
            self.gen_lines_recursive(x, y, small_step, s_width)


        # for i in range(9):
        #     x,y = [i*step2 for i in tlc[i]]
            
            
        #     for i in range(2):
        #         self.board.create_line(x,y, step+x,y, width=s_width)
        #         self.board.create_line(x,y, x,step+y, width=s_width)

                # self.board.create_line(pos2[i],0,pos2[i],step, width= b_width)

            



if __name__ == "__main__":
    Sudoku()