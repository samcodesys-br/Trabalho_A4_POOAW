from model.Cell import Cell
from model.MineField import MineField
import random

def create_field(row,col,mines):
    matrix=[]
    
    for i in range(row):
        line=[]
        for j in range(col):
            cell = Cell(0,False,(i,j),False,False)
            line.append(cell)
        matrix.append(line)

    field=MineField(matrix,row,col,mines,0,0,mines)
    return field

def create_mines(mines):
    mines_created = 0
    coordenadas = set()  

    while mines_created < mines:
        row = random.randrange(0, 10)
        col = random.randrange(0, 10)
        pos = (row, col)
        
        if pos not in coordenadas:
            coordenadas.add(pos)
            mines_created += 1
        
    return list(coordenadas)

def get_neighbors(field,mines):
   
    neighbors = []
    fake_bomb_neighbors=[]
    rows, cols = field.row, field.col
    for mine in mines:
        cell_matrix=field.matrix[mine[0]][mine[1]]
        row,col=mine[0],mine[1]
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < rows and 0 <= new_col < cols:
                    neighbors.append((new_row, new_col))
                    if cell_matrix.valor==10:
                        fake_bomb_neighbors.append((new_row, new_col))

    for cell in neighbors:
        cell_matrix=field.matrix[cell[0]][cell[1]]
        if cell_matrix.valor<9:
            cell_matrix.valor+=1

    for cell in fake_bomb_neighbors:
        cell_matrix=field.matrix[cell[0]][cell[1]]
        cell_matrix.is_fake_bomb_neighbor=True
    
    return field
   
def put_mines(field,mines):
    # Atribuir valor 9 para bombas verdadeiras
    for i in range(min(15, len(mines))):        
        x, y = mines[i]
        if 0 <= x < field.row and 0 <= y < field.col:
            mine = Cell(9, False, (x,y), True, False)
            field.matrix[x][y] = mine

    # Atribuir valor 10 para bombas falsas
    for i in range(15, min(20, len(mines))):
        x, y = mines[i]
        if 0 <= x < field.row and 0 <= y < field.col:
            mine = Cell(10, False, (x,y), True, True)
            field.matrix[x][y] = mine

    return field

def reveal_cell(field,row, col):
    cell = field.matrix[row][col]
    cell.isRevealed = True
    
    if cell.isMine and not cell.isFake:
        return {'type': 'bomb', 'value': cell.valor, 'end_game': True}
    elif cell.isMine and cell.isFake:
        
        return {
            'type': 'fake', 
            'value': cell.valor
        }
    else:
        return {'type': 'number', 'value': cell.valor}

def toggle_flag(field, row, col):
    cell = field.matrix[row][col]
    if cell.isRevealed:
        return {'flagged': cell.flagged, 'flags': field.flags}  
    cell.flagged = not getattr(cell, 'flagged', False)
    if cell.flagged:
        field.flags -= 1
    else:
        field.flags += 1
    return {'flagged': cell.flagged, 'flags': field.flags}

def count_fake_bombs_found(field):
    count = 0
    for row in field.matrix:
        for cell in row:
            if cell.isRevealed and cell.isMine and cell.isFake:
                count += 1
    return count

def check_victory(field):
    for row in field.matrix:
        for cell in row:
            if not cell.isMine and not cell.isRevealed:
                return False
    return True
