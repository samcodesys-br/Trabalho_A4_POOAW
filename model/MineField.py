from model import Cell

class MineField():
    def __init__(self,matrix,row,col,flags,score,time,mines):
        self.matrix=matrix
        self.row=row
        self.col=col
        self.flags=flags
        self.score=score
        self.time=time
        self.mines=mines
