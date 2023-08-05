import pyexcel as p
import os


class ExcelReader:

    def __init__(self, filename, datadir = "./proddata/"):
        self.__name = filename
        self.__file = os.path.join(datadir, filename)
        self.__sheet = "Tabelle 1"  
        self.__row = 0
        self.__col = 0
        self.load()

    def load(self):
        self.__book = p.get_book(file_name=self.__file)
        self.__sheet = self.__book.sheet_names()[0]

    def get_book(self):
        return self.__book

    def get_sheets(self):
        return self.__book.sheet_names()

    def get_sheet(self, name):
        return self.__book.sheet_by_name(name)

    def start(self):
        return (self.__row, self.__col)

    def sheet(self):
        return self.__sheet

    def filename(self):
        return self.__name

    def filepath(self):
        return self.__file

    def set_sheet(self, sheetname):
        self.__sheet = sheetname

    def set_start(self, row, col):
        self.__row = row
        self.__col = col

    def read(self):
        self.__records = p.get_records(
            name_columns_by_row=0, 
            file_name=self.__file, 
            start_row=self.__row, 
            start_column=self.__col, 
            sheet_name=self.__sheet)
        return self.count()

    def count(self):
        return len(self.__records)
    
    def get(self, row):
        return self.__records[row]

    def get_all(self):
        return [r for r in self.__records]

    def save(self, name=None):
        if name == None:
            return self.__book.save_as(self.__file)
        else:
            d = os.path.dirname(self.__file)
            f = os.path.join(d, name)
            return self.__book.save_as(f)
