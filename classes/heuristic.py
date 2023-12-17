class Heuristic:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells_record = [[0 for y in range(rows)] for x in range(cols)]

    def SetRecord(self, cell, distance):
        self.cells_record[cell.x][cell.y] = distance

    def GetRecord(self, cell):
        return self.cells_record[cell.x][cell.y]
