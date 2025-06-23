class Cell():
    
    def __init__(self,valor:int,isRevealed:bool,coord,isMine:bool,isFake:bool, flagged=False):
        self.isRevealed=isRevealed
        self.coord=coord
        self.isMine=isMine
        self.isFake=isFake
        self.valor=valor
        self.flagged=flagged
        self.is_fake_bomb_neighbor=False

    def __str__(self):
        return f'{self.valor:02d}:{int(self.isRevealed)}:{int(self.isMine)}:{int(self.isFake)}:{int(self.flagged)}'
        