import service.GameService as service
import ast
from model.Cell import Cell
from model.MineField import MineField

class FieldController():
    
    @staticmethod
    def initGame():
        field=service.create_field(10, 10,20)
        

        mines=service.create_mines(20)

        field=service.put_mines(field,mines)
        field=service.get_neighbors(field,mines)

        return field

    @staticmethod
    def reveal_cell(field,row, col):
        return service.reveal_cell(field,int(row), int(col))

    @staticmethod
    def toggle_flag(field, row, col):
        return service.toggle_flag(field, int(row), int(col))

    @staticmethod
    def check_victory(field):
        return service.check_victory(field)