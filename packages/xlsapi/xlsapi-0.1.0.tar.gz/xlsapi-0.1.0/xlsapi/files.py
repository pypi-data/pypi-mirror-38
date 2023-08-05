import os
from xlsapi.xlsreader import ExcelReader

class Files:

    def __init__(self, root = "./proddata"):
        self.__root = root
        self.__readers = {}
        self.__readers_list = []
        self.__cache_limit = 2
        self.scan()    

    def scan(self):
        self.__files = os.listdir(self.__root)
        self.__files.sort()

    def get_root(self):
        return self.__root
        
    def get_files(self):
        result = [file for file in self.__files if os.path.isfile(os.path.join(self.__root, file))]
        return result

    def is_file(self, name):
        file = os.path.join(self.__root, name)
        return os.path.isfile(file)

    def get_file(self, name):
        return os.path.join(self.__root, name)
    
    def get_reader(self, name):
        if name in self.__readers:
            return self.__readers[name]
        else:
            reader = ExcelReader(filename=name, datadir=self.__root)
            self.__readers[reader.filename()] = reader
            self.__readers_list.append(reader)
            if len(self.__readers_list) > self.__cache_limit:
                old = self.__readers_list.pop(0)
                del self.__readers[old.filename()]
            return reader
