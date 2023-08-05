from xlsapi.server import xlsapi


def get_files():
    return xlsapi().get_files()


def xls(fname, sname=None, row=0, col=0):
    return xlsapi().xls(fname, sname, col, row)


def xls_sheets(fname):
    return xlsapi().xls_sheets(fname)


def xls_sheet(fname, sname):
    return xlsapi().xls_sheet(fname, sname)


def xls_records(fname, sname, row=0, col=0):
    return xlsapi().xls_records(fname, sname, row, col)


def xls_data(fname, sname, row, col):
    return xlsapi().xls_data(fname, sname, row, col)


def xls_update(fname, sname, row, col, value):
    return xlsapi().xls_update(fname, sname, row, col, value)


def xls_rows(fname, sname):
    return xlsapi().xls_rows(fname, sname)


def xls_add_row(fname, sname, values, save=False):
    return xlsapi().xls_add_row(fname, sname, values)
