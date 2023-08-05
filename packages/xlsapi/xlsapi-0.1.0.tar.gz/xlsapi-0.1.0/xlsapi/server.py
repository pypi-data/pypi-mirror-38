import connexion
from flask import abort, request

from xlsapi.files import Files
from xlsapi.demo import Demo
from xlsapi.notification import Notification


def create_new_xlsapi(root):
    global xlsapi_instance
    xlsapi_instance = Server(root)
    return xlsapi_instance

def xlsapi(root='./proddata'):
    if 'xlsapi_instance' not in globals():
        global xlsapi_instance
        xlsapi_instance = Server(root)
    return xlsapi_instance


def create_demo(root='./proddata', push=True):
    api = xlsapi()

    flask = api.get_flask_app()
    flask.config['ENV'] = 'development'
    flask.config['TESTING'] = True

    app = api.get_app()
    Demo(api)
    if push:
        Notification(api)

    return app


class Server:

    @staticmethod
    def read(reader):
        try:
            reader.read()
        except ValueError:
            abort(404, "Sheet with name {sheet} not found in file {name}".format(name=reader.filename(), sheet=reader.sheet()))

    @staticmethod
    def parse_value(data):
        try:
            return int(data)
        except ValueError:
            try:
                return float(data)
            except ValueError:
                return data

    @staticmethod
    def to_row(values):
        row = []
        for value in values:
            row.append(Server.parse_value(value))
        return row

    @staticmethod
    def create_message(fname, sname):
        return "{\"file\": \"" + fname + "\", \"sheet\": \"" + sname + "\"}"

    def __init__(self, root):
        self.__files = Files(root)
        self.__app = connexion.App(__name__, specification_dir='./')
        self.__app.add_api('swagger.yml')
        self.__push = None

    def register_push(self, callback):
        self.__push = callback

    def get_app(self):
        return self.__app

    def get_flask_app(self):
        return self.__app.app

    def files(self):
        return self.__files

    def get_reader(self, fname):
        files = self.files()
        if files.is_file(fname):
            return files.get_reader(fname)
        else:
            abort(404, "File with name {name} not found".format(name=fname))

    def get_sheet(self, fname, sname):
        reader = self.get_reader(fname)
        try:
            return reader.get_sheet(sname)
        except KeyError:
            abort(404, "Sheet with name {sheet} not found in file {name}".format(name=fname, sheet=sname))

    def get_files(self):
        return self.__files.get_files()

    def xls(self, fname, sname=None, row=0, col=0):
        reader = self.get_reader(fname)
        if sname is not None:
            reader.set_sheet(sname)
        reader.set_start(row, col)
        Server.read(reader)
        return reader.get_all()

    def xls_sheets(self, fname):
        reader = self.get_reader(fname)
        return reader.get_sheets()

    def xls_sheet(self, fname, sname):
        sheet = self.get_sheet(fname, sname)
        return sheet.to_array()

    def xls_records(self, fname, sname, row=0, col=0):
        reader = self.get_reader(fname)
        reader.set_start(row, col)
        reader.set_sheet(sname)
        Server.read(reader)
        return reader.get_all()

    def xls_data(self, fname, sname, row, col):
        sheet = self.get_sheet(fname, sname)
        return sheet[row, col]

    def xls_update(self, fname, sname, row, col, value):
        reader = self.get_reader(fname)
        sheet = self.get_sheet(fname, sname)
        sheet[row, col] = Server.parse_value(value)
        reader.save()
        reader.load()

        if self.__push is not None:
            self.__push(Server.create_message(fname, sname))

        return reader.get_sheet(sname)[row, col]

    def xls_rows(self, fname, sname):
        sheet = self.get_sheet(fname, sname)
        return sheet.to_array()

    def xls_add_row(self, fname, sname, values, save=True):
        reader = self.get_reader(fname)
        sheet = self.get_sheet(fname, sname)

        row = Server.to_row(values)
        sheet.extend_rows([row])
        if save:
            reader.save()

        if self.__push is not None:
            self.__push(Server.create_message(fname, sname))

        data = sheet.to_array()
        return data[len(data) - 1]
